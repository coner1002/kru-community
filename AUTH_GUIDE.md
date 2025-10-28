# 인증 및 권한 시스템 가이드

로그인하지 않으면 공지사항 외 게시글을 볼 수 없도록 구현된 인증 시스템 가이드입니다.

## 📋 권한 정책

### 1. 비로그인 사용자
- ✅ 공지사항 조회 가능
- ✅ 공지사항 추천/공유 가능
- ❌ 공지사항 외 게시판 조회 불가
- ❌ 게시글 작성 불가
- ❌ 댓글 작성 불가

### 2. 일반 사용자 (로그인)
- ✅ 모든 게시판 조회 가능
- ✅ 게시글 작성 가능 (공지사항 제외)
- ✅ 자신의 게시글 수정/삭제 가능
- ✅ 댓글 작성 가능 (공지사항 제외)
- ✅ 추천/공유/신고 가능
- ❌ 공지사항 작성 불가

### 3. 관리자/모더레이터
- ✅ 모든 권한 보유
- ✅ 공지사항 작성/수정/삭제 가능
- ✅ 모든 게시글 수정/삭제 가능
- ✅ 공지사항에 댓글 작성 가능

---

## 🔐 백엔드 인증 구현

### API 엔드포인트별 권한

#### 1. 게시글 목록 조회
```
GET /api/posts/?category_id={id}
```

**권한:**
- 비로그인: 공지사항(notice) 카테고리만 조회 가능
- 로그인: 모든 카테고리 조회 가능

**응답:**
```python
# 비로그인 + 공지사항 아닌 카테고리 요청 시
{
  "detail": "로그인이 필요합니다"
}  # 401 Unauthorized
```

#### 2. 게시글 상세 조회
```
GET /api/posts/{post_id}
```

**권한:**
- 비로그인: 공지사항만 조회 가능
- 로그인: 모든 게시글 조회 가능

#### 3. 게시글 작성
```
POST /api/posts/
Authorization: Bearer {access_token}  (필수)
```

**권한:**
- 비로그인: 불가 (401 Unauthorized)
- 일반 사용자: 공지사항 외 작성 가능
- 관리자: 모든 카테고리 작성 가능

**응답:**
```python
# 일반 사용자가 공지사항 작성 시도 시
{
  "detail": "공지사항은 관리자만 작성할 수 있습니다"
}  # 403 Forbidden
```

#### 4. 게시글 수정
```
PUT /api/posts/{post_id}
Authorization: Bearer {access_token}  (필수)
```

**권한:**
- 작성자 또는 관리자만 수정 가능
- 공지사항: 관리자만 수정 가능

#### 5. 게시글 삭제
```
DELETE /api/posts/{post_id}
Authorization: Bearer {access_token}  (필수)
```

**권한:**
- 작성자 또는 관리자만 삭제 가능
- 공지사항: 관리자만 삭제 가능

---

## 🔑 로그인 시스템

### 1. 로그인 API
```
POST /api/auth/email/login
Content-Type: application/json

{
  "email": "test@example.com",
  "password": "test1234"
}
```

**응답:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### 2. 인증 토큰 사용

모든 인증이 필요한 API 요청 시 헤더에 포함:
```
Authorization: Bearer {access_token}
```

### 3. 테스트 계정

데이터베이스 초기화 시 생성된 테스트 계정:
```
이메일: test@example.com
비밀번호: test1234
역할: 일반 사용자 (user)
```

---

## 💻 프론트엔드 구현

### 1. 인증 상태 관리 (Zustand)

**파일:** `frontend/lib/stores/auth-store.ts`

```typescript
import { useAuthStore } from '@/lib/stores/auth-store';

// 컴포넌트에서 사용
const { user, accessToken, isAuthenticated, setAuth, clearAuth } = useAuthStore();

// 로그인
setAuth(user, accessToken, refreshToken);

// 로그아웃
clearAuth();

// 로그인 여부 확인
if (isAuthenticated) {
  // 로그인 상태
}
```

### 2. 로그인 모달 컴포넌트

**파일:** `frontend/components/auth/login-modal.tsx`

```typescript
import LoginModal from '@/components/auth/login-modal';

<LoginModal
  isOpen={isLoginModalOpen}
  onClose={() => setIsLoginModalOpen(false)}
  onSuccess={() => {
    // 로그인 성공 후 처리
    console.log('로그인 성공!');
  }}
/>
```

### 3. 게시글 조회 시 권한 체크

**파일:** `frontend/components/post/post-view.tsx`

```typescript
<PostView
  post={post}
  userLanguage="ko"
  currentUser={user}  // 인증 상태 전달
  categorySlug="notice"  // 카테고리 정보 전달
/>
```

**권한 분기:**
- 공지사항: 추천, 공유만 표시
- 일반 게시판: 추천, 댓글, 공유, 신고 표시
- 작성자/관리자: 수정, 삭제 버튼 추가 표시

---

## 🧪 테스트

### 1. 비로그인 상태 테스트

```bash
# 공지사항 조회 (성공)
curl http://localhost:8000/api/posts/?category_id=1

# 자유게시판 조회 (실패 - 401)
curl http://localhost:8000/api/posts/?category_id=2
```

**예상 결과:**
```json
{
  "detail": "로그인이 필요합니다"
}
```

### 2. 로그인 후 테스트

```bash
# 로그인
curl -X POST http://localhost:8000/api/auth/email/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test1234"}'

# 응답에서 access_token 복사

# 자유게시판 조회 (성공)
curl http://localhost:8000/api/posts/?category_id=2 \
  -H "Authorization: Bearer {access_token}"
```

### 3. 공지사항 작성 권한 테스트

```bash
# 일반 사용자로 공지사항 작성 시도 (실패 - 403)
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "테스트 공지",
    "content": "내용",
    "category_id": 1,
    "source_lang": "ko",
    "auto_translate": true
  }'
```

**예상 결과:**
```json
{
  "detail": "공지사항은 관리자만 작성할 수 있습니다"
}
```

---

## 📊 권한 매트릭스

| 기능 | 비로그인 | 일반 사용자 | 작성자 | 관리자 |
|-----|---------|-----------|-------|--------|
| 공지사항 조회 | ✅ | ✅ | ✅ | ✅ |
| 공지사항 작성 | ❌ | ❌ | ❌ | ✅ |
| 공지사항 수정 | ❌ | ❌ | ❌ | ✅ |
| 공지사항 삭제 | ❌ | ❌ | ❌ | ✅ |
| 공지사항 댓글 | ❌ | ❌ | ❌ | ✅ |
| 공지사항 추천/공유 | ✅ | ✅ | ✅ | ✅ |
| 일반 게시판 조회 | ❌ | ✅ | ✅ | ✅ |
| 일반 게시글 작성 | ❌ | ✅ | ✅ | ✅ |
| 일반 게시글 수정 | ❌ | ❌ | ✅ | ✅ |
| 일반 게시글 삭제 | ❌ | ❌ | ✅ | ✅ |
| 댓글 작성 | ❌ | ✅ | ✅ | ✅ |
| 신고 | ❌ | ✅ | ✅ | ✅ |

---

## 🔧 설정 파일

### Backend Dependencies

**파일:** `backend/app/core/dependencies.py`

주요 함수:
- `get_current_user()`: 인증 필수, 401 반환
- `get_optional_current_user()`: 인증 선택적, None 반환
- `require_admin()`: 관리자 권한 필수

### Security Configuration

**파일:** `backend/app/core/security.py`

- JWT 토큰 생성 및 검증
- 비밀번호 해싱
- Access Token 만료: 30분
- Refresh Token 만료: 7일

---

## 🚨 에러 코드

| 코드 | 설명 | 응답 메시지 |
|-----|------|----------|
| 401 | 인증 필요 | "로그인이 필요합니다" |
| 403 | 권한 부족 | "권한이 없습니다" |
| 403 | 공지사항 권한 | "공지사항은 관리자만 작성/수정/삭제할 수 있습니다" |
| 404 | 리소스 없음 | "게시글을 찾을 수 없습니다" |

---

## 📝 체크리스트

### 백엔드 설정
- [x] 인증 미들웨어 구현
- [x] 권한 검증 로직 추가
- [x] 공지사항 특수 권한 처리
- [x] API 엔드포인트별 인증 적용

### 프론트엔드 설정
- [x] 인증 상태 관리 (Zustand)
- [x] 로그인 모달 컴포넌트
- [x] API 클라이언트 인증 헤더 처리
- [x] 게시글 보기 권한 분기 UI

### 테스트
- [ ] 비로그인 상태로 공지사항 조회
- [ ] 비로그인 상태로 일반 게시판 조회 차단 확인
- [ ] 로그인 후 모든 게시판 조회 가능 확인
- [ ] 일반 사용자의 공지사항 작성 차단 확인
- [ ] 작성자의 게시글 수정/삭제 가능 확인

---

## 🎉 완료!

인증 및 권한 시스템이 구현되었습니다!

**주요 기능:**
- ✅ 공지사항 외 로그인 필수
- ✅ 공지사항 관리자 전용 작성/수정/삭제
- ✅ 공지사항 댓글 차단
- ✅ 권한별 UI 분기 처리
