# 개발 환경 설정 가이드

## 빠른 개발을 위한 권장 방법

### 방법 1: 로컬 개발 (가장 빠름, 권장)

**백엔드 (Python)**:
```bash
cd backend
pip install -r requirements.txt
export DATABASE_URL="postgresql://kru_user:password@localhost:5432/kru_community"
export REDIS_URL="redis://localhost:6379/0"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**프론트엔드 (HTML/JS)**:
- `frontend/public/*.html` 파일을 직접 수정
- 브라우저에서 `http://localhost/board-free.html` 열기
- 수정 후 브라우저 새로고침만 하면 즉시 반영됨

**데이터베이스 (Docker만 사용)**:
```bash
docker-compose up -d postgres redis
```

### 방법 2: Docker 개발 환경 (현재)

```bash
docker-compose -f docker-compose.dev.yml up -d
```

**장점**: 전체 환경 격리
**단점**: 파일 수정 시 반영이 느릴 수 있음

### 개발 팁

1. **백엔드 수정 시**:
   - 로컬에서 Python 직접 실행 (--reload 옵션으로 자동 재시작)
   - 또는 Docker 컨테이너 재시작: `docker-compose restart backend`

2. **프론트엔드 수정 시**:
   - 파일 수정 후 브라우저 강력 새로고침 (Ctrl+Shift+R)
   - 개발자 도구(F12) → Network 탭 → "Disable cache" 체크

3. **데이터베이스 초기화**:
   ```bash
   docker-compose exec backend python init_sample_data.py
   ```

### 현재 문제 해결

**"로그인이 필요합니다" 에러**:
- backend/app/api/posts.py의 get_posts 함수에서 로그인 체크 제거 필요
- 파일 수정 후 백엔드 재시작

**브라우저 캐시 문제**:
- Ctrl+Shift+R (강력 새로고침)
- 또는 시크릿 모드로 테스트
