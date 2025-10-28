#!/usr/bin/env python3
"""
카테고리 권한 설정 스크립트
각 게시판의 읽기/쓰기/댓글 권한을 설정합니다.
"""
import sys
from pathlib import Path

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.db.database import get_db
from app.models.post import Category, PermissionLevel
from sqlalchemy import select

def update_category_permissions():
    """카테고리 권한 업데이트"""

    # 카테고리별 권한 설정
    # 형식: {slug: (read, write, comment)}
    permissions = {
        # 공지사항: 모두 읽기, 스탭 쓰기, 일반회원 댓글
        'notice': (PermissionLevel.ALL, PermissionLevel.STAFF, PermissionLevel.USER),

        # 자유게시판/생활정보/행정정보/구인구직/벼룩시장: 일반회원 읽기/쓰기/댓글
        'free': (PermissionLevel.USER, PermissionLevel.USER, PermissionLevel.USER),
        'life': (PermissionLevel.USER, PermissionLevel.USER, PermissionLevel.USER),
        'admin': (PermissionLevel.USER, PermissionLevel.USER, PermissionLevel.USER),
        'job': (PermissionLevel.USER, PermissionLevel.USER, PermissionLevel.USER),
        'market': (PermissionLevel.USER, PermissionLevel.USER, PermissionLevel.USER),

        # 창업정보: 특별회원 읽기, 스탭 쓰기, 특별회원 댓글
        'startup': (PermissionLevel.PREMIUM, PermissionLevel.STAFF, PermissionLevel.PREMIUM),

        # 입점업체/무역파트너: 특별회원 읽기/쓰기/댓글
        'partners': (PermissionLevel.PREMIUM, PermissionLevel.PREMIUM, PermissionLevel.PREMIUM),
        'trade': (PermissionLevel.PREMIUM, PermissionLevel.PREMIUM, PermissionLevel.PREMIUM),

        # 광고 및 협력 요청: 관리자만 읽기, 일반회원 쓰기, 댓글 없음
        'ad': (PermissionLevel.ADMIN, PermissionLevel.USER, PermissionLevel.ADMIN),

        # 운영자에게 건의: 관리자만 읽기, 일반회원 쓰기, 댓글 없음
        'suggest': (PermissionLevel.ADMIN, PermissionLevel.USER, PermissionLevel.ADMIN),
    }

    db = next(get_db())

    try:
        updated_count = 0
        not_found_count = 0

        for slug, (read_perm, write_perm, comment_perm) in permissions.items():
            # 카테고리 찾기
            result = db.execute(
                select(Category).where(Category.slug == slug)
            )
            category = result.scalar_one_or_none()

            if not category:
                print(f"[SKIP] {slug} - 카테고리를 찾을 수 없습니다")
                not_found_count += 1
                continue

            # 권한 업데이트
            category.read_permission = read_perm
            category.write_permission = write_perm
            category.comment_permission = comment_perm

            print(f"[OK] {slug} ({category.name_ko})")
            print(f"     읽기: {read_perm.value}, 쓰기: {write_perm.value}, 댓글: {comment_perm.value}")
            updated_count += 1

        db.commit()

        print(f"\n=== 결과 ===")
        print(f"업데이트됨: {updated_count}개")
        print(f"찾을 수 없음: {not_found_count}개")
        print(f"총: {len(permissions)}개")

        print("\n=== 권한 설정 요약 ===")
        print("\n일반 게시판 (일반회원 읽기/쓰기/댓글):")
        print("  - 자유게시판, 생활정보, 행정정보, 구인구직, 벼룩시장")

        print("\n제한 게시판 (특별회원):")
        print("  - 창업정보: 특별회원 읽기, 스탭 쓰기, 특별회원 댓글")
        print("  - 입점업체: 특별회원 읽기/쓰기/댓글")
        print("  - 무역파트너: 특별회원 읽기/쓰기/댓글")

        print("\n관리자 전용 게시판:")
        print("  - 공지사항: 모두 읽기, 스탭 쓰기, 일반회원 댓글")
        print("  - 광고 및 협력 요청: 관리자만 읽기, 일반회원 쓰기")
        print("  - 운영자에게 건의: 관리자만 읽기, 일반회원 쓰기")

    except Exception as e:
        print(f"[ERROR] 오류 발생: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    update_category_permissions()
