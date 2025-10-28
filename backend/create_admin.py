"""관리자 계정 생성 스크립트"""
import sys
import os
import io

# Windows 콘솔 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.append(os.path.dirname(__file__))

from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.user import User, UserRole
from app.core.security import get_password_hash
from datetime import datetime

def create_admin():
    """관리자 계정 생성"""
    db: Session = SessionLocal()

    try:
        # 기존 관리자 확인
        admin_count = db.query(User).filter(User.role == UserRole.ADMIN).count()

        if admin_count > 0:
            print(f"ℹ️  이미 {admin_count}명의 관리자가 있습니다.")
            print("\n기존 관리자 목록:")
            admins = db.query(User).filter(User.role == UserRole.ADMIN).all()
            for admin in admins:
                print(f"  - Email: {admin.email}, Nickname: {admin.nickname}")

            choice = input("\n새 관리자를 추가하시겠습니까? (y/n): ").lower()
            if choice != 'y':
                print("취소되었습니다.")
                return

        print("\n=== 관리자 계정 생성 ===")

        # 이메일 입력
        email = input("이메일: ").strip()

        # 이메일 중복 확인
        existing_user = db.query(User).filter(User.email == email).first()

        if existing_user:
            print(f"\n⚠️  이미 존재하는 계정입니다: {existing_user.email}")
            choice = input("이 계정을 관리자로 승격하시겠습니까? (y/n): ").lower()

            if choice == 'y':
                existing_user.role = UserRole.ADMIN
                db.commit()
                print(f"✅ {existing_user.email} 계정이 관리자로 승격되었습니다!")
            else:
                print("취소되었습니다.")
            return

        # 새 관리자 계정 생성
        nickname = input("닉네임: ").strip()
        password = input("비밀번호: ").strip()

        # 비밀번호 확인
        password_confirm = input("비밀번호 확인: ").strip()
        if password != password_confirm:
            print("❌ 비밀번호가 일치하지 않습니다.")
            return

        # 관리자 계정 생성
        admin_user = User(
            email=email,
            nickname=nickname,
            password_hash=get_password_hash(password),
            role=UserRole.ADMIN,
            is_active=True,
            is_verified=True,
            email_verified_at=datetime.utcnow(),
            oauth_provider='EMAIL',
            preferred_lang='ko',
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        print("\n✅ 관리자 계정이 생성되었습니다!")
        print(f"   Email: {admin_user.email}")
        print(f"   Nickname: {admin_user.nickname}")
        print(f"   Role: {admin_user.role}")
        print("\n이제 이 계정으로 로그인하여 관리자 페이지(/admin.html)에 접속할 수 있습니다.")

    except Exception as e:
        db.rollback()
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    print("관리자 계정 생성 도구\n")
    create_admin()
