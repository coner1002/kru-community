from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db

router = APIRouter()

@router.get("/")
async def get_comments(db: Session = Depends(get_db)):
    return {"message": "Comments endpoint - coming soon"}