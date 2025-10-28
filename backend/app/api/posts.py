from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime
import re

from app.db.database import get_db
from app.models.post import Post, PostStatus, Category
from app.models.user import User
from app.schemas.post import PostCreate, PostUpdate, PostResponse, PostListResponse
from app.services.translation import translation_service
from app.utils.logger import setup_logger
from app.core.dependencies import get_current_user, get_optional_current_user

logger = setup_logger(__name__)
router = APIRouter()

def generate_slug(title: str, post_id: int) -> str:
    """게시글 제목으로부터 slug 생성"""
    # 한글, 러시아어, 영문, 숫자만 추출
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return f"{slug[:50]}-{post_id}"

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """게시글 생성 및 자동 번역 (로그인 필수)"""
    try:
        # category_slug가 제공된 경우 category_id로 변환
        category_id = post_data.category_id
        if post_data.category_slug and not category_id:
            category = db.query(Category).filter(Category.slug == post_data.category_slug).first()
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"카테고리 '{post_data.category_slug}'를 찾을 수 없습니다"
                )
            category_id = category.id

        # 카테고리 존재 확인
        if not category_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="category_id 또는 category_slug가 필요합니다"
            )

        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="카테고리를 찾을 수 없습니다"
            )

        # 공지사항 카테고리 확인 (관리자만 작성 가능)
        if category.slug == "notice" and current_user.role.value not in ["admin", "moderator"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="공지사항은 관리자만 작성할 수 있습니다"
            )

        # 게시글 생성
        new_post = Post(
            user_id=current_user.id,
            category_id=category_id,
            title=post_data.title,
            content=post_data.content,
            summary=post_data.summary,
            source_lang=post_data.source_lang,
            tags=post_data.tags,
            images=post_data.images,
            attachments=post_data.attachments,
            allow_comments=post_data.allow_comments,
            status=PostStatus.PUBLISHED,
            published_at=datetime.utcnow(),
            auto_translated=False
        )

        db.add(new_post)
        db.flush()  # ID 생성

        # Slug 생성
        new_post.slug = generate_slug(post_data.title, new_post.id)

        # 자동 번역 처리
        if post_data.auto_translate:
            try:
                # 원문 언어 확인
                source_lang = post_data.source_lang
                target_lang = "ru" if source_lang == "ko" else "ko"

                # 제목 번역
                title_result = await translation_service.translate_text(
                    post_data.title,
                    target_lang=target_lang,
                    source_lang=source_lang
                )

                # 내용 번역
                content_result = await translation_service.translate_text(
                    post_data.content,
                    target_lang=target_lang,
                    source_lang=source_lang
                )

                # 요약 번역 (있는 경우)
                summary_result = None
                if post_data.summary:
                    summary_result = await translation_service.translate_text(
                        post_data.summary,
                        target_lang=target_lang,
                        source_lang=source_lang
                    )

                # 번역 결과 저장
                if source_lang == "ko":
                    # 한국어가 원문인 경우
                    new_post.translated_title_ko = post_data.title
                    new_post.translated_content_ko = post_data.content
                    new_post.translated_summary_ko = post_data.summary
                    new_post.translated_title_ru = title_result["translated_text"]
                    new_post.translated_content_ru = content_result["translated_text"]
                    new_post.translated_summary_ru = summary_result["translated_text"] if summary_result else None
                else:
                    # 러시아어가 원문인 경우
                    new_post.translated_title_ru = post_data.title
                    new_post.translated_content_ru = post_data.content
                    new_post.translated_summary_ru = post_data.summary
                    new_post.translated_title_ko = title_result["translated_text"]
                    new_post.translated_content_ko = content_result["translated_text"]
                    new_post.translated_summary_ko = summary_result["translated_text"] if summary_result else None

                new_post.auto_translated = True
                logger.info(f"게시글 ID {new_post.id} 자동 번역 완료: {source_lang} → {target_lang}")

            except Exception as e:
                logger.error(f"게시글 번역 실패: {e}")
                # 번역 실패 시에도 게시글은 저장
                new_post.auto_translated = False

        db.commit()
        db.refresh(new_post)

        return new_post

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"게시글 생성 실패: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="게시글 생성 중 오류가 발생했습니다"
        )

@router.get("/", response_model=PostListResponse)
async def get_posts(
    page: int = 1,
    page_size: int = 20,
    category_id: Optional[int] = None,
    status_filter: Optional[PostStatus] = PostStatus.PUBLISHED,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """게시글 목록 조회 (로그인 불필요)"""
    try:
        # 기본 쿼리 (author 정보 포함)
        query = db.query(Post).options(joinedload(Post.author))

        # 필터 적용
        if category_id:
            query = query.filter(Post.category_id == category_id)
        if status_filter:
            query = query.filter(Post.status == status_filter)

        # 전체 개수
        total = query.count()

        # 페이징
        offset = (page - 1) * page_size
        posts = query.order_by(desc(Post.created_at)).offset(offset).limit(page_size).all()

        return PostListResponse(
            items=posts,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size
        )

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        logger.error(f"게시글 목록 조회 실패: {e}")
        logger.error(f"상세 오류:\n{error_details}")
        print(f"[ERROR] 게시글 목록 조회 실패: {e}", flush=True)
        print(f"[ERROR] 상세 오류:\n{error_details}", flush=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"게시글 목록을 불러오는 중 오류가 발생했습니다: {str(e)}"
        )

@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """게시글 상세 조회 (공지사항 외 로그인 필수)"""
    post = db.query(Post).options(joinedload(Post.author)).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다"
        )

    # 로그인 하지 않은 경우, 공지사항만 조회 가능
    if not current_user:
        category = db.query(Category).filter(Category.id == post.category_id).first()
        if not category or category.slug != "notice":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="로그인이 필요합니다",
                headers={"WWW-Authenticate": "Bearer"}
            )

    # 조회수 증가
    post.view_count += 1
    db.commit()

    return post

@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """게시글 수정 및 재번역 (로그인 필수, 작성자 또는 관리자만)"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다"
        )

    # 공지사항은 관리자만 수정 가능
    category = db.query(Category).filter(Category.id == post.category_id).first()
    if category and category.slug == "notice":
        if current_user.role.value not in ["admin", "moderator"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="공지사항은 관리자만 수정할 수 있습니다"
            )
    else:
        # 일반 게시글은 작성자 또는 관리자만 수정 가능
        if post.user_id != current_user.id and current_user.role.value not in ["admin", "moderator"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="게시글 수정 권한이 없습니다"
            )

    try:
        # 수정 가능한 필드 업데이트
        update_data = post_data.model_dump(exclude_unset=True, exclude={'auto_translate'})

        # 제목이나 내용이 변경된 경우 재번역
        needs_retranslation = False
        if 'title' in update_data or 'content' in update_data:
            needs_retranslation = post_data.auto_translate

        for field, value in update_data.items():
            setattr(post, field, value)

        # 재번역 처리
        if needs_retranslation:
            try:
                source_lang = post.source_lang
                target_lang = "ru" if source_lang == "ko" else "ko"

                # 제목 번역 (변경된 경우)
                if 'title' in update_data:
                    title_result = await translation_service.translate_text(
                        post.title,
                        target_lang=target_lang,
                        source_lang=source_lang
                    )
                    if source_lang == "ko":
                        post.translated_title_ko = post.title
                        post.translated_title_ru = title_result["translated_text"]
                    else:
                        post.translated_title_ru = post.title
                        post.translated_title_ko = title_result["translated_text"]

                # 내용 번역 (변경된 경우)
                if 'content' in update_data:
                    content_result = await translation_service.translate_text(
                        post.content,
                        target_lang=target_lang,
                        source_lang=source_lang
                    )
                    if source_lang == "ko":
                        post.translated_content_ko = post.content
                        post.translated_content_ru = content_result["translated_text"]
                    else:
                        post.translated_content_ru = post.content
                        post.translated_content_ko = content_result["translated_text"]

                post.auto_translated = True
                logger.info(f"게시글 ID {post_id} 재번역 완료")

            except Exception as e:
                logger.error(f"게시글 재번역 실패: {e}")

        db.commit()
        db.refresh(post)

        return post

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"게시글 수정 실패: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="게시글 수정 중 오류가 발생했습니다"
        )

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """게시글 삭제 (로그인 필수, 작성자 또는 관리자만)"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다"
        )

    # 공지사항은 관리자만 삭제 가능
    category = db.query(Category).filter(Category.id == post.category_id).first()
    if category and category.slug == "notice":
        if current_user.role.value not in ["admin", "moderator"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="공지사항은 관리자만 삭제할 수 있습니다"
            )
    else:
        # 일반 게시글은 작성자 또는 관리자만 삭제 가능
        if post.user_id != current_user.id and current_user.role.value not in ["admin", "moderator"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="게시글 삭제 권한이 없습니다"
            )

    # 소프트 삭제
    post.status = PostStatus.DELETED
    post.deleted_at = datetime.utcnow()
    db.commit()

    return None