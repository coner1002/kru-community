"""
기존 회원의 nickname_ko와 nickname_ru 필드 채우기
- 한국인/교포: 닉네임을 nickname_ko에, 로마자 표기를 nickname_ru에
- 러시아인: 닉네임을 nickname_ru에, 영문 표기를 nickname_ko에
"""
import sys
import os

# UTF-8 인코딩 설정
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.user import User

# 데이터베이스 연결
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def main():
    db = SessionLocal()
    try:
        print("=" * 60)
        print("닉네임 필드 업데이트 시작")
        print("=" * 60)

        users = db.query(User).all()
        updated_count = 0

        for user in users:
            # 이미 nickname_ko와 nickname_ru가 설정된 경우 건너뛰기
            if user.nickname_ko and user.nickname_ru:
                continue

            # ethnicity에 따라 닉네임 분배
            if user.ethnicity == "korean":
                # 한국인: 한글 닉네임 → nickname_ko, 영문 표기 → nickname_ru
                user.nickname_ko = user.nickname
                user.nickname_ru = user.nickname  # 일단 같은 값으로 설정
            elif user.ethnicity == "korean_russian":
                # 교포: 한글 닉네임 → nickname_ko, 러시아식 표기 → nickname_ru
                user.nickname_ko = user.nickname
                user.nickname_ru = user.nickname  # 일단 같은 값으로 설정
            elif user.ethnicity == "russian":
                # 러시아인: 러시아 닉네임 → nickname_ru, 영문 표기 → nickname_ko
                user.nickname_ru = user.nickname
                user.nickname_ko = user.nickname  # 일단 같은 값으로 설정
            else:
                # ethnicity가 없는 경우 (관리자/스탭) - 양쪽 모두 설정
                user.nickname_ko = user.nickname
                user.nickname_ru = user.nickname

            updated_count += 1

        db.commit()

        print(f"\n✅ 총 {updated_count}명의 회원 닉네임 필드가 업데이트되었습니다!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
