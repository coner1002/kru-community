"""
기존 회원들의 닉네임을 자동으로 음역하는 스크립트
"""
import sys
import os

# 상위 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.user import User
from app.utils.transliteration import transliterate_nickname


def transliterate_all_users():
    """모든 회원의 닉네임을 음역"""
    db: Session = SessionLocal()

    try:
        # 모든 회원 조회
        users = db.query(User).all()
        updated_count = 0

        print(f"총 {len(users)}명의 회원을 처리합니다...")

        for user in users:
            # nickname이 있는 경우 무조건 다시 음역
            if user.nickname:
                nickname_ko, nickname_ru = transliterate_nickname(user.nickname)

                # 기존 값과 다른 경우에만 업데이트
                if user.nickname_ko != nickname_ko or user.nickname_ru != nickname_ru:
                    user.nickname_ko = nickname_ko
                    user.nickname_ru = nickname_ru
                    print(f"ID {user.id}: {user.nickname} → KO: {nickname_ko}, RU: {nickname_ru}")
                    updated_count += 1
                else:
                    print(f"ID {user.id}: {user.nickname} - 이미 올바르게 음역됨")

        # 변경사항 저장
        db.commit()
        print(f"\n완료! {updated_count}명의 회원 닉네임을 업데이트했습니다.")

    except Exception as e:
        print(f"오류 발생: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    transliterate_all_users()
