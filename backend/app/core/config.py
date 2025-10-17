from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache

class Settings(BaseSettings):
    # 기본 설정
    PROJECT_NAME: str = "KRU Community"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"

    # 데이터베이스
    DATABASE_URL: str
    REDIS_URL: str

    # 보안
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # OAuth
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    KAKAO_CLIENT_ID: str = ""
    KAKAO_CLIENT_SECRET: str = ""
    NAVER_CLIENT_ID: str = ""
    NAVER_CLIENT_SECRET: str = ""
    FACEBOOK_APP_ID: str = ""
    FACEBOOK_APP_SECRET: str = ""
    VK_APP_ID: str = ""
    VK_APP_SECRET: str = ""
    VK_API_VERSION: str = "5.131"

    # 번역
    GOOGLE_CLOUD_PROJECT_ID: str = ""
    GOOGLE_APPLICATION_CREDENTIALS: str = ""
    DEEPL_API_KEY: str = ""
    TRANSLATION_PROVIDER: str = "deepl"

    # AWS S3
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_S3_BUCKET_NAME: str = "kru-community"
    AWS_S3_REGION: str = "ap-northeast-2"

    # 이메일
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""

    # Sentry
    SENTRY_DSN: str = ""

    # 환경
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # 파일 업로드
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_IMAGE_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "gif", "webp"]

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    TRANSLATION_RATE_LIMIT_PER_MINUTE: int = 20

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # 추가 환경 변수 무시

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()