"""
초기 회원 데이터 생성 스크립트
- 관리자 2명
- 스탭 3명
- 가상회원 100명 (한국인 20명, 교포 60명, 러시아인 20명)
"""
import sys
import os
import random
import json

# UTF-8 인코딩 설정
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User

# 데이터베이스 연결
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# 한국인 이름 풀
KOREAN_SURNAMES = ["김", "이", "박", "최", "정", "강", "조", "윤", "장", "임", "한", "오", "서", "신", "권", "황", "안", "송", "류", "홍"]
KOREAN_NAMES_MALE = ["민준", "서준", "예준", "도윤", "시우", "주원", "하준", "지호", "준서", "건우", "현우", "우진", "승현", "지훈", "승우"]
KOREAN_NAMES_FEMALE = ["서연", "민서", "지우", "서현", "지민", "예은", "수아", "하은", "윤서", "지유", "다은", "채원", "예린", "지안", "수빈"]

# 고려인(교포) 이름 풀 - 러시아식 발음의 한국 이름
KORYO_SURNAMES = ["김", "박", "리", "최", "정", "강", "한", "남", "조", "전"]
KORYO_NAMES_MALE = ["빅토르", "세르게이", "알렉산드르", "표트르", "이반", "미하일", "안드레이", "니콜라이", "드미트리", "파벨", "유리", "올레그", "블라디미르", "게오르기", "보리스"]
KORYO_NAMES_FEMALE = ["타티아나", "마리아", "옐레나", "이리나", "스베틀라나", "올가", "나탈리야", "안나", "베라", "류드밀라", "갈리나", "라리사", "발렌티나", "니나", "소피아"]

# 러시아인 이름 풀
RUSSIAN_NAMES_MALE = ["Александр", "Дмитрий", "Иван", "Михаил", "Сергей", "Андрей", "Алексей", "Артём", "Владимир", "Максим", "Павел", "Николай", "Денис", "Егор", "Кирилл"]
RUSSIAN_NAMES_FEMALE = ["Мария", "Анна", "Елена", "Ольга", "Татьяна", "Наталья", "Екатерина", "Ирина", "Светлана", "Юлия", "Анастасия", "София", "Виктория", "Дарья", "Алиса"]
RUSSIAN_SURNAMES = ["Иванов", "Смирнов", "Кузнецов", "Попов", "Соколов", "Лебедев", "Козлов", "Новиков", "Морозов", "Петров", "Волков", "Соловьев", "Васильев", "Зайцев", "Павлов"]

# 직업 풀
OCCUPATIONS_KO = ["회사원", "자영업", "프리랜서", "학생", "교사", "디자이너", "개발자", "마케터", "연구원", "의사", "변호사", "공무원", "요리사", "작가", "번역가"]
OCCUPATIONS_RU = ["Программист", "Менеджер", "Дизайнер", "Учитель", "Врач", "Инженер", "Бизнесмен", "Переводчик", "Фотограф", "Консультант", "Студент", "Юрист", "Повар", "Писатель", "Продавец"]

# 관심사 풀
INTERESTS_KO = ["여행", "음식", "사진", "독서", "운동", "음악", "영화", "게임", "요리", "언어학습", "비즈니스", "IT기술", "패션", "건강", "문화교류"]
INTERESTS_RU = ["Путешествия", "Кулинария", "Фотография", "Чтение", "Спорт", "Музыка", "Кино", "Игры", "Программирование", "Языки", "Бизнес", "Мода", "Культура", "Искусство", "История"]

# 게시 스타일
POSTING_STYLES = ["정보공유형", "질문형", "경험담형", "조언형", "유머형", "진지형", "친근형", "전문가형", "초보형", "활발형"]

def create_korean_nickname():
    """한국인 닉네임 생성"""
    surname = random.choice(KOREAN_SURNAMES)
    is_male = random.choice([True, False])
    name = random.choice(KOREAN_NAMES_MALE if is_male else KOREAN_NAMES_FEMALE)
    return surname + name, "male" if is_male else "female"

def create_koryo_nickname():
    """고려인 닉네임 생성"""
    surname = random.choice(KORYO_SURNAMES)
    is_male = random.choice([True, False])
    name = random.choice(KORYO_NAMES_MALE if is_male else KORYO_NAMES_FEMALE)
    return f"{surname}{name}", "male" if is_male else "female"

def create_russian_nickname():
    """러시아인 닉네임 생성"""
    is_male = random.choice([True, False])
    name = random.choice(RUSSIAN_NAMES_MALE if is_male else RUSSIAN_NAMES_FEMALE)
    surname = random.choice(RUSSIAN_SURNAMES)
    return f"{name} {surname}", "male" if is_male else "female"

def create_persona_data(ethnicity, gender):
    """페르소나 데이터 생성"""
    if ethnicity == "korean":
        occupation = random.choice(OCCUPATIONS_KO)
        interests = random.sample(INTERESTS_KO, k=random.randint(3, 6))
        korean_level = random.choice(["native", "fluent"])
        russian_level = random.choice(["basic", "intermediate", "advanced"])
    elif ethnicity == "korean_russian":
        occupation = random.choice(OCCUPATIONS_RU + OCCUPATIONS_KO)
        interests = random.sample(INTERESTS_KO + INTERESTS_RU, k=random.randint(3, 6))
        korean_level = random.choice(["intermediate", "advanced", "fluent"])
        russian_level = random.choice(["fluent", "native"])
    else:  # russian
        occupation = random.choice(OCCUPATIONS_RU)
        interests = random.sample(INTERESTS_RU, k=random.randint(3, 6))
        korean_level = random.choice(["beginner", "basic", "intermediate"])
        russian_level = random.choice(["native", "fluent"])

    return {
        "age": random.randint(22, 55),
        "occupation": occupation,
        "interests": json.dumps(interests, ensure_ascii=False),
        "activity_level": random.choice(["high", "medium", "low"]),
        "posting_style": random.choice(POSTING_STYLES),
        "korean_level": korean_level,
        "russian_level": russian_level
    }

def main():
    db = SessionLocal()
    try:
        print("="*60)
        print("초기 회원 데이터 생성 시작")
        print("="*60)

        created_count = 0

        # 1. 관리자 2명 생성
        print("\n[1] 관리자 2명 생성 중...")
        admin_names = [("김관리", "male"), ("박관리", "female")]
        for idx, (name, gender) in enumerate(admin_names, 1):
            user = User(
                email=f"admin{idx}@russian.town",
                nickname=name,
                password_hash=get_password_hash("admin1234"),
                role="ADMIN",
                user_type="admin",
                oauth_provider="email",
                preferred_lang="ko",
                is_active=True,
                is_verified=True
            )
            db.add(user)
            created_count += 1
            print(f"  ✅ 관리자 {idx}: {name}")

        # 2. 스탭 3명 생성
        print("\n[2] 스탭 3명 생성 중...")
        staff_names = [("이스탭", "male"), ("최스탭", "female"), ("정스탭", "male")]
        for idx, (name, gender) in enumerate(staff_names, 1):
            user = User(
                email=f"staff{idx}@russian.town",
                nickname=name,
                password_hash=get_password_hash("staff1234"),
                role="STAFF",
                user_type="staff",
                oauth_provider="email",
                preferred_lang="ko",
                is_active=True,
                is_verified=True
            )
            db.add(user)
            created_count += 1
            print(f"  ✅ 스탭 {idx}: {name}")

        # 3. 가상회원 100명 생성
        print("\n[3] 가상회원 100명 생성 중...")

        # 3-1. 한국인 20명
        print("  [3-1] 한국인 20명...")
        for i in range(20):
            nickname, gender = create_korean_nickname()
            persona = create_persona_data("korean", gender)
            user = User(
                email=f"korean{i+1}@virtual.russian.town",
                nickname=nickname,
                password_hash=get_password_hash("virtual1234"),
                role="USER",
                user_type="virtual",
                ethnicity="korean",
                persona_gender=gender,
                persona_age=persona["age"],
                persona_occupation=persona["occupation"],
                persona_interests=persona["interests"],
                persona_activity_level=persona["activity_level"],
                persona_posting_style=persona["posting_style"],
                persona_korean_level=persona["korean_level"],
                persona_russian_level=persona["russian_level"],
                oauth_provider="email",
                preferred_lang="ko",
                is_active=True,
                is_verified=True
            )
            db.add(user)
            created_count += 1
        print(f"    ✅ 한국인 20명 생성 완료")

        # 3-2. 고려인(교포) 60명
        print("  [3-2] 고려인(교포) 60명...")
        for i in range(60):
            nickname, gender = create_koryo_nickname()
            persona = create_persona_data("korean_russian", gender)
            user = User(
                email=f"koryo{i+1}@virtual.russian.town",
                nickname=nickname,
                password_hash=get_password_hash("virtual1234"),
                role="USER",
                user_type="virtual",
                ethnicity="korean_russian",
                persona_gender=gender,
                persona_age=persona["age"],
                persona_occupation=persona["occupation"],
                persona_interests=persona["interests"],
                persona_activity_level=persona["activity_level"],
                persona_posting_style=persona["posting_style"],
                persona_korean_level=persona["korean_level"],
                persona_russian_level=persona["russian_level"],
                oauth_provider="email",
                preferred_lang="ru",
                is_active=True,
                is_verified=True
            )
            db.add(user)
            created_count += 1
        print(f"    ✅ 고려인(교포) 60명 생성 완료")

        # 3-3. 러시아인 20명
        print("  [3-3] 러시아인 20명...")
        for i in range(20):
            nickname, gender = create_russian_nickname()
            persona = create_persona_data("russian", gender)
            user = User(
                email=f"russian{i+1}@virtual.russian.town",
                nickname=nickname,
                password_hash=get_password_hash("virtual1234"),
                role="USER",
                user_type="virtual",
                ethnicity="russian",
                persona_gender=gender,
                persona_age=persona["age"],
                persona_occupation=persona["occupation"],
                persona_interests=persona["interests"],
                persona_activity_level=persona["activity_level"],
                persona_posting_style=persona["posting_style"],
                persona_korean_level=persona["korean_level"],
                persona_russian_level=persona["russian_level"],
                oauth_provider="email",
                preferred_lang="ru",
                is_active=True,
                is_verified=True
            )
            db.add(user)
            created_count += 1
        print(f"    ✅ 러시아인 20명 생성 완료")

        # 커밋
        db.commit()

        print("\n" + "="*60)
        print(f"✅ 총 {created_count}명의 회원이 성공적으로 생성되었습니다!")
        print("="*60)
        print(f"  - 관리자: 2명")
        print(f"  - 스탭: 3명")
        print(f"  - 가상회원: 100명")
        print(f"    • 한국인: 20명")
        print(f"    • 고려인(교포): 60명")
        print(f"    • 러시아인: 20명")
        print("="*60)
        print("\n로그인 정보:")
        print("  관리자: admin1@russian.town / admin1234")
        print("  관리자: admin2@russian.town / admin1234")
        print("  스탭: staff1@russian.town / staff1234")
        print("  스탭: staff2@russian.town / staff1234")
        print("  스탭: staff3@russian.town / staff1234")

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
