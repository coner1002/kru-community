"""
Initialize sample data for KRU Community
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.db.database import get_db
from app.models.post import Category, Post
from app.models.user import User, UserRole
from sqlalchemy.orm import Session
from datetime import datetime
import bcrypt


def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def init_categories(db: Session):
    """Initialize board categories"""
    categories_data = [
        {
            "slug": "free",
            "name_ko": "자유게시판",
            "name_ru": "Свободная доска",
            "description_ko": "자유롭게 이야기를 나누는 공간",
            "description_ru": "Место для свободного общения",
            "icon": "💬",
            "sort_order": 1,
        },
        {
            "slug": "notice",
            "name_ko": "공지사항",
            "name_ru": "Объявления",
            "description_ko": "중요한 공지사항",
            "description_ru": "Важные объявления",
            "icon": "📢",
            "sort_order": 0,
        },
        {
            "slug": "life",
            "name_ko": "생활정보",
            "name_ru": "Информация о жизни",
            "description_ko": "한국 생활 정보 공유",
            "description_ru": "Обмен информацией о жизни в Корее",
            "icon": "🏠",
            "sort_order": 2,
        },
        {
            "slug": "job",
            "name_ko": "구인구직",
            "name_ru": "Работа",
            "description_ko": "채용 정보 및 구직 정보",
            "description_ru": "Информация о работе",
            "icon": "💼",
            "sort_order": 3,
        },
        {
            "slug": "market",
            "name_ko": "장터",
            "name_ru": "Маркет",
            "description_ko": "중고 거래 및 물물교환",
            "description_ru": "Продажа и обмен",
            "icon": "🛒",
            "sort_order": 4,
        },
        {
            "slug": "startup",
            "name_ko": "창업게시판",
            "name_ru": "Стартап",
            "description_ko": "창업 정보 및 경험 공유",
            "description_ru": "Информация о стартапах",
            "icon": "🚀",
            "sort_order": 5,
        },
        {
            "slug": "admin",
            "name_ko": "관리자게시판",
            "name_ru": "Администрация",
            "description_ko": "관리자 전용 게시판",
            "description_ru": "Доска администратора",
            "icon": "🔒",
            "sort_order": 6,
        },
    ]

    print("Creating categories...")
    created_categories = {}
    for cat_data in categories_data:
        existing = db.query(Category).filter(Category.slug == cat_data["slug"]).first()
        if existing:
            print(f"  - Category '{cat_data['slug']}' already exists")
            created_categories[cat_data["slug"]] = existing
        else:
            category = Category(**cat_data)
            db.add(category)
            created_categories[cat_data["slug"]] = category
            print(f"  + Created category: {cat_data['slug']}")

    db.commit()
    print(f"Categories initialized: {len(created_categories)}")
    return created_categories


def init_test_user(db: Session):
    """Initialize test user"""
    print("Creating test user...")

    # Check by email or username
    existing = db.query(User).filter(
        (User.email == "test@russian.town") | (User.username == "testuser")
    ).first()

    if existing:
        print(f"  - Test user already exists (email: {existing.email})")
        return existing

    user = User(
        email="test@russian.town",
        username="testuser",
        nickname="테스트유저",
        password_hash=hash_password("test1234"),
        role=UserRole.USER,
        is_active=True,
        is_verified=True,
        preferred_lang="ko",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(user)
    db.commit()
    print("  + Test user created: test@russian.town / test1234")
    return user


def init_sample_posts(db: Session, categories: dict, user: User):
    """Initialize sample posts"""
    print("Creating sample posts...")

    posts_data = [
        {
            "category": "notice",
            "title": "Russian.Town 커뮤니티에 오신 것을 환영합니다!",
            "content": """안녕하세요!

Russian.Town은 한국에 거주하는 러시아인과 러시아어 사용자들을 위한 커뮤니티 플랫폼입니다.

주요 기능:
- 다양한 게시판 (자유게시판, 생활정보, 구인구직, 장터 등)
- 한국어/러시아어 자동 번역
- 비즈니스 디렉토리
- OAuth 소셜 로그인

자유롭게 정보를 공유하고 소통해 주세요!""",
            "views": 150
        },
        {
            "category": "notice",
            "title": "Добро пожаловать в сообщество Russian.Town!",
            "content": """Здравствуйте!

Russian.Town - это платформа сообщества для русскоговорящих жителей Кореи.

Основные функции:
- Различные доски (свободная доска, информация о жизни, работа, маркет)
- Автоматический перевод корейского/русского языка
- Бизнес-каталог
- OAuth социальный вход

Свободно делитесь информацией и общайтесь!""",
            "views": 120
        },
        {
            "category": "free",
            "title": "서울에서 러시아 음식점 추천해주세요",
            "content": "안녕하세요! 서울에서 맛있는 러시아 음식점을 찾고 있습니다. 추천 부탁드립니다.",
            "views": 45
        },
        {
            "category": "free",
            "title": "Рекомендации русских ресторанов в Сеуле",
            "content": "Здравствуйте! Ищу вкусные русские рестораны в Сеуле. Буду благодарен за рекомендации.",
            "views": 38
        },
        {
            "category": "life",
            "title": "한국 의료보험 가입 방법",
            "content": """외국인으로서 한국 의료보험에 가입하는 방법을 공유합니다.

1. 외국인등록증 준비
2. 국민건강보험공단 방문
3. 필요 서류 제출
4. 보험료 납부

자세한 사항은 국민건강보험공단 웹사이트를 참고하세요.""",
            "views": 67
        },
        {
            "category": "life",
            "title": "Как оформить медицинскую страховку в Корее",
            "content": """Делюсь информацией о том, как иностранцу оформить медицинскую страховку в Корее.

1. Подготовка карты иностранца
2. Посещение Национальной службы медицинского страхования
3. Подача необходимых документов
4. Оплата страховых взносов

Подробности на сайте Национальной службы медицинского страхования.""",
            "views": 59
        },
        {
            "category": "job",
            "title": "[채용] IT 스타트업에서 러시아어 가능한 개발자를 찾습니다",
            "content": """강남 소재 IT 스타트업에서 러시아어가 가능한 백엔드 개발자를 채용합니다.

우대사항:
- Python/Django 경험
- 러시아어 능통
- 한국어 의사소통 가능

관심 있으신 분은 메시지 주세요!""",
            "views": 89
        },
        {
            "category": "job",
            "title": "[Вакансия] IT стартап ищет разработчика",
            "content": """IT стартап в районе Каннам нанимает backend разработчика со знанием русского языка.

Преимущества:
- Опыт работы с Python/Django
- Свободное владение русским языком
- Способность общаться на корейском

Заинтересованным просьба написать!""",
            "views": 76
        },
        {
            "category": "market",
            "title": "냉장고 판매합니다 (삼성 300L)",
            "content": """2년 사용한 삼성 냉장고 판매합니다.
가격: 20만원 (협상 가능)
위치: 서울 강남구
상태: 매우 깨끗""",
            "views": 34
        },
        {
            "category": "market",
            "title": "Продаю холодильник (Samsung 300L)",
            "content": """Продаю холодильник Samsung, использовался 2 года.
Цена: 200,000 вон (договорная)
Местоположение: Каннам-гу, Сеул
Состояние: отличное""",
            "views": 28
        },
        {
            "category": "startup",
            "title": "한국에서 스타트업 창업 경험 공유",
            "content": """최근 한국에서 IT 스타트업을 창업한 경험을 공유합니다.

주요 포인트:
- 법인 설립 절차
- 투자 유치 방법
- 정부 지원 프로그램
- 실수했던 부분들

궁금한 점 있으시면 댓글로 질문해주세요!""",
            "views": 102
        },
        {
            "category": "startup",
            "title": "Опыт создания стартапа в Корее",
            "content": """Делюсь опытом создания IT стартапа в Корее.

Основные моменты:
- Процедура регистрации компании
- Привлечение инвестиций
- Государственные программы поддержки
- Ошибки, которых стоит избегать

Если есть вопросы, пишите в комментариях!""",
            "views": 94
        },
    ]

    created = 0
    for post_data in posts_data:
        category_slug = post_data.pop("category")
        category = categories.get(category_slug)

        if not category:
            print(f"  ! Category '{category_slug}' not found, skipping post")
            continue

        post = Post(
            category_id=category.id,
            user_id=user.id,
            title=post_data["title"],
            content=post_data["content"],
            view_count=post_data.get("views", 0),
            status="PUBLISHED",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        db.add(post)
        created += 1

    db.commit()
    print(f"  + Created {created} sample posts")


def main():
    """Main initialization function"""
    print("=" * 60)
    print("Initializing sample data for Russian.Town")
    print("=" * 60)

    db = next(get_db())

    try:
        # Initialize categories
        categories = init_categories(db)

        # Initialize test user
        user = init_test_user(db)

        # Initialize sample posts
        init_sample_posts(db, categories, user)

        print("\n" + "=" * 60)
        print("Sample data initialization complete!")
        print("=" * 60)
        print("\nTest User Credentials:")
        print("  Email: test@russian.town")
        print("  Password: test1234")
        print("\nYou can now access the board pages with sample data.")

    except Exception as e:
        print(f"\nError during initialization: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
