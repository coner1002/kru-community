import logging
import sys
from loguru import logger
from app.core.config import settings

def setup_logger(name: str):
    """로거 설정"""
    logger.remove()  # 기본 핸들러 제거

    # 콘솔 로깅
    logger.add(
        sys.stdout,
        level="DEBUG" if settings.DEBUG else "INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True
    )

    # 파일 로깅 (프로덕션)
    if settings.ENVIRONMENT == "production":
        logger.add(
            "logs/app.log",
            rotation="10 MB",
            retention="30 days",
            level="INFO",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
        )

    return logger