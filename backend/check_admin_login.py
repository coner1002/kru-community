#!/usr/bin/env python3
"""
admin1@russian.town 계정 확인 및 생성
"""
import sys
import os

# 상위 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.user import User, UserRole
from app.core.security import get_password_hash, verify_password

db: Session = SessionLocal()

try:
    # admin1@russian.town 계정 확인
    admin = db.query(User).filter(User.email == "admin1@russian.town").first()

    if not admin:
        print("admin1@russian.town 계정이 없습니다. 생성합니다...")
        new_admin = User(
            email="admin1@russian.town",
            username="admin1",
            nickname="관리자1",
            nickname_ko="관리자1",
            nickname_ru="Администратор1",
            password_hash=get_password_hash("admin1234"),
            role=UserRole.ADMIN,
            is_verified=True,
            is_active=True,
            user_type='REAL'
        )
        db.add(new_admin)
        db.commit()
        print("admin1@russian.town 계정 생성 완료!")
        print("이메일: admin1@russian.town")
        print("비밀번호: admin1234")
    else:
        print(f"admin1@russian.town 계정 정보:")
        print(f"  ID: {admin.id}")
        print(f"  이메일: {admin.email}")
        print(f"  닉네임: {admin.nickname}")
        print(f"  역할: {admin.role}")
        print(f"  활성화: {admin.is_active}")
        print(f"  인증됨: {admin.is_verified}")

        # 비밀번호 테스트
        if verify_password("admin1234", admin.password_hash):
            print(f"  비밀번호: admin1234 (확인됨)")
        else:
            print(f"  비밀번호: admin1234로 재설정합니다...")
            admin.password_hash = get_password_hash("admin1234")
            db.commit()
            print("  비밀번호 재설정 완료!")

except Exception as e:
    print(f"오류 발생: {e}")
    db.rollback()
finally:
    db.close()
