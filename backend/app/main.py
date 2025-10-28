from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging
from app.core.config import settings
from app.db.database import engine, Base
from app.api import auth, users, posts, comments, categories, partners, admin, translation, data, verification
from app.core.middleware import LoggingMiddleware, RateLimitMiddleware
from app.utils.logger import setup_logger

# 모든 모델 import (테이블 생성을 위해 필요)
from app.models import user, post, partner

# 로거 설정
logger = setup_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 시작 시
    logger.info("애플리케이션 시작")
    # 데이터베이스 테이블 생성 (선택적)
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("데이터베이스 연결 성공")
    except Exception as e:
        logger.warning(f"데이터베이스 연결 실패 (파일 기반 모드로 동작): {e}")
    yield
    # 종료 시
    logger.info("애플리케이션 종료")

app = FastAPI(
    title="KRU Community API",
    description="한국-러시아 커뮤니티 플랫폼 API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 미들웨어
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 시에는 모든 origin 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 커스텀 미들웨어
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware)

# 라우터 등록
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(categories.router, prefix="/api/categories", tags=["Categories"])
app.include_router(posts.router, prefix="/api/posts", tags=["Posts"])
app.include_router(comments.router, prefix="/api/comments", tags=["Comments"])
app.include_router(partners.router, prefix="/api/partners", tags=["Partners"])
app.include_router(translation.router, prefix="/api/translate", tags=["Translation"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(data.router, prefix="/api/data", tags=["Data"])
app.include_router(verification.router, prefix="/api/verification", tags=["Verification"])
# app.include_router(contact.router, prefix="/api/contact", tags=["Contact"])  # Disabled - will implement later

# 정적 파일 서빙 (프론트엔드)
import os
import pathlib

# 절대 경로로 프론트엔드 디렉토리 설정
current_dir = pathlib.Path(__file__).parent.parent.parent  # backend/app/main.py에서 3단계 올라가기
frontend_path = current_dir / "frontend" / "public"

print(f"Frontend path: {frontend_path}")
print(f"Path exists: {frontend_path.exists()}")

if frontend_path.exists():
    from fastapi.responses import FileResponse

    # 정적 파일 서빙
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

    # 루트 경로에서 index.html 서빙
    @app.get("/")
    async def serve_frontend():
        return FileResponse(str(frontend_path / "index.html"))

@app.get("/api")
async def root():
    return {
        "message": "KRU Community API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if frontend_path.exists():
    # HTML 파일들을 직접 서빙하는 catch-all 라우트 (API 경로는 제외)
    @app.get("/{file_path:path}")
    async def serve_html(file_path: str):
        # API 경로는 이 핸들러로 오지 않도록 (이미 위에서 처리됨)
        if file_path.startswith('api/'):
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Not Found")

        # HTML 파일인 경우
        if file_path.endswith('.html'):
            file = frontend_path / file_path
            if file.exists():
                return FileResponse(str(file))
        # 정적 파일 (css, js, images 등)
        else:
            file = frontend_path / file_path
            if file.exists():
                return FileResponse(str(file))
        # 파일이 없으면 404
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Not Found")