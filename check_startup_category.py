import psycopg2
from psycopg2.extras import RealDictCursor

# 데이터베이스 연결
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="kru_community",
    user="kru_user",
    password="kru_pass"
)

try:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        # startup 카테고리 확인
        cursor.execute("""
            SELECT id, slug, name_ko, name_ru, is_active, is_group, sort_order, parent_id
            FROM categories
            WHERE slug = 'startup'
        """)
        startup = cursor.fetchone()

        if startup:
            print("[OK] startup 카테고리 발견:")
            print(f"  - ID: {startup['id']}")
            print(f"  - 한글명: {startup['name_ko']}")
            print(f"  - 러시아어명: {startup['name_ru']}")
            print(f"  - 활성화: {startup['is_active']}")
            print(f"  - 그룹 헤더: {startup['is_group']}")
            print(f"  - 정렬 순서: {startup['sort_order']}")
            print(f"  - 상위 카테고리 ID: {startup['parent_id']}")

            # startup 카테고리의 게시글 수 확인
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM posts
                WHERE category_id = %s
            """, (startup['id'],))
            post_count = cursor.fetchone()
            print(f"  - 게시글 수: {post_count['count']}")

        else:
            print("[오류] startup 카테고리가 데이터베이스에 없습니다!")
            print("\n모든 카테고리 목록:")
            cursor.execute("SELECT slug, name_ko, is_active FROM categories ORDER BY sort_order")
            categories = cursor.fetchall()
            for cat in categories:
                print(f"  - {cat['slug']}: {cat['name_ko']} (활성화: {cat['is_active']})")

finally:
    conn.close()
