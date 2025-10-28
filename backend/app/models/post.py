from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
# from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime
import enum
from app.db.database import Base

class PostStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    HIDDEN = "hidden"
    DELETED = "deleted"

class CategoryLayoutType(str, enum.Enum):
    LIST = "list"           # 기본 리스트형
    GALLERY = "gallery"     # 갤러리/사진 정렬
    CARD = "card"          # 카드형 정렬
    GRID = "grid"          # 그리드형
    FORM = "form"          # 문의폼형

class CategoryPermission(str, enum.Enum):
    PUBLIC = "public"           # 누구나 읽기/쓰기 가능
    READ_ALL = "read_all"       # 누구나 읽기, 로그인 후 쓰기
    LOGIN_ONLY = "login_only"   # 로그인 후 읽기/쓰기
    ADMIN_ONLY = "admin_only"   # 관리자만 읽기/쓰기

# 등급별 권한 정의
class PermissionLevel(str, enum.Enum):
    ALL = "all"           # 모두 (비로그인 포함)
    USER = "user"         # 일반회원 이상
    PREMIUM = "premium"   # 특별회원 이상
    STAFF = "staff"       # 스탭 이상
    ADMIN = "admin"       # 관리자만

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    slug = Column(String(100), unique=True, index=True)
    name_ko = Column(String(100), nullable=False)
    name_ru = Column(String(100), nullable=False)
    description_ko = Column(Text)
    description_ru = Column(Text)
    icon = Column(String(50))
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

    # 레이아웃 타입
    layout_type = Column(SQLEnum(CategoryLayoutType), default=CategoryLayoutType.LIST)

    # 권한 설정 (deprecated - 하위 호환성)
    permission = Column(SQLEnum(CategoryPermission), default=CategoryPermission.READ_ALL)

    # 세분화된 권한 설정
    read_permission = Column(SQLEnum(PermissionLevel), default=PermissionLevel.ALL)    # 읽기 권한
    write_permission = Column(SQLEnum(PermissionLevel), default=PermissionLevel.USER)  # 쓰기 권한
    comment_permission = Column(SQLEnum(PermissionLevel), default=PermissionLevel.USER) # 댓글 권한

    # 그룹 헤더 여부 (True면 게시판이 아니라 섹션 제목)
    is_group = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계
    parent = relationship("Category", remote_side=[id], backref="subcategories")
    posts = relationship("Post", back_populates="category")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    # 콘텐츠
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(String(500))

    # 언어 및 번역
    source_lang = Column(String(2), default="ko")  # 원문 언어
    translated_title_ko = Column(String(255))
    translated_title_ru = Column(String(255))
    translated_content_ko = Column(Text)
    translated_content_ru = Column(Text)
    translated_summary_ko = Column(String(500))
    translated_summary_ru = Column(String(500))
    auto_translated = Column(Boolean, default=False)

    # 메타데이터
    tags = Column(JSON, default=list)
    images = Column(JSON, default=list)
    attachments = Column(JSON, default=list)

    # 상태
    status = Column(SQLEnum(PostStatus), default=PostStatus.PUBLISHED)
    is_pinned = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    allow_comments = Column(Boolean, default=True)

    # 통계
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)
    report_count = Column(Integer, default=0)

    # SEO
    slug = Column(String(255), unique=True, index=True)
    meta_title = Column(String(255))
    meta_description = Column(String(500))

    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime)
    deleted_at = Column(DateTime)

    # 관계
    author = relationship("User", back_populates="posts")
    category = relationship("Category", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    likes = relationship("PostLike", back_populates="post", cascade="all, delete-orphan")
    bookmarks = relationship("Bookmark", back_populates="post", cascade="all, delete-orphan")
    # reports = relationship("Report", primaryjoin="and_(Post.id==Report.target_id, Report.target_type=='post')", foreign_keys="[Report.target_id]")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)

    # 콘텐츠
    content = Column(Text, nullable=False)
    source_lang = Column(String(2), default="ko")
    translated_content_ko = Column(Text)
    translated_content_ru = Column(Text)
    auto_translated = Column(Boolean, default=False)

    # 상태
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime)

    # 통계
    like_count = Column(Integer, default=0)
    report_count = Column(Integer, default=0)

    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계
    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")
    parent = relationship("Comment", remote_side=[id], backref="replies")
    likes = relationship("CommentLike", back_populates="comment", cascade="all, delete-orphan")

class PostLike(Base):
    __tablename__ = "post_likes"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    post = relationship("Post", back_populates="likes")

class CommentLike(Base):
    __tablename__ = "comment_likes"

    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable=False)
    user_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    comment = relationship("Comment", back_populates="likes")

class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="bookmarks")
    post = relationship("Post", back_populates="bookmarks")