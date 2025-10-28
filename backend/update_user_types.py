"""
기존 회원들의 user_type을 자동으로 분류하는 스크립트
- ADMIN role -> user_type = 'admin'
- STAFF role -> user_type = 'staff'
- 나머지 -> user_type = 'virtual' (분위기 조성용 가상 회원)
"""
import sys
import os

# UTF-8 인코딩 설정
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 데이터베이스 연결
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def update_user_types():
    db = SessionLocal()
    try:
        # 먼저 현재 회원 role 분포 확인
        print("\n현재 회원 role 분포:")
        result = db.execute(text("SELECT role, COUNT(*) as count FROM users GROUP BY role"))
        for row in result:
            print(f"  {row[0]}: {row[1]}명")

        # 1. ADMIN role을 가진 사용자 -> user_type = 'admin'
        result = db.execute(
            text("UPDATE users SET user_type = 'admin' WHERE role = 'admin' OR role = 'ADMIN'")
        )
        admin_count = result.rowcount
        print(f"\n✅ ADMIN 권한 회원 {admin_count}명 -> user_type = 'admin'")

        # 2. STAFF role을 가진 사용자 -> user_type = 'staff'
        result = db.execute(
            text("UPDATE users SET user_type = 'staff' WHERE role = 'staff' OR role = 'STAFF'")
        )
        staff_count = result.rowcount
        print(f"✅ STAFF 권한 회원 {staff_count}명 -> user_type = 'staff'")

        # 3. 나머지 (PREMIUM, USER) -> user_type = 'virtual'
        result = db.execute(
            text("UPDATE users SET user_type = 'virtual' WHERE (role = 'premium' OR role = 'PREMIUM' OR role = 'user' OR role = 'USER') AND (user_type IS NULL OR user_type = 'real')")
        )
        virtual_count = result.rowcount
        print(f"✅ 일반/프리미엄 회원 {virtual_count}명 -> user_type = 'virtual' (관리 가상회원)")

        db.commit()
        print("\n" + "="*50)
        print("✅ 회원 유형 분류 완료!")
        print("="*50)
        print(f"총 {admin_count + staff_count + virtual_count}명 업데이트")

        # 결과 확인
        print("\n현재 회원 유형 분포:")
        result = db.execute(text("""
            SELECT user_type, COUNT(*) as count
            FROM users
            GROUP BY user_type
        """))
        for row in result:
            type_labels = {
                'admin': '관리자',
                'staff': '스탭',
                'virtual': '관리 가상회원',
                'real': '실제 가입회원'
            }
            label = type_labels.get(row[0], row[0])
            print(f"  {label}: {row[1]}명")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("회원 유형 자동 분류 시작...")
    print("="*50)
    update_user_types()
