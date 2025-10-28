import hashlib
import json
from typing import Optional, Dict, List
from enum import Enum
import redis
import deepl
from google.cloud import translate_v2 as translate
from sqlalchemy.orm import Session
from app.core.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

def get_settings_from_db():
    """DB에서 시스템 설정 가져오기"""
    try:
        from app.db.database import SessionLocal
        from app.models.admin import SystemSettings

        db = SessionLocal()
        settings_dict = {}

        # 번역 관련 설정 가져오기
        translation_settings = db.query(SystemSettings).filter(
            SystemSettings.category == "translation"
        ).all()

        for setting in translation_settings:
            settings_dict[setting.key] = setting.value

        db.close()
        return settings_dict
    except Exception as e:
        logger.error(f"DB에서 설정 가져오기 실패: {e}")
        return {}

class TranslationProvider(str, Enum):
    GOOGLE = "google"
    DEEPL = "deepl"

class TranslationService:
    def __init__(self):
        # Redis 클라이언트 초기화 (개발 시에는 None으로 설정)
        try:
            self.redis_client = redis.from_url(
                settings.REDIS_URL,
                decode_responses=True
            )
            # 연결 테스트
            self.redis_client.ping()
        except:
            logger.warning("Redis 연결 실패 - 캐시 없이 진행합니다")
            self.redis_client = None

        # DB에서 설정 가져오기
        db_settings = get_settings_from_db()

        # 번역 프로바이더 초기화
        provider_name = db_settings.get('translation_provider') or getattr(settings, 'TRANSLATION_PROVIDER', 'deepl')
        self.provider = TranslationProvider(provider_name.lower())
        logger.info(f"번역 프로바이더: {self.provider.value}")

        # Google Translation 클라이언트
        self.google_client = None
        if settings.GOOGLE_APPLICATION_CREDENTIALS:
            try:
                self.google_client = translate.Client()
            except Exception as e:
                logger.error(f"Google Translation 클라이언트 초기화 실패: {e}")

        # DeepL 클라이언트
        self.deepl_client = None
        # DB에서 DeepL API Key 가져오기 (우선순위: DB > 환경변수)
        deepl_api_key = db_settings.get('deepl_api_key') or getattr(settings, 'DEEPL_API_KEY', None)

        if deepl_api_key:
            try:
                self.deepl_client = deepl.Translator(deepl_api_key)
                logger.info(f"DeepL 클라이언트 초기화 성공 (API Key: {deepl_api_key[:20]}...)")
            except Exception as e:
                logger.error(f"DeepL 클라이언트 초기화 실패: {e}")
        else:
            logger.warning("DeepL API Key가 설정되지 않았습니다")

    def _get_cache_key(self, text: str, source_lang: str, target_lang: str) -> str:
        """캐시 키 생성"""
        content = f"{text}:{source_lang}:{target_lang}"
        return f"translation:{hashlib.sha256(content.encode()).hexdigest()}"

    async def translate_text(
        self,
        text: str,
        target_lang: str,
        source_lang: Optional[str] = None
    ) -> Dict[str, str]:
        """
        텍스트 번역

        Args:
            text: 번역할 텍스트
            target_lang: 대상 언어 코드 (ko, ru)
            source_lang: 소스 언어 코드 (None이면 자동 감지)

        Returns:
            {
                "translated_text": "번역된 텍스트",
                "source_lang": "감지된 소스 언어",
                "target_lang": "대상 언어",
                "cached": bool
            }
        """
        if not text or not text.strip():
            return {
                "translated_text": "",
                "source_lang": source_lang or "ko",
                "target_lang": target_lang,
                "cached": False
            }

        # 캐시 확인 (Redis가 사용 가능한 경우에만)
        cached_result = None
        if self.redis_client:
            try:
                cache_key = self._get_cache_key(text, source_lang or "auto", target_lang)
                cached_result = self.redis_client.get(cache_key)
            except:
                pass

        if cached_result:
            result = json.loads(cached_result)
            result["cached"] = True
            return result

        # 번역 수행
        result = await self._perform_translation(text, target_lang, source_lang)

        # 캐시 저장 (24시간) - Redis가 사용 가능한 경우에만
        if self.redis_client:
            try:
                cache_key = self._get_cache_key(text, source_lang or "auto", target_lang)
                self.redis_client.setex(
                    cache_key,
                    86400,  # 24 hours
                    json.dumps(result)
                )
            except:
                pass

        result["cached"] = False
        return result

    async def _perform_translation(
        self,
        text: str,
        target_lang: str,
        source_lang: Optional[str] = None
    ) -> Dict[str, str]:
        """실제 번역 수행"""
        if self.provider == TranslationProvider.GOOGLE:
            return await self._translate_with_google(text, target_lang, source_lang)
        elif self.provider == TranslationProvider.DEEPL:
            return await self._translate_with_deepl(text, target_lang, source_lang)
        else:
            raise ValueError(f"지원하지 않는 번역 프로바이더: {self.provider}")

    async def _translate_with_google(
        self,
        text: str,
        target_lang: str,
        source_lang: Optional[str] = None
    ) -> Dict[str, str]:
        """Google Cloud Translation API를 사용한 번역"""
        if not self.google_client:
            logger.error("Google Translation 클라이언트가 초기화되지 않았습니다")
            return {
                "translated_text": text,
                "source_lang": source_lang or "ko",
                "target_lang": target_lang
            }

        try:
            # Google Translation API 호출
            result = self.google_client.translate(
                text,
                target_language=target_lang,
                source_language=source_lang
            )

            return {
                "translated_text": result["translatedText"],
                "source_lang": result.get("detectedSourceLanguage", source_lang or "ko"),
                "target_lang": target_lang
            }
        except Exception as e:
            logger.error(f"Google 번역 실패: {e}")
            return {
                "translated_text": text,
                "source_lang": source_lang or "ko",
                "target_lang": target_lang
            }

    async def _translate_with_deepl(
        self,
        text: str,
        target_lang: str,
        source_lang: Optional[str] = None
    ) -> Dict[str, str]:
        """DeepL API를 사용한 번역"""
        if not self.deepl_client:
            logger.error("DeepL 클라이언트가 초기화되지 않았습니다")
            return {
                "translated_text": text,
                "source_lang": source_lang or "ko",
                "target_lang": target_lang
            }

        try:
            # DeepL 언어 코드 매핑 (KO → KO, RU → RU, EN → EN-US)
            deepl_target_lang = target_lang.upper()
            if deepl_target_lang == "EN":
                deepl_target_lang = "EN-US"

            deepl_source_lang = None
            if source_lang:
                deepl_source_lang = source_lang.upper()

            # DeepL API 호출
            result = self.deepl_client.translate_text(
                text,
                target_lang=deepl_target_lang,
                source_lang=deepl_source_lang
            )

            detected_lang = result.detected_source_lang.lower() if result.detected_source_lang else (source_lang or "ko")

            return {
                "translated_text": result.text,
                "source_lang": detected_lang,
                "target_lang": target_lang
            }
        except Exception as e:
            logger.error(f"DeepL 번역 실패: {e}")
            return {
                "translated_text": text,
                "source_lang": source_lang or "ko",
                "target_lang": target_lang
            }


    async def translate_batch(
        self,
        texts: List[str],
        target_lang: str,
        source_lang: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """여러 텍스트를 일괄 번역"""
        results = []
        for text in texts:
            result = await self.translate_text(text, target_lang, source_lang)
            results.append(result)
        return results

    async def translate_content(
        self,
        content: Dict[str, str],
        target_langs: List[str],
        source_lang: Optional[str] = None
    ) -> Dict[str, Dict[str, str]]:
        """
        콘텐츠를 여러 언어로 번역

        Args:
            content: {"title": "제목", "content": "내용", ...}
            target_langs: ["ko", "ru"]
            source_lang: 소스 언어

        Returns:
            {
                "ko": {"title": "...", "content": "..."},
                "ru": {"title": "...", "content": "..."}
            }
        """
        translations = {}

        for lang in target_langs:
            if lang == source_lang:
                translations[lang] = content
                continue

            translated = {}
            for key, value in content.items():
                if isinstance(value, str) and value:
                    result = await self.translate_text(value, lang, source_lang)
                    translated[key] = result["translated_text"]
                else:
                    translated[key] = value

            translations[lang] = translated

        return translations

    def detect_language(self, text: str) -> str:
        """언어 자동 감지"""
        if not self.google_client:
            # 간단한 휴리스틱 기반 감지
            if any(ord(char) >= 0x0400 and ord(char) <= 0x04FF for char in text):
                return "ru"  # 키릴 문자 감지
            elif any(ord(char) >= 0xAC00 and ord(char) <= 0xD7AF for char in text):
                return "ko"  # 한글 감지
            else:
                return "en"

        try:
            result = self.google_client.detect_language(text)
            return result["language"]
        except Exception as e:
            logger.error(f"언어 감지 실패: {e}")
            return "ko"

    async def check_rate_limit(self, user_id: int) -> bool:
        """사용자별 번역 요청 제한 확인"""
        if not self.redis_client:
            # Redis가 없으면 제한하지 않음
            return True

        try:
            key = f"translation_rate:{user_id}"
            current_count = self.redis_client.get(key)

            if current_count is None:
                # 처음 요청
                self.redis_client.setex(key, 60, 1)
                return True

            current_count = int(current_count)
            if current_count >= settings.TRANSLATION_RATE_LIMIT_PER_MINUTE:
                return False

            self.redis_client.incr(key)
            return True
        except:
            # Redis 오류 시 제한하지 않음
            return True

    def clear_cache(self, pattern: Optional[str] = None):
        """번역 캐시 삭제"""
        if pattern:
            keys = self.redis_client.keys(f"translation:*{pattern}*")
        else:
            keys = self.redis_client.keys("translation:*")

        if keys:
            self.redis_client.delete(*keys)
            logger.info(f"{len(keys)}개의 번역 캐시가 삭제되었습니다")

# 싱글톤 인스턴스
translation_service = TranslationService()