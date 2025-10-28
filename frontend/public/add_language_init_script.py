#!/usr/bin/env python3
"""
모든 페이지의 head에 language-init.js 추가
"""

import re
from pathlib import Path

CURRENT_DIR = Path(__file__).parent

ALL_FILES = (
    list(CURRENT_DIR.glob("board-*.html")) +
    list(CURRENT_DIR.glob("contact-*.html")) +
    [CURRENT_DIR / "index.html"]
)

EXCLUDE_FILES = ['board-write.html', 'board-view.html', 'board-job-old.html']

SCRIPT_TAG = '<script src="/js/language-init.js"></script>'

def add_language_init_script(file_path):
    """head 섹션에 language-init.js 추가"""
    print(f"Processing: {file_path.name}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 이미 있는지 확인
    if 'language-init.js' in content:
        print(f"  [-] 스크립트 이미 존재: {file_path.name}")
        return False

    # </head> 태그 찾기
    head_end = content.find('</head>')
    if head_end == -1:
        print(f"  [SKIP] </head> 태그 없음: {file_path.name}")
        return False

    # 스크립트 삽입 (</head> 바로 앞)
    new_content = content[:head_end] + f'    {SCRIPT_TAG}\n' + content[head_end:]

    # 저장
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  [OK] 스크립트 추가됨: {file_path.name}")
    return True

def main():
    print("=" * 60)
    print("모든 페이지에 language-init.js 추가")
    print("=" * 60)
    print()

    updated_count = 0

    for file_path in ALL_FILES:
        if not file_path.exists():
            continue

        if file_path.name in EXCLUDE_FILES:
            print(f"Skipping: {file_path.name}")
            continue

        try:
            if add_language_init_script(file_path):
                updated_count += 1
        except Exception as e:
            print(f"  [ERROR] {file_path.name}: {e}")

    print()
    print("=" * 60)
    print(f"완료: {updated_count}개 파일 업데이트")
    print("=" * 60)

if __name__ == "__main__":
    main()
