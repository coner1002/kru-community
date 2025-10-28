from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"          # 관리자
    STAFF = "staff"          # 스탭
    PREMIUM = "premium"      # 특별회원
    USER = "user"            # 일반회원

class UserType(str, enum.Enum):
    ADMIN = "admin"          # 관리자 계정
    STAFF = "staff"          # 스탭 계정
    VIRTUAL = "virtual"      # 관리 가상회원 (분위기 조성용)
    REAL = "real"            # 실제 가입회원

class OAuthProvider(str, enum.Enum):
    EMAIL = "email"
    GOOGLE = "google"
    KAKAO = "kakao"
    NAVER = "naver"
    FACEBOOK = "facebook"
    VK = "vk"

class Language(str, enum.Enum):
    KO = "ko"
    RU = "ru"

class Ethnicity(str, enum.Enum):
    KOREAN = "korean"           # 한국인
    KOREAN_RUSSIAN = "korean_russian"  # 고려인(교포)
    RUSSIAN = "russian"         # 러시아인

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True)
    nickname = Column(String(50), nullable=False)  # 기본 닉네임 (레거시)
    nickname_ko = Column(String(50))  # 한글 닉네임
    nickname_ru = Column(String(50))  # 러시아어 닉네임
    password_hash = Column(String(255))  # NULL for OAuth users

    # OAuth 정보
    oauth_provider = Column(SQLEnum(OAuthProvider), default=OAuthProvider.EMAIL)
    oauth_uid = Column(String(255))

    # 프로필 정보
    preferred_lang = Column(SQLEnum(Language), default=Language.KO)
    region = Column(String(100))
    bio = Column(Text)
    profile_image = Column(String(500))

    # 권한 및 상태
    role = Column(SQLEnum(UserRole), default=UserRole.USER)
    user_type = Column(SQLEnum(UserType), default=UserType.REAL)  # 회원 유형 구분
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    email_verified_at = Column(DateTime)

    # 추가 정보
    phone = Column(String(20))
    phone_verified = Column(Boolean, default=False)
    notification_settings = Column(JSON, default=dict)

    # 페르소나 정보 (가상회원 전용)
    ethnicity = Column(SQLEnum(Ethnicity))  # 민족 구분
    persona_age = Column(Integer)  # 나이
    persona_gender = Column(String(10))  # 성별 (male/female)
    persona_occupation = Column(String(100))  # 직업
    persona_interests = Column(JSON)  # 관심사 리스트
    persona_activity_level = Column(String(20))  # 활동 수준 (high/medium/low)
    persona_posting_style = Column(String(50))  # 게시 스타일
    persona_korean_level = Column(String(20))  # 한국어 수준
    persona_russian_level = Column(String(20))  # 러시아어 수준

    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime)

    # 관계
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
    reports = relationship("Report", foreign_keys="[Report.reporter_id]", back_populates="reporter")
    handled_reports = relationship("Report", foreign_keys="[Report.handled_by]", back_populates="handler")
    bookmarks = relationship("Bookmark", back_populates="user", cascade="all, delete-orphan")

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    access_token_jti = Column(String(255), unique=True, index=True)
    refresh_token_jti = Column(String(255), unique=True, index=True)
    user_agent = Column(String(500))
    ip_address = Column(String(45))
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

class EmailVerification(Base):
    __tablename__ = "email_verifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    token = Column(String(255), unique=True, index=True)
    email = Column(String(255))
    expires_at = Column(DateTime)
    verified_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

class SMSVerification(Base):
    __tablename__ = "sms_verifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)  # 회원가입 전에는 NULL
    phone = Column(String(20), nullable=False)
    code = Column(String(6), nullable=False)  # 6자리 인증번호
    expires_at = Column(DateTime)
    verified_at = Column(DateTime)
    attempt_count = Column(Integer, default=0)  # 인증 시도 횟수
    created_at = Column(DateTime, default=datetime.utcnow)