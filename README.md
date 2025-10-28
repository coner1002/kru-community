# KRU Community (Korea-Russia Community)

## 프로젝트 개요
한국 입국 러시아인/교포를 위한 커뮤니티 및 정보 공유 플랫폼

### 핵심 기능
- 다국어 지원 (한국어/러시아어)
- 자동 번역 시스템
- 소셜 로그인 (Google, Kakao, VK)
- 커뮤니티 게시판
- 비즈니스 디렉터리
- 관리자 대시보드

## 기술 스택

### Frontend
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- React Query
- next-intl (i18n)

### Backend
- FastAPI
- PostgreSQL
- Redis
- SQLAlchemy
- Alembic (migrations)

### Infrastructure
- Docker & Docker Compose
- Nginx
- AWS S3 (파일 스토리지)
- Google Cloud Translation API

## 프로젝트 구조
```
kru-community/
├── backend/              # FastAPI 백엔드
│   ├── app/
│   ├── migrations/
│   └── tests/
├── frontend/            # Next.js 프론트엔드
│   ├── app/
│   ├── components/
│   └── locales/
├── docker/              # Docker 설정
└── docs/               # 문서
```

## 시작하기

### 개발 환경 설정

1. 환경 변수 설정
```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local
```

2. Docker Compose로 실행
```bash
docker-compose up -d
```

3. 데이터베이스 마이그레이션
```bash
cd backend
alembic upgrade head
```

### 로컬 개발

Backend:
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

## 라이센스
MIT License