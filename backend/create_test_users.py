#!/usr/bin/env python3
"""
테스트 사용자 계정 생성 스크립트
각 권한 등급별로 2개씩 총 8개의 테스트 계정을 생성합니다.
"""
import asyncio
import sys
from pathlib import Path

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.db.database import get_db
from app.models.user import User, UserRole
from app.core.security import get_password_hash
from sqlalchemy import select

async def create_test_users():
    """테스트 사용자 계정 생성"""

    # 테스트 계정 정의
    test_users = [
        # 관리자 (Admin)
        {
            "email": "admin1@test.com",
            "username": "admin1",
            "nickname": "관리자1",
            "password": "admin1234",
            "role": UserRole.ADMIN,
            "is_verified": True
        },
        {
            "email": "admin2@test.com",
            "username": "admin2",
            "nickname": "관리자2",
            "password": "admin2234",
            "role": UserRole.ADMIN,
            "is_verified": True
        },
        # 스탭 (Staff)
        {
            "email": "staff1@test.com",
            "username": "staff1",
            "nickname": "스탭1",
            "password": "staff1234",
            "role": UserRole.STAFF,
            "is_verified": True
        },
        {
            "email": "staff2@test.com",
            "username": "staff2",
            "nickname": "스탭2",
            "password": "staff2234",
            "role": UserRole.STAFF,
            "is_verified": True
        },
        # 특별회원 (Premium)
        {
            "email": "premium1@test.com",
            "username": "premium1",
            "nickname": "특별회원1",
            "password": "premium1234",
            "role": UserRole.PREMIUM,
            "is_verified": True
        },
        {
            "email": "premium2@test.com",
            "username": "premium2",
            "nickname": "특별회원2",
            "password": "premium2234",
            "role": UserRole.PREMIUM,
            "is_verified": True
        },
        # 일반회원 (User)
        {
            "email": "user1@test.com",
            "username": "user1",
            "nickname": "일반회원1",
            "password": "user1234",
            "role": UserRole.USER,
            "is_verified": True
        },
        {
            "email": "user2@test.com",
            "username": "user2",
            "nickname": "일반회원2",
            "password": "user2234",
            "role": UserRole.USER,
            "is_verified": True
        }
    ]

    db = next(get_db())

    try:
        created_count = 0
        skipped_count = 0

        for user_data in test_users:
            # 이미 존재하는 사용자인지 확인
            result = db.execute(
                select(User).where(User.email == user_data["email"])
            )
            existing_user = result.scalar_one_or_none()

            if existing_user:
                print(f"[SKIP] {user_data['email']} - 이미 존재하는 계정입니다")
                skipped_count += 1
                continue

            # 새 사용자 생성
            new_user = User(
                email=user_data["email"],
                username=user_data["username"],
                nickname=user_data["nickname"],
                password_hash=get_password_hash(user_data["password"]),
                role=user_data["role"],
                is_verified=user_data["is_verified"],
                is_active=True
            )

            db.add(new_user)
            db.commit()

            print(f"[OK] {user_data['email']} ({user_data['role']}) - 계정 생성 완료")
            created_count += 1

        print(f"\n=== 결과 ===")
        print(f"생성됨: {created_count}개")
        print(f"건너뜀: {skipped_count}개")
        print(f"총: {len(test_users)}개")

        if created_count > 0:
            print("\n=== 테스트 계정 정보 ===")
            print("\n관리자 (Admin):")
            print("  admin1@test.com / admin1234")
            print("  admin2@test.com / admin2234")
            print("\n스탭 (Staff):")
            print("  staff1@test.com / staff1234")
            print("  staff2@test.com / staff2234")
            print("\n특별회원 (Premium):")
            print("  premium1@test.com / premium1234")
            print("  premium2@test.com / premium2234")
            print("\n일반회원 (User):")
            print("  user1@test.com / user1234")
            print("  user2@test.com / user2234")

    except Exception as e:
        print(f"[ERROR] 오류 발생: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(create_test_users())
