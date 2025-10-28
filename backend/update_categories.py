#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
카테고리 데이터베이스를 사용자가 원하는 13개 목록으로 업데이트
"""
import sys
import io

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from app.db.database import SessionLocal
from app.models.post import Category, CategoryLayoutType, CategoryPermission

# 사용자가 원하는 최종 카테고리 목록
DESIRED_CATEGORIES = [
    # 게시판 섹션
    {"sort_order": 1, "slug": "notice", "name_ko": "공지사항", "name_ru": "Объявления", "icon": "📢", "layout_type": "list", "permission": "read_all"},
    {"sort_order": 2, "slug": "free", "name_ko": "자유게시판", "name_ru": "Свободное общение", "icon": "💬", "layout_type": "list", "permission": "read_all"},
    {"sort_order": 3, "slug": "life", "name_ko": "생활정보", "name_ru": "Жизнь в Корее", "icon": "🏠", "layout_type": "list", "permission": "read_all"},
    {"sort_order": 4, "slug": "admin", "name_ko": "행정정보", "name_ru": "Админ. информация", "icon": "📋", "layout_type": "list", "permission": "read_all"},
    {"sort_order": 5, "slug": "job", "name_ko": "구인구직", "name_ru": "Работа", "icon": "💼", "layout_type": "list", "permission": "read_all"},
    {"sort_order": 6, "slug": "market", "name_ko": "벼룩시장", "name_ru": "Барахолка", "icon": "🛒", "layout_type": "gallery", "permission": "read_all"},

    # 비즈니스 섹션
    {"sort_order": 7, "slug": "business", "name_ko": "비즈니스", "name_ru": "Бизнес", "icon": "💼", "layout_type": "list", "permission": "read_all"},
    {"sort_order": 8, "slug": "startup", "name_ko": "창업정보", "name_ru": "Информация о стартапах", "icon": "🚀", "layout_type": "list", "permission": "read_all"},
    {"sort_order": 9, "slug": "partners", "name_ko": "입점업체", "name_ru": "Партнерские компании", "icon": "🏢", "layout_type": "card", "permission": "read_all"},
    {"sort_order": 10, "slug": "trade", "name_ko": "무역파트너", "name_ru": "Торговые партнеры", "icon": "🌐", "layout_type": "card", "permission": "read_all"},

    # 운영자 연락 섹션
    {"sort_order": 11, "slug": "contact", "name_ko": "운영자 연락", "name_ru": "Связаться с администрацией", "icon": "✉️", "layout_type": "list", "permission": "read_all"},
    {"sort_order": 12, "slug": "ad", "name_ko": "광고 및 협력 요청", "name_ru": "Реклама и сотрудничество", "icon": "📣", "layout_type": "list", "permission": "read_all"},
    {"sort_order": 13, "slug": "suggest", "name_ko": "운영자에게 건의", "name_ru": "Предложения администрации", "icon": "💡", "layout_type": "list", "permission": "read_all"},
]

def main():
    db = SessionLocal()

    try:
        print("=" * 80)
        print("카테고리 데이터베이스 업데이트 시작")
        print("=" * 80)

        # 기존 카테고리 모두 가져오기
        existing_categories = {cat.slug: cat for cat in db.query(Category).all()}

        updated_count = 0
        created_count = 0

        for cat_data in DESIRED_CATEGORIES:
            slug = cat_data["slug"]

            if slug in existing_categories:
                # 기존 카테고리 업데이트
                cat = existing_categories[slug]
                cat.name_ko = cat_data["name_ko"]
                cat.name_ru = cat_data["name_ru"]
                cat.icon = cat_data["icon"]
                cat.sort_order = cat_data["sort_order"]
                cat.layout_type = cat_data["layout_type"]
                cat.permission = cat_data["permission"]
                cat.is_active = True
                print(f"✓ 업데이트: {slug:15s} | {cat_data['name_ko']:20s} | {cat_data['name_ru']}")
                updated_count += 1
            else:
                # 새 카테고리 생성
                cat = Category(
                    slug=slug,
                    name_ko=cat_data["name_ko"],
                    name_ru=cat_data["name_ru"],
                    icon=cat_data["icon"],
                    sort_order=cat_data["sort_order"],
                    layout_type=cat_data["layout_type"],
                    permission=cat_data["permission"],
                    is_active=True
                )
                db.add(cat)
                print(f"+ 생성: {slug:15s} | {cat_data['name_ko']:20s} | {cat_data['name_ru']}")
                created_count += 1

        # 변경사항 저장
        db.commit()

        print("=" * 80)
        print(f"✓ 완료: {updated_count}개 업데이트, {created_count}개 생성")
        print("=" * 80)

        # 최종 결과 확인
        print("\n최종 카테고리 목록:")
        print("=" * 80)
        categories = db.query(Category).filter(Category.is_active == True).order_by(Category.sort_order).all()
        for cat in categories:
            print(f"[{cat.sort_order:2d}] {cat.slug:15s} | {cat.name_ko:20s} | {cat.name_ru}")
        print("=" * 80)
        print(f"총 {len(categories)}개 활성 카테고리")

    except Exception as e:
        db.rollback()
        print(f"✗ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    main()
