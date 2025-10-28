#!/usr/bin/env python3
"""
초기 데이터 생성 스크립트
- 관리자 계정 생성
- 기본 카테고리 생성
- 테스트 데이터 생성 (옵션)
"""

import sys
import os
from pathlib import Path

# 프로젝트 루트를 Python path에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "backend"))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from passlib.context import CryptContext
import argparse

# 모델 import
from app.models.user import User, UserRole, OAuthProvider, Language
from app.models.post import Category
from app.models.partner import Partner, PartnerCategory

# 비밀번호 해싱
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db_session():
    """데이터베이스 세션 생성"""
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://kru_user:password@localhost:5432/kru_community"
    )
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

def create_admin_user(db):
    """관리자 계정 생성"""
    print("📝 관리자 계정 생성 중...")

    # 기존 관리자 확인
    existing_admin = db.query(User).filter(User.username == "admin1234").first()
    if existing_admin:
        print("   ⚠️  관리자 계정이 이미 존재합니다.")
        return existing_admin

    # 관리자 계정 생성
    admin = User(
        email="admin@russki.center",
        username="admin1234",
        nickname="관리자",
        password_hash=pwd_context.hash("kuro##@@"),
        oauth_provider=OAuthProvider.EMAIL,
        preferred_lang=Language.KO,
        role=UserRole.ADMIN,
        is_active=True,
        is_verified=True,
        email_verified_at=datetime.utcnow(),
        created_at=datetime.utcnow()
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    print(f"   ✅ 관리자 계정 생성 완료: {admin.username} / kuro##@@")
    return admin

def create_categories(db):
    """기본 카테고리 생성"""
    print("\n📂 카테고리 생성 중...")

    categories_data = [
        {
            "slug": "notice",
            "name_ko": "공지사항",
            "name_ru": "Объявления",
            "description_ko": "사이트 공지사항 및 중요 알림",
            "description_ru": "Объявления сайта и важные уведомления",
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
            "name_ko": "질문답변",
            "name_ru": "Вопросы и ответы",
            "description_ko": "궁금한 점을 묻고 답하는 곳",
            "description_ru": "Задавайте вопросы и получайте ответы",
            "icon": "❓",
            "sort_order": 3
        },
        {
            "slug": "info",
            "name_ko": "정보공유",
            "name_ru": "Обмен информацией",
            "description_ko": "유용한 정보를 공유하는 게시판",
            "description_ru": "Делитесь полезной информацией",
            "icon": "ℹ️",
            "sort_order": 4
        },
        {
            "slug": "market",
            "name_ko": "중고장터",
            "name_ru": "Барахолка",
            "description_ko": "중고 물품 거래",
            "description_ru": "Покупка и продажа подержанных вещей",
            "icon": "🛒",
            "sort_order": 5
        },
        {
            "slug": "job",
            "name_ko": "구인구직",
            "name_ru": "Работа",
            "description_ko": "구인·구직 정보 교환",
            "description_ru": "Информация о работе",
            "icon": "💼",
            "sort_order": 6
        },
        {
            "slug": "event",
            "name_ko": "행사/이벤트",
            "name_ru": "События",
            "description_ko": "각종 행사 및 이벤트 안내",
            "description_ru": "Информация о мероприятиях и событиях",
            "icon": "🎉",
            "sort_order": 7
        },
        {
            "slug": "travel",
            "name_ko": "여행/관광",
            "name_ru": "Путешествия",
            "description_ko": "여행 정보 및 후기",
            "description_ru": "Информация о путешествиях",
            "icon": "✈️",
            "sort_order": 8
        }
    ]

    created_count = 0
    for cat_data in categories_data:
        # 기존 카테고리 확인
        existing = db.query(Category).filter(Category.slug == cat_data["slug"]).first()
        if existing:
            print(f"   ⚠️  카테고리 '{cat_data['name_ko']}'이(가) 이미 존재합니다.")
            continue

        category = Category(**cat_data)
        db.add(category)
        created_count += 1
        print(f"   ✅ {cat_data['icon']} {cat_data['name_ko']} / {cat_data['name_ru']}")

    if created_count > 0:
        db.commit()
        print(f"\n   총 {created_count}개 카테고리 생성 완료")
    else:
        print("   모든 카테고리가 이미 존재합니다.")

def create_test_users(db):
    """테스트 사용자 생성"""
    print("\n👥 테스트 사용자 생성 중...")

    test_users = [
        {
            "email": "test@test.com",
            "username": "test",
            "nickname": "테스트유저",
            "password": "test",
            "role": UserRole.USER
        },
        {
            "email": "korean@test.com",
            "username": "korean_user",
            "nickname": "한국인",
            "password": "test1234",
            "preferred_lang": Language.KO,
            "role": UserRole.USER
        },
        {
            "email": "russian@test.com",
            "username": "russian_user",
            "nickname": "Русский",
            "password": "test1234",
            "preferred_lang": Language.RU,
            "role": UserRole.USER
        }
    ]

    created_count = 0
    for user_data in test_users:
        # 기존 사용자 확인
        existing = db.query(User).filter(User.username == user_data["username"]).first()
        if existing:
            print(f"   ⚠️  사용자 '{user_data['username']}'이(가) 이미 존재합니다.")
            continue

        password = user_data.pop("password")
        user = User(
            **user_data,
            password_hash=pwd_context.hash(password),
            oauth_provider=OAuthProvider.EMAIL,
            is_active=True,
            is_verified=True,
            email_verified_at=datetime.utcnow(),
            created_at=datetime.utcnow()
        )

        db.add(user)
        created_count += 1
        print(f"   ✅ {user_data['username']} / {user_data['nickname']}")

    if created_count > 0:
        db.commit()
        print(f"\n   총 {created_count}명 테스트 사용자 생성 완료")

def create_sample_partners(db):
    """샘플 파트너 생성"""
    print("\n🤝 샘플 파트너 생성 중...")

    partners_data = [
        {
            "name_ko": "러시아 레스토랑",
            "name_ru": "Русский ресторан",
            "category": PartnerCategory.RESTAURANT,
            "description_ko": "정통 러시아 음식을 맛볼 수 있는 레스토랑",
            "description_ru": "Аутентичная русская кухня",
            "address_ko": "서울시 강남구 테헤란로 123",
            "address_ru": "Сеул, Каннам-гу, Тэхеран-ро 123",
            "phone": "02-1234-5678",
            "is_featured": True,
            "sort_order": 1
        },
        {
            "name_ko": "러시아어 학원",
            "name_ru": "Школа русского языка",
            "category": PartnerCategory.EDUCATION,
            "description_ko": "원어민 강사와 함께하는 러시아어 교육",
            "description_ru": "Обучение русскому языку с носителями",
            "address_ko": "서울시 서초구 강남대로 456",
            "address_ru": "Сеул, Сочо-гу, Каннам-дэро 456",
            "phone": "02-2345-6789",
            "is_featured": True,
            "sort_order": 2
        }
    ]

    created_count = 0
    for partner_data in partners_data:
        # 기존 파트너 확인
        existing = db.query(Partner).filter(
            Partner.name_ko == partner_data["name_ko"]
        ).first()
        if existing:
            print(f"   ⚠️  파트너 '{partner_data['name_ko']}'이(가) 이미 존재합니다.")
            continue

        partner = Partner(**partner_data)
        db.add(partner)
        created_count += 1
        print(f"   ✅ {partner_data['name_ko']} / {partner_data['name_ru']}")

    if created_count > 0:
        db.commit()
        print(f"\n   총 {created_count}개 파트너 생성 완료")

def main():
    parser = argparse.ArgumentParser(description='초기 데이터 생성 스크립트')
    parser.add_argument('--test-data', action='store_true', help='테스트 데이터도 함께 생성')
    parser.add_argument('--minimal', action='store_true', help='최소 데이터만 생성 (관리자 + 카테고리)')
    args = parser.parse_args()

    print("="*60)
    print("  KRU Community - 초기 데이터 생성")
    print("="*60)

    try:
        db = get_db_session()

        # 필수 데이터
        admin = create_admin_user(db)
        create_categories(db)

        # 선택 데이터
        if not args.minimal:
            if args.test_data:
                create_test_users(db)
                create_sample_partners(db)

        print("\n" + "="*60)
        print("  ✅ 초기 데이터 생성 완료!")
        print("="*60)
        print("\n📌 생성된 계정:")
        print(f"   관리자: admin1234 / kuro##@@")

        if args.test_data:
            print(f"   테스트: test / test")
            print(f"   한국인: korean_user / test1234")
            print(f"   러시아인: russian_user / test1234")

        print("\n🌐 접속 정보:")
        print("   사이트: http://localhost:3000")
        print("   관리자: http://localhost:3000/admin.html")
        print("   pgAdmin: http://localhost:5050")
        print(f"   - Email: admin@russki.center")
        print(f"   - Password: admin1234")

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    main()
