# KRU Community 프로젝트 구조

## 📁 주요 디렉토리

- `backend/` - FastAPI 백엔드 서버
- `frontend/` - Next.js 프론트엔드 (또는 정적 HTML)
- `scripts/` - 유틸리티 스크립트
- `data/` - 데이터 파일
- `deploy/` - 배포 관련 파일
- `backup/` - 정리된 임시 파일들의 백업

## 🚀 실행 방법

### 백엔드 + 정적 프론트엔드 (권장)
```bash
QUICK_START.bat
```

### 백엔드만 실행
```bash
START_BACKEND.bat
```

## 📚 문서

- `AUTH_GUIDE.md` - 인증 시스템 가이드
- `DEPLOYMENT.md` - 배포 가이드
- `CLAUDE.md` - Claude AI 프롬프트

## 🗂️ 백업 정보

임시 수정 스크립트와 중복 배치 파일들은 `backup/` 폴더에 날짜별로 보관됩니다.
필요시 언제든 복구할 수 있습니다.

---
마지막 정리: 2025-10-17 14:02:59