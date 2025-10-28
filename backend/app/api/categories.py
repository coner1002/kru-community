from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models import Category

router = APIRouter()

@router.get("/")
async def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).filter(Category.is_active == True).order_by(Category.sort_order).all()
    return [
        {
            "id": cat.id,
            "slug": cat.slug,
            "name_ko": cat.name_ko,
            "name_ru": cat.name_ru,
            "description_ko": cat.description_ko,
            "description_ru": cat.description_ru,
            "icon": cat.icon,
            "parent_id": cat.parent_id,
            "sort_order": cat.sort_order,
            "is_active": cat.is_active,
            "is_group": cat.is_group if cat.is_group is not None else False,
            "layout_type": cat.layout_type.value if hasattr(cat.layout_type, 'value') else str(cat.layout_type),
            "permission": cat.permission.value if hasattr(cat.permission, 'value') else str(cat.permission)
        }
        for cat in categories
    ]