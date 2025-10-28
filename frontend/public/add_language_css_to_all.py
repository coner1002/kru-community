#!/usr/bin/env python3
"""
모든 게시판 페이지에 언어 전환 CSS가 있는지 확인하고 없으면 추가
"""

import os
import re
from pathlib import Path

# 현재 디렉토리
CURRENT_DIR = Path(__file__).parent

# 모든 HTML 파일
ALL_FILES = (
    list(CURRENT_DIR.glob("board-*.html")) +
    list(CURRENT_DIR.glob("contact-*.html"))
)

EXCLUDE_FILES = ['board-write.html', 'board-view.html', 'board-job-old.html']

# 추가할 CSS
LANGUAGE_CSS = """
        /* 언어 전환 CSS */
        body[data-lang="ko"] .russian-text,
        body[data-lang="ko"] .russian-label,
        body[data-lang="ko"] .russian-subtitle,
        body[data-lang="ko"] .russian-title {
            display: none !important;
        }

        body[data-lang="ru"] .korean-text,
        body[data-lang="ru"] .korean-label,
        body[data-lang="ru"] .korean-subtitle,
        body[data-lang="ru"] .korean-title {
            display: none !important;
        }

        body[data-lang="both"] .russian-text,
        body[data-lang="both"] .russian-label,
        body[data-lang="both"] .korean-text,
        body[data-lang="both"] .korean-label {
            display: block !important;
        }
"""

def add_language_css(file_path):
    """파일에 언어 CSS가 있는지 확인하고 없으면 추가"""
    print(f"Processing: {file_path.name}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 이미 언어 CSS가 있는지 확인
    if 'body[data-lang="ko"]' in content and 'russian-text' in content:
        print(f"  [-] 언어 CSS 이미 존재: {file_path.name}")
        return False

    # </style> 태그 찾기 (첫 번째)
    style_end = content.find('</style>')
    if style_end == -1:
        print(f"  [SKIP] </style> 태그 없음: {file_path.name}")
        return False

    # CSS 삽입
    new_content = content[:style_end] + LANGUAGE_CSS + content[style_end:]

    # 저장
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  [OK] 언어 CSS 추가됨: {file_path.name}")
    return True

def main():
    print("=" * 60)
    print("모든 게시판 페이지에 언어 전환 CSS 추가")
    print("=" * 60)
    print()

    updated_count = 0
    skipped_count = 0

    for file_path in ALL_FILES:
        if not file_path.exists():
            continue

        if file_path.name in EXCLUDE_FILES:
            print(f"Skipping: {file_path.name} (excluded)")
            skipped_count += 1
            continue

        try:
            if add_language_css(file_path):
                updated_count += 1
        except Exception as e:
            print(f"  [ERROR] {file_path.name}: {e}")

    print()
    print("=" * 60)
    print(f"완료: {updated_count}개 파일 업데이트")
    print("=" * 60)

if __name__ == "__main__":
    main()
