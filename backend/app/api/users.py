from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.dependencies import get_current_user
from app.models import User

router = APIRouter()

@router.get("/me")
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "nickname": current_user.nickname,
        "preferred_lang": current_user.preferred_lang,
        "role": current_user.role.name if hasattr(current_user.role, 'name') else str(current_user.role),
        "is_verified": current_user.is_verified
    }