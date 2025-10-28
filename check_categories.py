#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.db.database import SessionLocal
from app.models.post import Category

db = SessionLocal()
categories = db.query(Category).order_by(Category.sort_order).all()

print('현재 데이터베이스의 카테고리 목록:')
print('='*80)
for cat in categories:
    status = 'O' if cat.is_active else 'X'
    layout = cat.layout_type.value if hasattr(cat.layout_type, 'value') else str(cat.layout_type)
    perm = cat.permission.value if hasattr(cat.permission, 'value') else str(cat.permission)
    print(f'{status} [{cat.sort_order:2d}] {cat.slug:15s} | {cat.name_ko:20s} | {cat.name_ru}')
    print(f'     Layout: {layout:10s} Permission: {perm:15s}')
print('='*80)
print(f'총 {len(categories)}개 카테고리')

db.close()
