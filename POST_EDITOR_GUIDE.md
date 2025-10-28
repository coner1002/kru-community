# 게시글 에디터 사용 가이드

DeepL 자동 번역이 포함된 Rich Text Editor 사용 방법입니다.

## 📋 개선 사항

### ✅ 완료된 기능

1. **Rich Text Editor (Quill) 적용**
   - ✓ 진짜 볼드, 이탤릭, 밑줄 적용 (마크다운 방식이 아님)
   - ✓ 글꼴, 크기, 색상 변경 가능
   - ✓ 이미지 첨부 (파일 선택 가능)
   - ✓ 동영상 첨부 (파일 선택 가능)
   - ✓ HTML 형식으로 저장

2. **제목 입력 방식 개선**
   - ✓ 단일 언어로만 입력 (한국어 또는 러시아어)
   - ✓ 언어 자동 감지
   - ✓ 등록 시 자동으로 반대 언어로 번역

3. **데이터베이스 초기화**
   - ✓ 테스트 사용자 생성
   - ✓ 카테고리 5개 생성

---

## 🚀 설치 및 실행

### 1. 프론트엔드 패키지 설치

```bash
cd frontend
npm install
```

새로 추가된 패키지:
- `react-quill@2.0.0` - React용 Quill 에디터
- `quill@1.3.7` - Quill 에디터 코어
- `@types/react-quill@1.3.10` - TypeScript 타입 정의

### 2. 백엔드 데이터베이스 초기화

```bash
cd backend
python scripts/init_data.py
```

실행 결과:
```
============================================================
KRU Community - 데이터베이스 초기화
============================================================

✓ 테이블 생성 완료
✓ 테스트 사용자 생성: testuser (ID: 1)
✓ 5개 카테고리 생성 완료

테스트 계정 정보:
  이메일: test@example.com
  비밀번호: test1234
  User ID: 1
```

### 3. 서버 시작

```bash
# 백엔드 (터미널 1)
cd backend
uvicorn app.main:app --reload --port 8000

# 프론트엔드 (터미널 2)
cd frontend
npm run dev
```

---

## 📝 Rich Text Editor 기능

### 텍스트 서식

| 기능 | 설명 | 결과 |
|-----|------|------|
| **볼드** | 텍스트 선택 후 Bold 버튼 클릭 | `<strong>텍스트</strong>` |
| *이탤릭* | 텍스트 선택 후 Italic 버튼 클릭 | `<em>텍스트</em>` |
| <u>밑줄</u> | 텍스트 선택 후 Underline 버튼 클릭 | `<u>텍스트</u>` |
| ~~취소선~~ | 텍스트 선택 후 Strike 버튼 클릭 | `<s>텍스트</s>` |

### 글꼴 및 크기

- **Header**: H1 ~ H6 헤더 설정
- **Font**: 다양한 글꼴 선택
- **Size**: 글자 크기 변경 (Small, Normal, Large, Huge)

### 색상

- **텍스트 색상**: 글자 색 변경
- **배경색**: 글자 배경색 변경

### 정렬 및 목록

- **정렬**: 왼쪽, 가운데, 오른쪽, 양쪽 정렬
- **번호 목록**: 1, 2, 3...
- **글머리 기호**: •, ◦, ▪

### 미디어 첨부

#### 이미지 첨부
1. 툴바에서 📷 이미지 버튼 클릭
2. 파일 탐색기가 열림
3. 이미지 파일 선택 (jpg, png, gif 등)
4. 이미지가 에디터에 삽입됨

#### 동영상 첨부
1. 툴바에서 🎥 동영상 버튼 클릭
2. 파일 탐색기가 열림
3. 동영상 파일 선택 (mp4, webm 등)
4. 동영상이 에디터에 삽입됨

---

## ✏️ 게시글 작성 방법

### 1. 기본 작성 흐름

```typescript
import PostEditorV2 from '@/components/post/post-editor-v2';

<PostEditorV2
  categoryId={1}
  onSuccess={(postId) => {
    console.log('게시글 작성 완료:', postId);
    // 게시글 목록 페이지로 이동
  }}
  onCancel={() => {
    // 취소 처리
  }}
/>
```

### 2. 언어 자동 감지

에디터는 입력한 텍스트를 분석하여 자동으로 언어를 감지합니다:

- **한글 감지**: 한글 문자(ㄱ-ㅎ, ㅏ-ㅣ, 가-힣) 포함 시 → 🇰🇷 한국어
- **키릴 문자 감지**: 러시아어 문자(А-Я, а-я) 포함 시 → 🇷🇺 러시아어

### 3. 제목 입력

```
┌─────────────────────────────────────┐
│ 감지된 언어: 🇰🇷 한국어             │
│ ☑ 러시아어로 자동 번역              │
└─────────────────────────────────────┘

제목 (한국어) *
┌─────────────────────────────────────┐
│ 안녕하세요                          │
└─────────────────────────────────────┘

🇷🇺 러시아어 번역: Здравствуйте
```

### 4. 본문 작성 (Rich Text)

```
내용 *
┌─────────────────────────────────────┐
│ [B] [I] [U] [S] [색] [크기] [정렬]  │ ← 툴바
├─────────────────────────────────────┤
│                                     │
│ 여기에 내용을 작성하세요...         │
│                                     │
│ • 볼드, 이탤릭, 밑줄 사용 가능      │
│ • 이미지/동영상 첨부 가능           │
│ • HTML 형식으로 저장됨              │
│                                     │
└─────────────────────────────────────┘
```

### 5. 게시글 등록

```
[ 게시글 등록 ]  [ 취소 ]
```

등록 시:
1. 제목 + 내용이 DeepL API로 번역됨
2. 원문 + 번역본 모두 저장됨
3. 게시글 목록에 표시됨

---

## 🔍 실제 사용 예시

### 예시 1: 한국어 게시글 작성

**입력:**
```
제목: 안녕하세요
내용: <p><strong>한국-러시아 커뮤니티</strong>에 오신 것을 환영합니다.</p>
```

**저장 결과:**
```javascript
{
  title: "안녕하세요",
  content: "<p><strong>한국-러시아 커뮤니티</strong>에 오신 것을 환영합니다.</p>",
  source_lang: "ko",
  translated_title_ko: "안녕하세요",
  translated_title_ru: "Здравствуйте",
  translated_content_ko: "<p><strong>한국-러시아 커뮤니티</strong>에 오신 것을 환영합니다.</p>",
  translated_content_ru: "<p><strong>Корейско-российское сообщество</strong> приветствует вас.</p>",
  auto_translated: true
}
```

### 예시 2: 러시아어 게시글 작성

**입력:**
```
제목: Новости
내용: <p><u>Важная информация</u> для всех участников.</p>
```

**저장 결과:**
```javascript
{
  title: "Новости",
  content: "<p><u>Важная информация</u> для всех участников.</p>",
  source_lang: "ru",
  translated_title_ru: "Новости",
  translated_title_ko: "뉴스",
  translated_content_ru: "<p><u>Важная информация</u> для всех участников.</p>",
  translated_content_ko: "<p><u>중요한 정보</u> 모든 회원을 위한.</p>",
  auto_translated: true
}
```

---

## 🎨 HTML 출력 예시

Rich Text Editor는 다음과 같은 HTML을 생성합니다:

### 서식 적용
```html
<p><strong>볼드 텍스트</strong></p>
<p><em>이탤릭 텍스트</em></p>
<p><u>밑줄 텍스트</u></p>
<p><s>취소선 텍스트</s></p>
```

### 색상 및 배경
```html
<p><span style="color: rgb(255, 0, 0);">빨간색 텍스트</span></p>
<p><span style="background-color: rgb(255, 255, 0);">노란 배경</span></p>
```

### 헤더 및 크기
```html
<h1>대제목</h1>
<h2>중제목</h2>
<p class="ql-size-large">큰 텍스트</p>
```

### 목록
```html
<ol>
  <li>첫 번째 항목</li>
  <li>두 번째 항목</li>
</ol>

<ul>
  <li>글머리 기호 1</li>
  <li>글머리 기호 2</li>
</ul>
```

### 이미지
```html
<p><img src="data:image/png;base64,iVBORw0KG..." alt="이미지"></p>
```

---

## 📊 API 호출 흐름

### 게시글 작성 요청

```
클라이언트                    백엔드                    DeepL API
    │                           │                           │
    │  POST /api/posts/         │                           │
    ├─────────────────────────►│                           │
    │  {                        │                           │
    │    title: "안녕하세요",   │                           │
    │    content: "<p>...</p>", │                           │
    │    source_lang: "ko",     │                           │
    │    auto_translate: true   │                           │
    │  }                        │                           │
    │                           │  POST /translate          │
    │                           ├─────────────────────────►│
    │                           │  title + content          │
    │                           │                           │
    │                           │  ◄────────────────────────┤
    │                           │  { translated_text: "Здравствуйте" }
    │                           │                           │
    │  ◄─────────────────────────┤                           │
    │  {                        │                           │
    │    id: 1,                 │                           │
    │    translated_title_ru: "Здравствуйте",              │
    │    translated_content_ru: "<p>...</p>",              │
    │    ...                    │                           │
    │  }                        │                           │
```

---

## 🐛 트러블슈팅

### 1. 게시글이 목록에 나타나지 않음

**원인**: 카테고리나 사용자가 없음

**해결**:
```bash
cd backend
python scripts/init_data.py
```

### 2. Rich Text Editor가 로드되지 않음

**원인**: 패키지 미설치

**해결**:
```bash
cd frontend
npm install
```

### 3. 이미지 업로드 안됨

**현재 상태**: Base64 인코딩으로 저장 (개발 모드)

**프로덕션 개선 방법**:
- S3나 CDN을 사용한 이미지 업로드 서버 구축
- `onImageUpload` prop에 업로드 핸들러 전달

```typescript
<RichTextEditor
  value={content}
  onChange={setContent}
  onImageUpload={async (file) => {
    // S3 업로드 로직
    const url = await uploadToS3(file);
    return url;
  }}
/>
```

### 4. 동영상이 재생되지 않음

**원인**: 파일 크기 또는 형식 문제

**권장 사항**:
- 동영상은 YouTube 또는 Vimeo 링크 사용
- 서버에 파일 업로드 후 URL 삽입

---

## 📚 참고 자료

- [Quill 공식 문서](https://quilljs.com/)
- [React Quill GitHub](https://github.com/zenoamaro/react-quill)
- [DeepL API 문서](https://www.deepl.com/docs-api)

---

## ✅ 체크리스트

설치 및 설정:
- [ ] `npm install` 실행
- [ ] `python scripts/init_data.py` 실행
- [ ] 백엔드 서버 실행 (포트 8000)
- [ ] 프론트엔드 서버 실행 (포트 3000)

기능 테스트:
- [ ] 한국어 게시글 작성 → 러시아어로 번역 확인
- [ ] 러시아어 게시글 작성 → 한국어로 번역 확인
- [ ] 볼드, 이탤릭, 밑줄 적용 확인
- [ ] 이미지 첨부 확인
- [ ] 게시글 목록에 표시 확인

---

## 🎉 완료!

이제 개선된 Rich Text Editor로 게시글을 작성할 수 있습니다!

**주요 개선사항**:
✅ 진짜 볼드/이탤릭/밑줄 (마크다운 ❌)
✅ 글꼴, 크기, 색상 변경 가능
✅ 이미지/동영상 첨부 (파일 선택)
✅ 제목 단일 입력 + 자동 번역
✅ HTML 형식 저장
