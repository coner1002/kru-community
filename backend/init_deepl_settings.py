"""DeepL API 설정 초기화 스크립트"""
import sys
import os
import io

# Windows 콘솔 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.append(os.path.dirname(__file__))

from sqlalchemy.orm import Session
from app.db.database import engine, SessionLocal
from app.models.admin import SystemSettings
from datetime import datetime

def init_deepl_settings():
    """DeepL API Key 설정 초기화"""
    db: Session = SessionLocal()

    try:
        # DeepL API Key 설정 확인
        deepl_setting = db.query(SystemSettings).filter(
            SystemSettings.key == "deepl_api_key"
        ).first()

        if not deepl_setting:
            # DeepL API Key 설정 생성
            deepl_setting = SystemSettings(
                key="deepl_api_key",
                value="8ea8ad3f-c670-4df8-b1b4-abd4fe050c94:fx",
                description="DeepL Translation API Key",
                category="translation",
                is_encrypted=False,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(deepl_setting)
            print("✅ DeepL API Key 설정 생성됨")
        else:
            print(f"ℹ️  DeepL API Key 이미 존재: {deepl_setting.value[:20]}...")

        # Translation Provider 설정
        provider_setting = db.query(SystemSettings).filter(
            SystemSettings.key == "translation_provider"
        ).first()

        if not provider_setting:
            provider_setting = SystemSettings(
                key="translation_provider",
                value="deepl",  # "google" or "deepl"
                description="Translation Service Provider (google or deepl)",
                category="translation",
                is_encrypted=False,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(provider_setting)
            print("✅ Translation Provider 설정 생성됨 (DeepL)")
        else:
            print(f"ℹ️  Translation Provider: {provider_setting.value}")

        db.commit()
        print("\n✅ DeepL 설정 초기화 완료!")

    except Exception as e:
        db.rollback()
        print(f"❌ 오류 발생: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("DeepL API 설정 초기화 시작...")
    init_deepl_settings()
