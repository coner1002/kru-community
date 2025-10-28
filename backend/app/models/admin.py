from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.database import Base

class ReportTargetType(str, enum.Enum):
    POST = "post"
    COMMENT = "comment"
    USER = "user"
    PARTNER = "partner"
    REVIEW = "review"

class ReportReason(str, enum.Enum):
    SPAM = "spam"
    INAPPROPRIATE = "inappropriate"
    HARASSMENT = "harassment"
    FALSE_INFO = "false_info"
    COPYRIGHT = "copyright"
    OTHER = "other"

class ReportStatus(str, enum.Enum):
    PENDING = "pending"
    REVIEWING = "reviewing"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    target_type = Column(SQLEnum(ReportTargetType), nullable=False)
    target_id = Column(Integer, nullable=False)
    reporter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reason = Column(SQLEnum(ReportReason), nullable=False)
    description = Column(Text)
    status = Column(SQLEnum(ReportStatus), default=ReportStatus.PENDING)
    handled_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    resolution_note = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime)

    # 관계
    reporter = relationship("User", foreign_keys=[reporter_id], back_populates="reports")
    handler = relationship("User", foreign_keys=[handled_by], back_populates="handled_reports")

class Banner(Base):
    __tablename__ = "banners"

    id = Column(Integer, primary_key=True, index=True)
    position = Column(String(50), nullable=False)  # top, sidebar, infeed
    title = Column(String(255))
    image_url = Column(String(500), nullable=False)
    link_url = Column(String(500))
    advertiser_name = Column(String(255))
    advertiser_contact = Column(String(255))
    click_count = Column(Integer, default=0)
    impression_count = Column(Integer, default=0)
    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(Integer)
    actor_email = Column(String(255))
    action = Column(String(100), nullable=False)
    target_type = Column(String(50))
    target_id = Column(Integer)
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    meta = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class SystemNotice(Base):
    __tablename__ = "system_notices"

    id = Column(Integer, primary_key=True, index=True)
    title_ko = Column(String(255), nullable=False)
    title_ru = Column(String(255))
    content_ko = Column(Text, nullable=False)
    content_ru = Column(Text)
    type = Column(String(50), default="info")  # info, warning, error, success
    is_important = Column(Boolean, default=False)
    show_from = Column(DateTime)
    show_until = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class BlockedKeyword(Base):
    __tablename__ = "blocked_keywords"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String(255), nullable=False, unique=True)
    reason = Column(String(500))
    is_regex = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SystemSettings(Base):
    __tablename__ = "system_settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), nullable=False, unique=True, index=True)
    value = Column(Text)
    description = Column(String(500))
    category = Column(String(50), default="general")  # general, translation, email, oauth, etc.
    is_encrypted = Column(Boolean, default=False)
    updated_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계
    updater = relationship("User", foreign_keys=[updated_by])