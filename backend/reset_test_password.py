#!/usr/bin/env python3
"""테스트 사용자 비밀번호 재설정"""

from app.db.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def reset_password():
    db = SessionLocal()
    try:
        # test@example.com 사용자 찾기
        user = db.query(User).filter(User.email == "test@example.com").first()

        if not user:
            print("❌ 사용자를 찾을 수 없습니다.")
            return

        print(f"✅ 사용자 발견: {user.email} (username: {user.username})")

        # 비밀번호를 Test1234로 재설정
        new_password = "Test1234"
        user.password_hash = get_password_hash(new_password)

        db.commit()

        print(f"✅ 비밀번호가 '{new_password}'로 재설정되었습니다.")
        print(f"   - Email: {user.email}")
        print(f"   - Username: {user.username}")
        print(f"   - Role: {user.role}")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    reset_password()
