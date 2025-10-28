#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
데이터베이스 상태 확인 스크립트
"""
import sys
import os

# 환경 변수 설정
os.environ.setdefault('DATABASE_URL', 'sqlite:///./backend/kru_community.db')
os.environ.setdefault('REDIS_URL', 'redis://localhost:6379/0')
os.environ.setdefault('SECRET_KEY', 'dev-secret-key')

# backend 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from app.db.database import SessionLocal
    from app.models.post import Category, Post

    # 데이터베이스 세션 생성
    db = SessionLocal()

    print("=" * 60)
    print("Database Connection Status Check")
    print("=" * 60)

    # 카테고리 확인
    print("\n[Category List]")
    categories = db.query(Category).all()
    if categories:
        for cat in categories:
            print(f"  ID: {cat.id}, Slug: {cat.slug}, Korean: {cat.name_ko}, Russian: {cat.name_ru}")
    else:
        print("  ! No categories found!")

    # 게시글 통계
    print("\n[Posts per Category]")
    for cat in categories:
        count = db.query(Post).filter(Post.category_id == cat.id).count()
        print(f"  {cat.name_ko} ({cat.slug}): {count} posts")

    # 전체 게시글 수
    total_posts = db.query(Post).count()
    print(f"\nTotal posts: {total_posts}")

    # 최근 게시글 5개
    print("\n[Recent 5 Posts]")
    recent_posts = db.query(Post).order_by(Post.created_at.desc()).limit(5).all()
    for post in recent_posts:
        title_preview = post.title[:40] if len(post.title) <= 40 else post.title[:37] + "..."
        print(f"  #{post.id}: {title_preview} (Category ID: {post.category_id})")

    db.close()
    print("\nDatabase check completed successfully!")

except Exception as e:
    print(f"\nError occurred: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
