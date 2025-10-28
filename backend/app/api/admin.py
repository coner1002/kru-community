from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from datetime import datetime, timedelta
from typing import Optional, List
from app.db.database import get_db
from app.core.dependencies import get_current_admin
from app.models.user import User
from app.models.post import Post, Comment, Category
from app.models.partner import Partner
from app.models.admin import Report, ReportStatus, Banner, AuditLog, SystemNotice, BlockedKeyword, SystemSettings
from pydantic import BaseModel

router = APIRouter()

# Pydantic schemas
class DashboardStats(BaseModel):
    total_users: int
    total_posts: int
    total_comments: int
    total_partners: int
    new_users_today: int
    new_posts_today: int
    pending_reports: int
    active_banners: int

class ReportResponse(BaseModel):
    id: int
    target_type: str
    target_id: int
    reporter_id: int
    reporter_email: str
    reason: str
    description: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class ReportUpdateRequest(BaseModel):
    status: str
    resolution_note: Optional[str] = None

class BannerCreate(BaseModel):
    position: str
    title: Optional[str]
    image_url: str
    link_url: Optional[str]
    advertiser_name: Optional[str]
    advertiser_contact: Optional[str]
    start_at: datetime
    end_at: datetime
    priority: int = 0

class BannerUpdate(BaseModel):
    position: Optional[str]
    title: Optional[str]
    image_url: Optional[str]
    link_url: Optional[str]
    is_active: Optional[bool]
    priority: Optional[int]

class SystemNoticeCreate(BaseModel):
    title_ko: str
    title_ru: Optional[str]
    content_ko: str
    content_ru: Optional[str]
    type: str = "info"
    is_important: bool = False
    show_from: Optional[datetime]
    show_until: Optional[datetime]

class UserManagementResponse(BaseModel):
    id: int
    email: str
    nickname: str
    nickname_ko: Optional[str] = None  # 한글 닉네임
    nickname_ru: Optional[str] = None  # 러시아어 닉네임
    role: str  # admin, staff, premium, user
    user_type: Optional[str] = None  # admin, staff, virtual, real
    is_active: bool
    is_verified: bool
    created_at: datetime
    # 페르소나 정보 (가상회원용)
    ethnicity: Optional[str] = None
    persona_age: Optional[int] = None
    persona_gender: Optional[str] = None
    persona_occupation: Optional[str] = None
    persona_interests: Optional[str] = None
    persona_activity_level: Optional[str] = None
    persona_posting_style: Optional[str] = None
    persona_korean_level: Optional[str] = None
    persona_russian_level: Optional[str] = None

    class Config:
        from_attributes = True

class PersonaUpdateRequest(BaseModel):
    ethnicity: Optional[str] = None
    persona_age: Optional[int] = None
    persona_gender: Optional[str] = None
    persona_occupation: Optional[str] = None
    persona_interests: Optional[str] = None
    persona_activity_level: Optional[str] = None
    persona_posting_style: Optional[str] = None
    persona_korean_level: Optional[str] = None
    persona_russian_level: Optional[str] = None

# Dashboard
@router.get("/dashboard", response_model=DashboardStats)
async def get_admin_dashboard(
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin)
):
    """관리자 대시보드 통계"""
    today = datetime.utcnow().date()

    total_users = db.query(func.count(User.id)).scalar()
    total_posts = db.query(func.count(Post.id)).scalar()
    total_comments = db.query(func.count(Comment.id)).scalar()
    total_partners = db.query(func.count(Partner.id)).scalar()

    new_users_today = db.query(func.count(User.id)).filter(
        func.date(User.created_at) == today
    ).scalar()

    new_posts_today = db.query(func.count(Post.id)).filter(
        func.date(Post.created_at) == today
    ).scalar()

    pending_reports = db.query(func.count(Report.id)).filter(
        Report.status == ReportStatus.PENDING
    ).scalar()

    active_banners = db.query(func.count(Banner.id)).filter(
        and_(
            Banner.is_active == True,
            Banner.start_at <= datetime.utcnow(),
            Banner.end_at >= datetime.utcnow()
        )
    ).scalar()

    return DashboardStats(
        total_users=total_users or 0,
        total_posts=total_posts or 0,
        total_comments=total_comments or 0,
        total_partners=total_partners or 0,
        new_users_today=new_users_today or 0,
        new_posts_today=new_posts_today or 0,
        pending_reports=pending_reports or 0,
        active_banners=active_banners or 0
    )

# 신고 관리
@router.get("/reports", response_model=List[ReportResponse])
async def get_reports(
    status: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin)
):
    """신고 목록 조회"""
    query = db.query(Report).join(User, Report.reporter_id == User.id)

    if status:
        query = query.filter(Report.status == status)

    reports = query.order_by(Report.created_at.desc()).offset(skip).limit(limit).all()

    return [
        ReportResponse(
            id=r.id,
            target_type=r.target_type.value,
            target_id=r.target_id,
            reporter_id=r.reporter_id,
            reporter_email=r.reporter.email,
            reason=r.reason.value,
            description=r.description,
            status=r.status.value,
            created_at=r.created_at
        ) for r in reports
    ]

@router.patch("/reports/{report_id}")
async def update_report(
    report_id: int,
    update_data: ReportUpdateRequest,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin)
):
    """신고 상태 업데이트"""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    report.status = ReportStatus(update_data.status)
    report.handled_by = admin_user.id
    if update_data.resolution_note:
        report.resolution_note = update_data.resolution_note
    if update_data.status in ["resolved", "dismissed"]:
        report.resolved_at = datetime.utcnow()

    db.commit()
    return {"message": "Report updated successfully"}

# 사용자 관리
@router.get("/users/count")
async def get_users_count(
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    user_type: Optional[str] = None,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin)
):
    """사용자 총 수 조회"""
    query = db.query(func.count(User.id))

    if search:
        query = query.filter(
            or_(
                User.email.ilike(f"%{search}%"),
                User.nickname.ilike(f"%{search}%")
            )
        )

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    if user_type is not None:
        query = query.filter(User.user_type == user_type.upper())

    total = query.scalar()
    return {"total": total}

@router.get("/users", response_model=List[UserManagementResponse])
async def get_users(
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    user_type: Optional[str] = None,  # admin, staff, virtual, real
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin)
):
    """사용자 목록 조회 (user_type 필터 추가)"""
    query = db.query(User)

    if search:
        query = query.filter(
            or_(
                User.email.ilike(f"%{search}%"),
                User.nickname.ilike(f"%{search}%")
            )
        )

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    # user_type 필터링 (대소문자 구분 없이)
    if user_type is not None:
        query = query.filter(User.user_type == user_type.upper())

    users = query.order_by(User.created_at.desc()).offset(skip).limit(limit).all()
    return users

@router.patch("/users/{user_id}/toggle-active")
async def toggle_user_active(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin)
):
    """사용자 활성/비활성 토글"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = not user.is_active
    db.commit()

    return {"message": f"User {'activated' if user.is_active else 'deactivated'}", "is_active": user.is_active}

@router.patch("/users/{user_id}/persona")
async def update_user_persona(
    user_id: int,
    persona_data: PersonaUpdateRequest,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin)
):
    """가상회원 페르소나 정보 업데이트"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 페르소나 필드 업데이트
    if persona_data.ethnicity is not None:
        user.ethnicity = persona_data.ethnicity
    if persona_data.persona_age is not None:
        user.persona_age = persona_data.persona_age
    if persona_data.persona_gender is not None:
        user.persona_gender = persona_data.persona_gender
    if persona_data.persona_occupation is not None:
        user.persona_occupation = persona_data.persona_occupation
    if persona_data.persona_interests is not None:
        user.persona_interests = persona_data.persona_interests
    if persona_data.persona_activity_level is not None:
        user.persona_activity_level = persona_data.persona_activity_level
    if persona_data.persona_posting_style is not None:
        user.persona_posting_style = persona_data.persona_posting_style
    if persona_data.persona_korean_level is not None:
        user.persona_korean_level = persona_data.persona_korean_level
    if persona_data.persona_russian_level is not None:
        user.persona_russian_level = persona_data.persona_russian_level

    db.commit()
    db.refresh(user)

    return {"message": "Persona updated successfully", "user": user}

# 게시글 관리
@router.get("/posts")
async def get_posts_admin(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin)
):
    """게시글 목록 조회 (관리자용)"""
    posts = db.query(Post).order_by(Post.created_at.desc()).offset(skip).limit(limit).all()
    return posts

@router.delete("/posts/{post_id}")
async def delete_post_admin(
    post_id: int,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin)
):
    """게시글 삭제"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"}

# 배너 관리
@router.get("/banners")
async def get_banners(
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin)
):
    """배너 목록 조회"""
    query = db.query(Banner)
    if is_active is not None:
        query = query.filter(Banner.is_active == is_active)

    banners = query.order_by(Banner.priority.desc(), Banner.created_at.desc()).all()
    return banners

@router.post("/banners")
async def create_banner(
    banner: BannerCreate,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin)
):
    """배너 생성"""
    new_banner = Banner(**banner.dict())
    db.add(new_banner)
    db.commit()
    db.refresh(new_banner)
    return new_banner

@router.patch("/banners/{banner_id}")
async def update_banner(
    banner_id: int,
    banner_update: BannerUpdate,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin)
):
    """배너 수정"""
    banner = db.query(Banner).filter(Banner.id == banner_id).first()
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")

    for key, value in banner_update.dict(exclude_unset=True).items():
        setattr(banner, key, value)

    banner.updated_at = datetime.utcnow()
    db.commit()
    return banner

@router.delete("/banners/{banner_id}")
async def delete_banner(
    banner_id: int,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin)
):
    """배너 삭제"""
    banner = db.query(Banner).filter(Banner.id == banner_id).first()
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")

    db.delete(banner)
    db.commit()
    return {"message": "Banner deleted successfully"}

# 감사 로그
@router.get("/audit-logs")
async def get_audit_logs(
    action: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin)
):
    """감사 로그 조회"""
    query = db.query(AuditLog)

    if action:
        query = query.filter(AuditLog.action == action)

    logs = query.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()
    return logs

# 시스템 공지
@router.post("/notices")
async def create_notice(
    notice: SystemNoticeCreate,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin)
):
    """시스템 공지 생성"""
    new_notice = SystemNotice(**notice.dict())
    db.add(new_notice)
    db.commit()
    db.refresh(new_notice)
    return new_notice

@router.get("/notices")
async def get_notices(
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin)
):
    """시스템 공지 목록"""
    query = db.query(SystemNotice)
    if is_active is not None:
        query = query.filter(SystemNotice.is_active == is_active)

    notices = query.order_by(SystemNotice.created_at.desc()).all()
    return notices

# System Settings endpoints
class SystemSettingResponse(BaseModel):
    id: int
    key: str
    value: Optional[str]
    description: Optional[str]
    category: str
    is_encrypted: bool
    updated_at: datetime

    class Config:
        from_attributes = True

class SystemSettingUpdate(BaseModel):
    value: str

@router.get("/settings", response_model=List[SystemSettingResponse])
async def get_system_settings(
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin)
):
    """시스템 설정 목록 조회"""
    query = db.query(SystemSettings)
    if category:
        query = query.filter(SystemSettings.category == category)

    settings = query.order_by(SystemSettings.category, SystemSettings.key).all()
    return settings

@router.get("/settings/{key}", response_model=SystemSettingResponse)
async def get_system_setting(
    key: str,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin)
):
    """특정 시스템 설정 조회"""
    setting = db.query(SystemSettings).filter(SystemSettings.key == key).first()
    if not setting:
        raise HTTPException(status_code=404, detail="설정을 찾을 수 없습니다")
    return setting

@router.put("/settings/{key}", response_model=SystemSettingResponse)
async def update_system_setting(
    key: str,
    update_data: SystemSettingUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin)
):
    """시스템 설정 업데이트"""
    setting = db.query(SystemSettings).filter(SystemSettings.key == key).first()
    if not setting:
        raise HTTPException(status_code=404, detail="설정을 찾을 수 없습니다")

    setting.value = update_data.value
    setting.updated_by = admin_user.id
    setting.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(setting)

    return setting

@router.post("/test-deepl")
async def test_deepl_connection(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin)
):
    """DeepL API 연결 테스트"""
    import httpx

    # 데이터베이스에서 DeepL API 키 가져오기
    setting = db.query(SystemSettings).filter(SystemSettings.key == "deepl_api_key").first()
    if not setting or not setting.value:
        raise HTTPException(status_code=400, detail="DeepL API Key가 설정되지 않았습니다")

    api_key = setting.value.strip()

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                'https://api-free.deepl.com/v2/translate',
                headers={
                    'Authorization': f'DeepL-Auth-Key {api_key}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                data={
                    'text': '안녕하세요',
                    'target_lang': 'RU'
                },
                timeout=10.0
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "message": "DeepL API 연결 성공",
                    "test_translation": {
                        "original": "안녕하세요",
                        "translated": data['translations'][0]['text']
                    }
                }
            elif response.status_code == 403:
                raise HTTPException(status_code=403, detail="API Key가 유효하지 않습니다")
            else:
                raise HTTPException(status_code=response.status_code, detail=f"DeepL API 오류: {response.text}")

    except httpx.TimeoutException:
        raise HTTPException(status_code=408, detail="DeepL API 요청 시간 초과")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"연결 실패: {str(e)}")

# 카테고리(게시판) 관리
class CategoryCreate(BaseModel):
    slug: str
    name_ko: str
    name_ru: str
    description_ko: Optional[str] = None
    description_ru: Optional[str] = None
    icon: Optional[str] = None
    sort_order: int = 0
    is_active: Optional[bool] = True  # 활성화 여부
    parent_id: Optional[int] = None
    is_group: Optional[bool] = False  # 그룹 헤더 여부
    layout_type: Optional[str] = "list"  # list, card, gallery, form
    permission: Optional[str] = "read_all"  # public, read_all, login_only, admin_only (deprecated)
    read_permission: Optional[str] = "ALL"  # ALL, USER, PREMIUM, STAFF, ADMIN
    write_permission: Optional[str] = "USER"  # ALL, USER, PREMIUM, STAFF, ADMIN
    comment_permission: Optional[str] = "USER"  # ALL, USER, PREMIUM, STAFF, ADMIN

class CategoryUpdate(BaseModel):
    slug: Optional[str] = None
    name_ko: Optional[str] = None
    name_ru: Optional[str] = None
    description_ko: Optional[str] = None
    description_ru: Optional[str] = None
    icon: Optional[str] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None
    parent_id: Optional[int] = None
    is_group: Optional[bool] = None
    layout_type: Optional[str] = None
    permission: Optional[str] = None  # deprecated
    read_permission: Optional[str] = None  # ALL, USER, PREMIUM, STAFF, ADMIN
    write_permission: Optional[str] = None  # ALL, USER, PREMIUM, STAFF, ADMIN
    comment_permission: Optional[str] = None  # ALL, USER, PREMIUM, STAFF, ADMIN

class CategoryResponse(BaseModel):
    id: int
    slug: str
    name_ko: str
    name_ru: str
    description_ko: Optional[str]
    description_ru: Optional[str]
    icon: Optional[str]
    sort_order: int
    is_active: bool
    parent_id: Optional[int]
    is_group: bool
    layout_type: str
    permission: Optional[str] = None  # deprecated
    read_permission: Optional[str] = "ALL"  # ALL, USER, PREMIUM, STAFF, ADMIN
    write_permission: Optional[str] = "USER"  # ALL, USER, PREMIUM, STAFF, ADMIN
    comment_permission: Optional[str] = "USER"  # ALL, USER, PREMIUM, STAFF, ADMIN
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

@router.get("/categories", response_model=List[CategoryResponse])
async def get_all_categories(
    include_inactive: bool = Query(False),
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin)
):
    """모든 카테고리 조회 (비활성 포함)"""
    query = db.query(Category)
    if not include_inactive:
        query = query.filter(Category.is_active == True)

    categories = query.order_by(Category.sort_order, Category.id).all()
    return categories

@router.post("/categories", response_model=CategoryResponse)
async def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin)
):
    """새 카테고리 생성"""
    # slug 중복 확인
    existing = db.query(Category).filter(Category.slug == category_data.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="이미 존재하는 slug입니다")

    # parent_id 유효성 검사
    if category_data.parent_id:
        parent = db.query(Category).filter(Category.id == category_data.parent_id).first()
        if not parent:
            raise HTTPException(status_code=404, detail="상위 카테고리를 찾을 수 없습니다")

    new_category = Category(**category_data.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

@router.put("/categories/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin)
):
    """카테고리 수정"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="카테고리를 찾을 수 없습니다")

    # slug 중복 확인
    if category_data.slug and category_data.slug != category.slug:
        existing = db.query(Category).filter(Category.slug == category_data.slug).first()
        if existing:
            raise HTTPException(status_code=400, detail="이미 존재하는 slug입니다")

    # parent_id 유효성 검사
    if category_data.parent_id:
        if category_data.parent_id == category_id:
            raise HTTPException(status_code=400, detail="자기 자신을 상위 카테고리로 설정할 수 없습니다")
        parent = db.query(Category).filter(Category.id == category_data.parent_id).first()
        if not parent:
            raise HTTPException(status_code=404, detail="상위 카테고리를 찾을 수 없습니다")

    # 업데이트
    for key, value in category_data.dict(exclude_unset=True).items():
        setattr(category, key, value)

    category.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(category)

    return category

@router.delete("/categories/{category_id}")
async def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin)
):
    """카테고리 삭제 (소프트 삭제 - is_active를 False로)"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="카테고리를 찾을 수 없습니다")

    # 하위 카테고리 확인
    has_subcategories = db.query(Category).filter(Category.parent_id == category_id).count() > 0
    if has_subcategories:
        raise HTTPException(status_code=400, detail="하위 카테고리가 있어 삭제할 수 없습니다")

    # 게시글 확인
    has_posts = db.query(Post).filter(Post.category_id == category_id).count() > 0
    if has_posts:
        # 소프트 삭제
        category.is_active = False
        category.updated_at = datetime.utcnow()
        db.commit()
        return {"message": "카테고리가 비활성화되었습니다 (게시글이 존재함)"}
    else:
        # 실제 삭제
        db.delete(category)
        db.commit()
        return {"message": "카테고리가 삭제되었습니다"}