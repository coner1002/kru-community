from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db

router = APIRouter()

@router.get("/")
async def get_partners(db: Session = Depends(get_db)):
    return {"message": "Partners endpoint - coming soon"}