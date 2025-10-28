#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
특수 페이지들(무역파트너, 입점업체, 광고/협력, 건의)에 Russian 테마 적용
"""

import re

# 소스 파일
source_file = 'board-free.html'

# 대상 파일 목록
target_files = [
    'trade-partners.html',
    'partners.html',
    'contact-ad.html',
    'contact-suggest.html',
]

def extract_css_variables(content):
    """CSS 변수 추출"""
    pattern = r':root \{[^}]+\}'
    match = re.search(pattern, content, re.DOTALL)
    return match.group(0) if match else None

def extract_header_styles(content):
    """헤더 스타일 추출"""
    pattern = r'/\* 헤더 \*/.*?(?=/\* 검색박스|/\* 메인 레이아웃)'
    match = re.search(pattern, content, re.DOTALL)
    return match.group(0) if match else None

def extract_sidebar_styles(content):
    """사이드바 스타일 추출"""
    pattern = r'/\* 사이드바 \*/.*?(?=/\* 언어 전환|/\* 우측 사이드바|/\* 게시판)'
    match = re.search(pattern, content, re.DOTALL)
    return match.group(0) if match else None

def main():
    print("Reading source file: board-free.html\n")

    # 소스 파일 읽기
    with open(source_file, 'r', encoding='utf-8') as f:
        source_content = f.read()

    # 스타일 추출
    css_vars = extract_css_variables(source_content)
    header_styles = extract_header_styles(source_content)
    sidebar_styles = extract_sidebar_styles(source_content)

    if not css_vars:
        print("Error: Could not extract CSS variables")
        return

    print(f"Extracted CSS variables: {len(css_vars)} characters")
    print(f"Extracted header styles: {len(header_styles) if header_styles else 0} characters")
    print(f"Extracted sidebar styles: {len(sidebar_styles) if sidebar_styles else 0} characters\n")

    # 각 대상 파일에 적용
    updated_count = 0
    for target_file in target_files:
        try:
            print(f"Updating {target_file}...")

            with open(target_file, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # CSS 변수 교체
            old_vars_pattern = r':root \{[^}]+\}'
            if re.search(old_vars_pattern, content):
                content = re.sub(old_vars_pattern, css_vars, content, flags=re.DOTALL)
                print(f"  - CSS variables replaced")
            else:
                print(f"  - WARNING: CSS variables pattern not found")

            # 헤더 스타일 교체
            if header_styles:
                old_header_pattern = r'/\* 헤더 \*/.*?(?=/\* 언어 전환|/\* 메인 레이아웃|/\* 사이드바)'
                if re.search(old_header_pattern, content, re.DOTALL):
                    content = re.sub(old_header_pattern, header_styles, content, flags=re.DOTALL)
                    print(f"  - Header styles replaced")

            # 사이드바 스타일 교체
            if sidebar_styles:
                old_sidebar_pattern = r'/\* 사이드바 \*/.*?(?=/\* 언어 전환|/\* 우측 사이드바|/\* 컨텐츠|/\* 파트너)'
                if re.search(old_sidebar_pattern, content, re.DOTALL):
                    content = re.sub(old_sidebar_pattern, sidebar_styles, content, flags=re.DOTALL)
                    print(f"  - Sidebar styles replaced")

            # 변경사항이 있으면 저장
            if content != original_content:
                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  SUCCESS: {target_file} updated\n")
                updated_count += 1
            else:
                print(f"  SKIPPED: {target_file} (no changes)\n")

        except Exception as e:
            print(f"  ERROR: {target_file} - {e}\n")

    print(f"\nComplete! Updated {updated_count} of {len(target_files)} files.")

if __name__ == '__main__':
    main()
