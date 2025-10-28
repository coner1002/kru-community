# 자동 번역 기능 설정 가이드

DeepL API를 사용한 게시글 자동 번역 기능 설정 및 사용 방법입니다.

## 📋 목차

1. [기능 개요](#기능-개요)
2. [설치 및 설정](#설치-및-설정)
3. [사용 방법](#사용-방법)
4. [API 엔드포인트](#api-엔드포인트)
5. [테스트](#테스트)

---

## 🎯 기능 개요

### 주요 기능
- ✅ 게시글 작성 시 한국어 ↔ 러시아어 자동 번역
- ✅ 언어 자동 감지 (한글/키릴 문자)
- ✅ DeepL API 연동 (고품질 번역)
- ✅ 원문/번역본 동시 저장
- ✅ 사용자 언어 설정에 따른 자동 표시
- ✅ 원문 보기/번역 보기 토글 기능

### 지원 언어
- 🇰🇷 한국어 (ko)
- 🇷🇺 러시아어 (ru)

---

## 🛠️ 설치 및 설정

### 1. 백엔드 패키지 설치

```bash
cd backend
pip install -r requirements.txt
```

새로 추가된 패키지:
- `deepl==1.16.1` - DeepL API 클라이언트

### 2. 환경 변수 설정

`backend/.env` 파일에 다음 설정을 추가하세요:

```env
# Translation
DEEPL_API_KEY=BTLrkuUyQSku9G9V5
TRANSLATION_PROVIDER=deepl
```

### 3. 데이터베이스 확인

데이터베이스 테이블이 이미 번역 필드를 포함하고 있습니다:
- `translated_title_ko`, `translated_title_ru`
- `translated_content_ko`, `translated_content_ru`
- `translated_summary_ko`, `translated_summary_ru`
- `auto_translated` (번역 여부 플래그)
- `source_lang` (원문 언어)

### 4. 서버 시작

```bash
# 백엔드 서버
cd backend
uvicorn app.main:app --reload --port 8000

# 프론트엔드 서버 (별도 터미널)
cd frontend
npm run dev
```

---

## 📝 사용 방법

### 게시글 작성

1. **언어 자동 감지**
   - 제목이나 내용을 입력하면 자동으로 언어를 감지합니다
   - 한글이 포함되면 한국어, 키릴 문자가 포함되면 러시아어로 감지

2. **자동 번역 옵션**
   - 기본적으로 "자동 번역" 옵션이 활성화되어 있습니다
   - 체크박스를 해제하면 번역 없이 원문만 저장됩니다

3. **게시글 작성 흐름**
   ```
   사용자 입력 → 언어 감지 → 게시글 저장 → DeepL API 호출 → 번역 저장 → 완료
   ```

### 게시글 보기

1. **자동 언어 표시**
   - 사용자의 언어 설정에 따라 자동으로 번역된 내용을 표시합니다
   - 한국어 사용자: 한국어 버전 표시
   - 러시아어 사용자: 러시아어 버전 표시

2. **원문/번역 토글**
   - "원문 보기" 버튼을 클릭하여 원본 언어로 작성된 글을 확인할 수 있습니다
   - "번역 보기" 버튼을 클릭하여 다시 번역된 버전을 볼 수 있습니다

---

## 🔌 API 엔드포인트

### 1. 게시글 생성

**POST** `/api/posts/`

**Request Body:**
```json
{
  "title": "안녕하세요",
  "content": "이것은 테스트 게시글입니다.",
  "summary": "테스트 요약",
  "category_id": 1,
  "tags": ["테스트", "공지"],
  "source_lang": "ko",
  "auto_translate": true,
  "allow_comments": true
}
```

**Response:**
```json
{
  "id": 1,
  "title": "안녕하세요",
  "content": "이것은 테스트 게시글입니다.",
  "source_lang": "ko",
  "translated_title_ko": "안녕하세요",
  "translated_title_ru": "Здравствуйте",
  "translated_content_ko": "이것은 테스트 게시글입니다.",
  "translated_content_ru": "Это тестовая статья.",
  "auto_translated": true,
  "created_at": "2025-10-02T12:00:00Z",
  ...
}
```

### 2. 게시글 목록 조회

**GET** `/api/posts/?page=1&page_size=20`

**Response:**
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "page_size": 20,
  "total_pages": 5
}
```

### 3. 게시글 상세 조회

**GET** `/api/posts/{post_id}`

### 4. 게시글 수정

**PUT** `/api/posts/{post_id}`

제목이나 내용이 수정되면 자동으로 재번역됩니다.

### 5. 게시글 삭제

**DELETE** `/api/posts/{post_id}`

---

## 🧪 테스트

### 1. 수동 테스트 (cURL)

**한국어 게시글 작성:**
```bash
curl -X POST "http://localhost:8000/api/posts/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "안녕하세요",
    "content": "이것은 한국어로 작성된 게시글입니다.",
    "category_id": 1,
    "source_lang": "ko",
    "auto_translate": true
  }'
```

**러시아어 게시글 작성:**
```bash
curl -X POST "http://localhost:8000/api/posts/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Привет",
    "content": "Это статья на русском языке.",
    "category_id": 1,
    "source_lang": "ru",
    "auto_translate": true
  }'
```

### 2. 프론트엔드 컴포넌트 사용

```tsx
import PostEditor from '@/components/post/post-editor';
import PostView from '@/components/post/post-view';

// 게시글 작성
<PostEditor
  categoryId={1}
  onSuccess={(postId) => console.log('Created:', postId)}
/>

// 게시글 보기
<PostView
  post={postData}
  userLanguage="ko"
/>
```

### 3. 테스트 시나리오

#### 시나리오 1: 한국어 → 러시아어 번역
1. 제목: "안녕하세요"
2. 내용: "한국-러시아 커뮤니티에 오신 것을 환영합니다."
3. 예상 번역: "Здравствуйте" / "Добро пожаловать в корейско-российское сообщество."

#### 시나리오 2: 러시아어 → 한국어 번역
1. 제목: "Новости"
2. 내용: "Важная информация для всех участников."
3. 예상 번역: "뉴스" / "모든 회원을 위한 중요한 정보."

#### 시나리오 3: 번역 비활성화
1. auto_translate: false 설정
2. 번역 없이 원문만 저장
3. translated_* 필드가 null로 유지

---

## 🔍 트러블슈팅

### DeepL API 오류

**증상:** DeepL API 호출 실패
```
DeepL 번역 실패: Authentication failed
```

**해결방법:**
1. API 키 확인: `.env` 파일의 `DEEPL_API_KEY` 값 확인
2. API 키 유효성: DeepL 계정에서 키 상태 확인
3. 네트워크: 인터넷 연결 확인

### 번역이 저장되지 않음

**증상:** auto_translated = false로 표시됨

**해결방법:**
1. 로그 확인: 백엔드 로그에서 번역 실패 원인 확인
2. 언어 코드: source_lang이 'ko' 또는 'ru'인지 확인
3. 텍스트 길이: 너무 긴 텍스트는 번역 실패 가능

### Redis 연결 오류

**증상:** Redis 캐시 연결 실패 경고

**해결방법:**
- Redis 없이도 정상 작동합니다 (캐시만 비활성화됨)
- Redis를 사용하려면 Redis 서버를 시작하세요:
  ```bash
  redis-server
  ```

---

## 📊 성능 최적화

### 캐싱 전략
- Redis를 사용하여 번역 결과를 24시간 캐싱
- 동일한 텍스트 재번역 방지
- API 호출 비용 절감

### Rate Limiting
- 사용자당 분당 20회 번역 요청 제한
- 남용 방지 및 API 비용 관리

### 비동기 처리
- 게시글 저장과 번역을 비동기로 처리
- 번역 실패 시에도 게시글은 정상 저장

---

## 📚 참고 자료

- [DeepL API 문서](https://www.deepl.com/docs-api)
- [FastAPI 문서](https://fastapi.tiangolo.com/)
- [Next.js 문서](https://nextjs.org/docs)

---

## 💡 추가 개선 사항

### 향후 추가 가능 기능
1. 댓글 자동 번역
2. 실시간 번역 미리보기
3. 번역 품질 평가 시스템
4. 다국어 지원 확대 (영어, 중국어 등)
5. 번역 히스토리 관리
6. 사용자 맞춤 번역 설정

---

## 🎉 완료!

이제 DeepL API를 사용한 자동 번역 기능이 준비되었습니다. 게시글을 작성하면 자동으로 한국어와 러시아어로 번역되어 양쪽 언어 사용자 모두 콘텐츠를 이용할 수 있습니다.
