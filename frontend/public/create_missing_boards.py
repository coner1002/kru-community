#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
누락된 게시판 HTML 페이지를 board-free.html 템플릿으로부터 생성
"""
import sys
import io
import os
import re

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 생성할 게시판 목록 (slug, 한국어명, 러시아어명)
BOARDS_TO_CREATE = [
    ("business", "비즈니스", "Бизнес"),
    ("partners", "입점업체", "Партнерские компании"),
    ("trade", "무역파트너", "Торговые партнеры"),
    ("contact", "운영자 연락", "Связаться с администрацией"),
    ("ad", "광고 및 협력 요청", "Реклама и сотрудничество"),
    ("suggest", "운영자에게 건의", "Предложения администрации"),
]

def create_board_page(template_path, slug, name_ko, name_ru):
    """템플릿으로부터 새 게시판 페이지 생성"""

    # 템플릿 읽기
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # CURRENT_SLUG 변경
    content = re.sub(
        r"const CURRENT_SLUG = '[^']*';",
        f"const CURRENT_SLUG = '{slug}';",
        content
    )

    # 페이지 제목 변경 (head의 title 태그)
    content = re.sub(
        r'<title>[^<]*</title>',
        f'<title>{name_ko} - Russian.Town</title>',
        content
    )

    # 페이지 헤더 변경 (게시판 제목)
    content = re.sub(
        r'<div class="board-header-title">\s*<span class="korean-text">[^<]*</span>\s*<div class="russian-text">[^<]*</div>',
        f'<div class="board-header-title">\n                    <span class="korean-text">{name_ko}</span>\n                    <div class="russian-text">{name_ru}</div>',
        content
    )

    # 새 파일 저장
    output_path = os.path.join(os.path.dirname(template_path), f'board-{slug}.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return output_path

def main():
    template_path = 'board-free.html'

    if not os.path.exists(template_path):
        print(f'✗ 템플릿 파일을 찾을 수 없습니다: {template_path}')
        return

    print('=' * 80)
    print('누락된 게시판 페이지 생성 시작')
    print('=' * 80)

    created_count = 0

    for slug, name_ko, name_ru in BOARDS_TO_CREATE:
        output_file = f'board-{slug}.html'

        if os.path.exists(output_file):
            print(f'○ 스킵: {output_file} (이미 존재)')
            continue

        try:
            output_path = create_board_page(template_path, slug, name_ko, name_ru)
            print(f'✓ 생성: {output_file}')
            created_count += 1
        except Exception as e:
            print(f'✗ 오류: {output_file} - {e}')

    print('=' * 80)
    print(f'✓ 완료: {created_count}개 페이지 생성')
    print('=' * 80)

if __name__ == '__main__':
    main()
