#!/usr/bin/env python3
"""
모든 게시판 및 관련 페이지의 사이드바를 공통 사이드바로 교체하는 스크립트
"""

import os
import re
from pathlib import Path

# 현재 디렉토리
CURRENT_DIR = Path(__file__).parent

# 모든 사이드바가 있는 페이지들 찾기
ALL_FILES = (
    list(CURRENT_DIR.glob("board-*.html")) +
    list(CURRENT_DIR.glob("contact-*.html")) +
    list(CURRENT_DIR.glob("*-write.html")) +
    [CURRENT_DIR / "partners.html", CURRENT_DIR / "trade-partners.html"]
)

# 제외할 파일들
EXCLUDE_FILES = ['board-write.html', 'board-view.html', 'board-job-old.html',
                 'common-sidebar.html', 'sidebar.html', 'standard-sidebar.html',
                 'test-sidebar.html']

def replace_sidebar(file_path):
    """파일에서 사이드바를 공통 사이드바로 교체"""
    print(f"Processing: {file_path.name}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 1. 사이드바 HTML 교체 (여러 패턴 시도)
    # 패턴 1: 좌측 사이드바 주석이 있는 경우
    sidebar_pattern1 = r'<!-- 좌측 사이드바 -->\s*<aside class="sidebar">.*?</aside>'
    # 패턴 2: 사이드바 주석이 있는 경우
    sidebar_pattern2 = r'<!-- 사이드바 -->\s*<aside class="sidebar">.*?</aside>'
    # 패턴 3: 주석 없이 aside만 있는 경우
    sidebar_pattern3 = r'<aside class="sidebar">\s*<!-- 게시판 메뉴 -->.*?</aside>'

    # 교체용 텍스트
    sidebar_replacement = '<div id="sidebar-container"></div>'

    # 패턴들을 순서대로 시도
    for pattern in [sidebar_pattern1, sidebar_pattern2, sidebar_pattern3]:
        if re.search(pattern, content, flags=re.DOTALL):
            new_content = re.sub(pattern, sidebar_replacement, content, flags=re.DOTALL)
            break
    else:
        new_content = content

    # 2. loadBoardMenu 스크립트 제거
    script_pattern = r'<script>\s*// API에서 게시판 메뉴 동적 생성.*?</script>'
    script_replacement = '<!-- 공통 사이드바 로드 스크립트 -->\n    <script src="/js/load-sidebar.js"></script>'

    new_content = re.sub(script_pattern, script_replacement, new_content, flags=re.DOTALL)

    # 변경사항이 있으면 파일 저장
    if content != new_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  [OK] Updated: {file_path.name}")
        return True
    else:
        print(f"  [-] No changes needed: {file_path.name}")
        return False

def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("모든 게시판 및 관련 페이지의 사이드바를 공통 사이드바로 교체")
    print("=" * 60)
    print()

    updated_count = 0
    skipped_count = 0

    for file_path in ALL_FILES:
        if file_path.name in EXCLUDE_FILES:
            print(f"Skipping: {file_path.name} (excluded)")
            skipped_count += 1
            continue

        try:
            if replace_sidebar(file_path):
                updated_count += 1
        except Exception as e:
            print(f"  [ERROR] Error processing {file_path.name}: {e}")

    print()
    print("=" * 60)
    print(f"완료: {updated_count}개 파일 업데이트, {skipped_count}개 파일 제외")
    print("=" * 60)

if __name__ == "__main__":
    main()
