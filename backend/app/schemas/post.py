from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class PostStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    HIDDEN = "hidden"
    DELETED = "deleted"

class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="게시글 제목")
    content: str = Field(..., min_length=1, description="게시글 내용")
    summary: Optional[str] = Field(None, max_length=500, description="요약")
    category_id: Optional[int] = Field(None, description="카테고리 ID")
    tags: Optional[List[str]] = Field(default_factory=list, description="태그 목록")
    images: Optional[List[str]] = Field(default_factory=list, description="이미지 URL 목록")
    attachments: Optional[List[dict]] = Field(default_factory=list, description="첨부파일 목록")
    allow_comments: bool = Field(True, description="댓글 허용 여부")
    source_lang: str = Field("ko", description="원문 언어 (ko 또는 ru)")

class PostCreate(PostBase):
    """게시글 생성 스키마"""
    category_slug: Optional[str] = Field(None, description="카테고리 slug (category_id 대신 사용 가능)")
    auto_translate: bool = Field(True, description="자동 번역 여부")

    @field_validator('category_id')
    @classmethod
    def validate_category(cls, v, info):
        # category_id와 category_slug 중 하나는 반드시 있어야 함
        category_slug = info.data.get('category_slug')
        if v is None and category_slug is None:
            raise ValueError('category_id 또는 category_slug 중 하나는 필수입니다')
        return v

    @field_validator('source_lang')
    @classmethod
    def validate_source_lang(cls, v):
        if v not in ['ko', 'ru']:
            raise ValueError('source_lang must be "ko" or "ru"')
        return v

class PostUpdate(BaseModel):
    """게시글 수정 스키마"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = Field(None, min_length=1)
    summary: Optional[str] = Field(None, max_length=500)
    category_id: Optional[int] = None
    tags: Optional[List[str]] = None
    status: Optional[PostStatus] = None
    is_pinned: Optional[bool] = None
    is_featured: Optional[bool] = None
    allow_comments: Optional[bool] = None
    auto_translate: bool = Field(True, description="자동 번역 여부")

class PostTranslation(BaseModel):
    """게시글 번역 정보"""
    title_ko: Optional[str] = None
    title_ru: Optional[str] = None
    content_ko: Optional[str] = None
    content_ru: Optional[str] = None
    summary_ko: Optional[str] = None
    summary_ru: Optional[str] = None

class AuthorInfo(BaseModel):
    """작성자 정보"""
    id: int
    username: Optional[str] = None
    nickname: Optional[str] = None
    email: str
    profile_image: Optional[str] = None

    class Config:
        from_attributes = True

class PostResponse(PostBase):
    """게시글 응답 스키마"""
    id: int
    user_id: int
    slug: Optional[str] = None
    status: PostStatus
    source_lang: str

    # 번역된 내용
    translated_title_ko: Optional[str] = None
    translated_title_ru: Optional[str] = None
    translated_content_ko: Optional[str] = None
    translated_content_ru: Optional[str] = None
    translated_summary_ko: Optional[str] = None
    translated_summary_ru: Optional[str] = None
    auto_translated: bool = False

    # 메타데이터
    is_pinned: bool = False
    is_featured: bool = False

    # 통계
    view_count: int = 0
    like_count: int = 0
    comment_count: int = 0
    share_count: int = 0

    # 타임스탬프
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None

    # 작성자 정보
    author: Optional[AuthorInfo] = None

    class Config:
        from_attributes = True

class PostListResponse(BaseModel):
    """게시글 목록 응답"""
    items: List[PostResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
