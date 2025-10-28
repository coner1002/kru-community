#!/usr/bin/env python3
"""
모든 페이지에서 중복된 언어 전환 스크립트를 제거하는 스크립트
load-sidebar.js가 언어 전환을 처리하므로 중복 제거 필요
"""

import os
import re
from pathlib import Path

# 현재 디렉토리
CURRENT_DIR = Path(__file__).parent

# 모든 HTML 파일 찾기
ALL_FILES = (
    list(CURRENT_DIR.glob("board-*.html")) +
    list(CURRENT_DIR.glob("contact-*.html"))
)

# 제외할 파일들
EXCLUDE_FILES = ['board-write.html', 'board-view.html', 'board-job-old.html']

def remove_duplicate_language_script(file_path):
    """파일에서 중복된 언어 전환 스크립트를 제거"""
    print(f"Processing: {file_path.name}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 언어 전환 스크립트 패턴 찾기 (load-sidebar.js 이전에 있는 것만)
    # 패턴: 언어 버튼 이벤트 리스너와 저장된 언어 불러오기
    pattern = r'<script>\s*// 언어 전환 기능\s*document\.querySelectorAll.*?</script>'

    # 스크립트가 load-sidebar.js보다 앞에 있으면 제거하지 않음
    # load-sidebar.js 뒤에 있으면 제거
    if 'load-sidebar.js' in content:
        # load-sidebar.js 위치 찾기
        sidebar_pos = content.find('load-sidebar.js')

        # 언어 전환 스크립트 찾기
        matches = list(re.finditer(pattern, content, flags=re.DOTALL))

        for match in matches:
            # 언어 스크립트가 sidebar 스크립트보다 뒤에 있으면 제거
            if match.start() > sidebar_pos:
                print(f"  [REMOVE] 중복 언어 스크립트 제거 at position {match.start()}")
                content = content[:match.start()] + content[match.end():]
                break

    # 변경사항이 있으면 파일 저장
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [OK] Updated: {file_path.name}")
        return True
    else:
        print(f"  [-] No changes needed: {file_path.name}")
        return False

def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("중복된 언어 전환 스크립트 제거")
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
            if remove_duplicate_language_script(file_path):
                updated_count += 1
        except Exception as e:
            print(f"  [ERROR] Error processing {file_path.name}: {e}")

    print()
    print("=" * 60)
    print(f"완료: {updated_count}개 파일 업데이트, {skipped_count}개 파일 제외")
    print("=" * 60)

if __name__ == "__main__":
    main()
