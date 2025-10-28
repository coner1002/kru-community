"""
가상회원들의 비밀번호를 통일된 비밀번호로 변경하는 스크립트
"""
import sys
import os

# 상위 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash


def reset_virtual_passwords(new_password: str = "virtual1234"):
    """모든 가상회원의 비밀번호를 통일"""
    db: Session = SessionLocal()

    try:
        # 가상회원 조회
        virtual_users = db.query(User).filter(User.user_type == 'VIRTUAL').all()

        print(f"총 {len(virtual_users)}명의 가상회원을 처리합니다...")
        print(f"새 비밀번호: {new_password}")
        print()

        if len(virtual_users) == 0:
            print("가상회원이 없습니다.")
            return

        # 비밀번호 해시 생성
        hashed_password = get_password_hash(new_password)

        # 모든 가상회원의 비밀번호 업데이트
        for user in virtual_users:
            user.password_hash = hashed_password
            print(f"ID {user.id}: {user.nickname} ({user.email}) - 비밀번호 변경")

        # 변경사항 저장
        db.commit()
        print(f"\n완료! {len(virtual_users)}명의 가상회원 비밀번호를 '{new_password}'로 변경했습니다.")

        # 로그인 정보 출력
        print("\n=== 가상회원 로그인 정보 ===")
        print(f"비밀번호: {new_password}")
        print("\n이메일 목록:")
        for user in virtual_users[:10]:  # 처음 10개만 출력
            print(f"  - {user.email}")
        if len(virtual_users) > 10:
            print(f"  ... 외 {len(virtual_users) - 10}명")

    except Exception as e:
        print(f"오류 발생: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    # 원하는 비밀번호를 여기서 설정
    NEW_PASSWORD = "virtual1234"

    confirm = input(f"모든 가상회원의 비밀번호를 '{NEW_PASSWORD}'로 변경하시겠습니까? (yes/no): ")

    if confirm.lower() == 'yes':
        reset_virtual_passwords(NEW_PASSWORD)
    else:
        print("취소되었습니다.")
