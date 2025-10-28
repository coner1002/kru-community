from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.database import get_db
from app.core.dependencies import get_current_user
from app.services.translation import translation_service
from app.models import User

router = APIRouter()

class TranslateRequest(BaseModel):
    text: str
    target_lang: str
    source_lang: str = None

@router.post("/")
async def translate_text(
    request: TranslateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Rate limiting 체크
    if not await translation_service.check_rate_limit(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="번역 요청 한도를 초과했습니다. 잠시 후 다시 시도해주세요."
        )

    result = await translation_service.translate_text(
        request.text,
        request.target_lang,
        request.source_lang
    )

    return result