#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
board-free.html의 완성된 CSS를 모든 게시판 페이지에 복사하는 스크립트
"""

import re

# 소스 파일 (완성된 CSS가 있는 파일)
source_file = 'board-free.html'

# 대상 파일 목록
target_files = [
    'board-life.html',
    'board-admin.html',
    'board-job.html',
    'board-market.html',
    'board-startup.html',
    'board-notice.html',
]

def extract_css_block(content, start_pattern, end_pattern):
    """특정 CSS 블록을 추출"""
    match = re.search(f'{start_pattern}.*?{end_pattern}', content, re.DOTALL)
    if match:
        return match.group(0)
    return None

def replace_css_block(content, old_pattern, new_block):
    """기존 CSS 블록을 새로운 블록으로 교체"""
    return re.sub(old_pattern, new_block, content, flags=re.DOTALL)

def main():
    print("Reading source file: board-free.html\n")

    # 소스 파일 읽기
    with open(source_file, 'r', encoding='utf-8') as f:
        source_content = f.read()

    # 검색박스 스타일 추출 (.search-input ~ .search-btn:hover)
    search_css = extract_css_block(
        source_content,
        r'\.search-input\s*\{',
        r'\.search-btn:hover\s*\{[^}]+\}'
    )

    # 네비게이션 스타일 추출 (.nav-menu ~ .nav-menu a:hover::after)
    nav_css = extract_css_block(
        source_content,
        r'\.nav-menu\s*\{',
        r'\.nav-menu a:hover::after\s*\{[^}]+\}'
    )

    # 사이드바 스타일 추출 (.sidebar-section ~ .sidebar-item.active)
    sidebar_css = extract_css_block(
        source_content,
        r'/\* 사이드바 \*/',
        r'\.sidebar-item\.active\s*\{[^}]+\}'
    )

    if not all([search_css, nav_css, sidebar_css]):
        print("Error: Could not extract all CSS blocks from source file")
        return

    print(f"Extracted CSS blocks:")
    print(f"  - Search box: {len(search_css)} characters")
    print(f"  - Navigation: {len(nav_css)} characters")
    print(f"  - Sidebar: {len(sidebar_css)} characters\n")

    # 각 대상 파일에 적용
    updated_count = 0
    for target_file in target_files:
        try:
            print(f"Updating {target_file}...")

            with open(target_file, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # 검색박스 스타일 교체
            content = replace_css_block(
                content,
                r'\.search-input\s*\{.*?\.search-btn:hover\s*\{[^}]+\}',
                search_css
            )

            # 네비게이션 스타일 교체
            content = replace_css_block(
                content,
                r'\.nav-menu\s*\{.*?\.nav-menu a:hover::after\s*\{[^}]+\}',
                nav_css
            )

            # 사이드바 스타일 교체
            content = replace_css_block(
                content,
                r'/\* 사이드바 \*/.*?\.sidebar-item\.active\s*\{[^}]+\}',
                sidebar_css
            )

            # 변경사항이 있으면 저장
            if content != original_content:
                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  SUCCESS: {target_file} updated")
                updated_count += 1
            else:
                print(f"  SKIPPED: {target_file} (no changes)")

        except Exception as e:
            print(f"  ERROR: {target_file} - {e}")

    print(f"\nComplete! Updated {updated_count} of {len(target_files)} files.")

if __name__ == '__main__':
    main()
