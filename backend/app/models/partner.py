from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, JSON, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
# from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime
import enum
from app.db.database import Base

class PartnerCategory(str, enum.Enum):
    REAL_ESTATE = "real_estate"  # 부동산
    HOSPITAL = "hospital"  # 병원
    ACADEMY = "academy"  # 학원
    TRANSLATION = "translation"  # 통역/번역
    LAW = "law"  # 법률
    RESTAURANT = "restaurant"  # 레스토랑
    SHOPPING = "shopping"  # 쇼핑
    BEAUTY = "beauty"  # 미용
    OTHER = "other"  # 기타

class Partner(Base):
    __tablename__ = "partners"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)  # 관리 유저 (옵션)

    # 기본 정보
    name_ko = Column(String(255), nullable=False)
    name_ru = Column(String(255))
    category = Column(SQLEnum(PartnerCategory), nullable=False)
    description_ko = Column(Text)
    description_ru = Column(Text)

    # 연락처
    phone = Column(String(50))
    kakao_id = Column(String(100))
    telegram = Column(String(100))
    whatsapp = Column(String(50))
    email = Column(String(255))
    website = Column(String(500))

    # 위치 정보
    address_ko = Column(String(500))
    address_ru = Column(String(500))
    latitude = Column(Float)
    longitude = Column(Float)
    region = Column(String(100))

    # 운영 정보
    business_hours = Column(JSON)  # {"mon": "09:00-18:00", ...}
    languages = Column(JSON, default=list)  # ["ko", "ru", "en"]
    services = Column(JSON, default=list)

    # 이미지
    logo = Column(String(500))
    images = Column(JSON, default=list)

    # 평가 및 리뷰
    rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)

    # 광고 및 노출
    is_premium = Column(Boolean, default=False)
    premium_until = Column(DateTime)
    priority_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    # 통계
    view_count = Column(Integer, default=0)
    contact_count = Column(Integer, default=0)

    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계
    reviews = relationship("PartnerReview", back_populates="partner", cascade="all, delete-orphan")

class PartnerReview(Base):
    __tablename__ = "partner_reviews"

    id = Column(Integer, primary_key=True, index=True)
    partner_id = Column(Integer, ForeignKey("partners.id"), nullable=False)
    user_id = Column(Integer, nullable=False)

    # 리뷰 내용
    rating = Column(Integer, nullable=False)  # 1-5
    title = Column(String(255))
    content = Column(Text)
    source_lang = Column(String(2), default="ko")
    translated_content_ko = Column(Text)
    translated_content_ru = Column(Text)

    # 이미지
    images = Column(JSON, default=list)

    # 상태
    is_verified_purchase = Column(Boolean, default=False)
    is_hidden = Column(Boolean, default=False)

    # 통계
    helpful_count = Column(Integer, default=0)
    report_count = Column(Integer, default=0)

    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계
    partner = relationship("Partner", back_populates="reviews")