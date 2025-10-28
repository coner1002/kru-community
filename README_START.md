# KRU Community - 로컬 개발 환경

## 📍 현재 위치
```
D:\Projects\kru-community
```

## 🚀 빠른 시작

### 옵션 1: 백엔드만 실행 (가장 간단)
```bash
START_HERE.bat
```
- 백엔드 API: http://localhost:8000
- API 문서: http://localhost:8000/docs
- 정적 HTML: http://localhost:8000

### 옵션 2: 백엔드 + Next.js 프론트엔드

**터미널 1 - 백엔드**:
```bash
START_HERE.bat
```

**터미널 2 - 프론트엔드**:
```bash
START_FRONTEND.bat
```
- 프론트엔드: http://localhost:3000
- 백엔드 API: http://localhost:8000

## 📁 프로젝트 구조

```
D:\Projects\kru-community\
├── backend/              # FastAPI 백엔드
│   ├── app/
│   │   ├── main.py      # 메인 애플리케이션
│   │   ├── api/         # API 라우터
│   │   ├── models/      # 데이터베이스 모델
│   │   └── core/        # 설정 및 보안
│   └── ...
├── frontend/            # Next.js 프론트엔드
│   ├── public/          # 정적 HTML 파일
│   ├── package.json
│   └── node_modules/    ✅ 설치 완료
├── START_HERE.bat       # 백엔드 실행
├── START_FRONTEND.bat   # 프론트엔드 실행
└── README_START.md      # 이 파일

```

## 🔧 개발 도구

### Python 패키지 설치
```bash
cd backend
pip install -r requirements.txt
```

### 데이터베이스 마이그레이션
```bash
cd backend
alembic upgrade head
```

### 샘플 데이터 생성
```bash
cd backend
python scripts/init_data.py
```

## 📚 주요 문서

- `AUTH_GUIDE.md` - 인증 시스템 가이드
- `DEPLOYMENT.md` - 배포 가이드
- `PROJECT_STRUCTURE.md` - 프로젝트 구조

## ⚡ 빠른 테스트

### API 상태 확인
```bash
curl http://localhost:8000/health
```

### 프론트엔드 빌드
```bash
cd frontend
npm run build
```

## 🎯 개발 팁

1. **백엔드 개발**: `backend/` 폴더에서 작업
2. **프론트엔드 개발**: `frontend/` 폴더에서 작업
3. **Hot Reload**: 두 서버 모두 자동 리로드 지원
4. **디버깅**: VS Code에서 디버그 구성 사용 가능

---
✅ 프로젝트가 D 드라이브로 성공적으로 이동되었습니다!
🚀 이제 Google Drive 동기화 충돌 없이 개발할 수 있습니다.
