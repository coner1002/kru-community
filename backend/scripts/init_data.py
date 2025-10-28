"""
데이터베이스 초기 데이터 생성 스크립트
"""
import sys
import os
from pathlib import Path

# UTF-8 인코딩 설정 (Windows 호환)
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# 프로젝트 루트를 Python 경로에 추가
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine, Base
from app.models.user import User, UserRole, Language
from app.models.post import Category, PostStatus
from datetime import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_database():
    """데이터베이스 초기화"""
    print("데이터베이스 테이블 생성 중...")
    Base.metadata.create_all(bind=engine)
    print("✓ 테이블 생성 완료")

def create_test_user(db: Session):
    """테스트 사용자 생성"""
    # 기존 사용자 확인
    existing_user = db.query(User).filter(User.email == "test@example.com").first()
    if existing_user:
        print(f"✓ 테스트 사용자 이미 존재: {existing_user.username} (ID: {existing_user.id})")
        return existing_user

    # 새 사용자 생성
    test_user = User(
        email="test@example.com",
        username="testuser",
        nickname="테스트 사용자",
        password_hash=pwd_context.hash("test1234"),
        role=UserRole.USER,
        preferred_lang=Language.KO,
        is_active=True,
        is_verified=True
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    print(f"✓ 테스트 사용자 생성: {test_user.username} (ID: {test_user.id})")
    return test_user

def create_regular_user(db: Session):
    """일반 사용자 생성"""
    # 기존 사용자 확인
    existing_user = db.query(User).filter(User.username == "coner1002").first()
    if existing_user:
        print(f"✓ 일반 사용자 이미 존재: {existing_user.username} (ID: {existing_user.id})")
        return existing_user

    # 새 일반 사용자 생성
    regular_user = User(
        email="coner1002@kru.community",
        username="coner1002",
        nickname="Coner",
        password_hash=pwd_context.hash("w2261vp!!@"),
        role=UserRole.USER,
        preferred_lang=Language.KO,
        is_active=True,
        is_verified=True
    )
    db.add(regular_user)
    db.commit()
    db.refresh(regular_user)
    print(f"✓ 일반 사용자 생성: {regular_user.username} (ID: {regular_user.id})")
    return regular_user

def create_categories(db: Session):
    """카테고리 생성"""
    categories_data = [
        {
            "slug": "notice",
            "name_ko": "공지사항",
            "name_ru": "Объявления",
            "description_ko": "중요한 공지사항",
            "description_ru": "Важные объявления",
            "icon": "📢",
            "sort_order": 1
        },
        {
            "slug": "free",
            "name_ko": "자유게시판",
            "name_ru": "Свободная доска",
            "description_ko": "자유롭게 이야기를 나누는 공간",
            "description_ru": "Место для свободного общения",
            "icon": "💬",
            "sort_order": 2
        },
        {
            "slug": "qna",
            "name_ko": "질문과 답변",
            "name_ru": "Вопросы и ответы",
            "description_ko": "궁금한 점을 물어보세요",
            "description_ru": "Задавайте вопросы",
            "icon": "❓",
            "sort_order": 3
        },
        {
            "slug": "market",
            "name_ko": "장터",
            "name_ru": "Рынок",
            "description_ko": "물건을 사고파는 장터",
            "description_ru": "Покупка и продажа товаров",
            "icon": "🛒",
            "sort_order": 4
        },
        {
            "slug": "job",
            "name_ko": "구인구직",
            "name_ru": "Работа",
            "description_ko": "구인 및 구직 정보",
            "description_ru": "Информация о работе",
            "icon": "💼",
            "sort_order": 5
        }
    ]

    created_count = 0
    for cat_data in categories_data:
        # 기존 카테고리 확인
        existing = db.query(Category).filter(Category.slug == cat_data["slug"]).first()
        if existing:
            print(f"  • {cat_data['name_ko']} ({cat_data['name_ru']}) - 이미 존재")
            continue

        # 새 카테고리 생성
        category = Category(**cat_data)
        db.add(category)
        created_count += 1
        print(f"  • {cat_data['name_ko']} ({cat_data['name_ru']}) - 생성")

    if created_count > 0:
        db.commit()
        print(f"✓ {created_count}개 카테고리 생성 완료")
    else:
        print("✓ 모든 카테고리가 이미 존재합니다")

def main():
    print("=" * 60)
    print("KRU Community - 데이터베이스 초기화")
    print("=" * 60)
    print()

    # 데이터베이스 초기화
    init_database()
    print()

    # 데이터베이스 세션 생성
    db = SessionLocal()

    try:
        # 테스트 사용자 생성
        print("테스트 사용자 생성 중...")
        test_user = create_test_user(db)
        print()

        # 일반 사용자 생성
        print("일반 사용자 생성 중...")
        regular_user = create_regular_user(db)
        print()

        # 카테고리 생성
        print("카테고리 생성 중...")
        create_categories(db)
        print()

        print("=" * 60)
        print("✓ 초기화 완료!")
        print("=" * 60)
        print()
        print("계정 정보:")
        print()
        print("1. 테스트 계정:")
        print(f"   이메일: test@example.com")
        print(f"   비밀번호: test1234")
        print(f"   User ID: {test_user.id}")
        print()
        print("2. 일반 사용자 계정:")
        print(f"   아이디: coner1002")
        print(f"   이메일: coner1002@kru.community")
        print(f"   비밀번호: w2261vp!!@")
        print(f"   User ID: {regular_user.id}")
        print()

    except Exception as e:
        print(f"✗ 오류 발생: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
