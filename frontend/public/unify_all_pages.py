#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
board-free.html의 완전한 헤더/사이드바/위젯 구조를 특수 페이지들에 복사
"""

import re

source_file = 'board-free.html'

target_files = [
    'trade-partners.html',
    'partners.html',
    'contact-ad.html',
    'contact-suggest.html',
]

def extract_complete_header(content):
    """헤더 전체 추출 (로고부터 네비게이션까지)"""
    # <header>부터 </header>까지
    pattern = r'<header class="header">.*?</header>'
    match = re.search(pattern, content, re.DOTALL)
    return match.group(0) if match else None

def extract_sidebar_html(content):
    """좌측 사이드바 HTML 추출"""
    # <aside class="sidebar">부터 </aside>까지
    pattern = r'<aside class="sidebar">.*?</aside>'
    match = re.search(pattern, content, re.DOTALL)
    return match.group(0) if match else None

def extract_right_sidebar_html(content):
    """우측 사이드바 HTML 추출"""
    # <aside class="right-sidebar">부터 </aside>까지
    pattern = r'<aside class="right-sidebar">.*?</aside>'
    match = re.search(pattern, content, re.DOTALL)
    return match.group(0) if match else None

def extract_complete_styles(content):
    """전체 스타일 추출"""
    # <style>부터 </style>까지
    pattern = r'<style>.*?</style>'
    match = re.search(pattern, content, re.DOTALL)
    return match.group(0) if match else None

def main():
    print(f"Reading source file: {source_file}\n")

    # 소스 파일 읽기
    with open(source_file, 'r', encoding='utf-8') as f:
        source_content = f.read()

    # 모든 요소 추출
    complete_styles = extract_complete_styles(source_content)
    header_html = extract_complete_header(source_content)
    sidebar_html = extract_sidebar_html(source_content)
    right_sidebar_html = extract_right_sidebar_html(source_content)

    if not all([complete_styles, header_html, sidebar_html]):
        print("Error: Could not extract required elements")
        return

    print(f"Extracted complete styles: {len(complete_styles)} characters")
    print(f"Extracted header HTML: {len(header_html)} characters")
    print(f"Extracted sidebar HTML: {len(sidebar_html)} characters")
    print(f"Extracted right sidebar HTML: {len(right_sidebar_html) if right_sidebar_html else 0} characters\n")

    # 각 대상 파일 처리
    for target_file in target_files:
        try:
            print(f"Processing {target_file}...")

            with open(target_file, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # 1. 전체 스타일 교체
            old_style_pattern = r'<style>.*?</style>'
            if re.search(old_style_pattern, content, re.DOTALL):
                content = re.sub(old_style_pattern, complete_styles, content, flags=re.DOTALL)
                print(f"  - Complete styles replaced")

            # 2. 헤더 교체
            old_header_pattern = r'<header[^>]*>.*?</header>'
            if re.search(old_header_pattern, content, re.DOTALL):
                content = re.sub(old_header_pattern, header_html, content, flags=re.DOTALL)
                print(f"  - Header replaced")

            # 3. 좌측 사이드바 교체
            old_sidebar_pattern = r'<aside class="sidebar">.*?</aside>'
            if re.search(old_sidebar_pattern, content, re.DOTALL):
                content = re.sub(old_sidebar_pattern, sidebar_html, content, flags=re.DOTALL)
                print(f"  - Left sidebar replaced")
            else:
                # 사이드바가 없으면 main-layout에 추가
                main_layout_pattern = r'<div class="main-layout">'
                if re.search(main_layout_pattern, content):
                    content = re.sub(main_layout_pattern,
                                   f'<div class="main-layout">\n        {sidebar_html}\n        ',
                                   content)
                    print(f"  - Left sidebar added")

            # 4. 우측 사이드바 교체/추가
            if right_sidebar_html:
                old_right_sidebar_pattern = r'<aside class="right-sidebar">.*?</aside>'
                if re.search(old_right_sidebar_pattern, content, re.DOTALL):
                    content = re.sub(old_right_sidebar_pattern, right_sidebar_html, content, flags=re.DOTALL)
                    print(f"  - Right sidebar replaced")
                else:
                    # 우측 사이드바가 없으면 main-layout 끝에 추가
                    main_layout_end = r'</div>\s*</div>\s*<!-- container -->'
                    if re.search(main_layout_end, content):
                        content = re.sub(r'(</div>\s*)(</div>\s*<!-- container -->)',
                                       f'{right_sidebar_html}\n        \\1\\2',
                                       content, count=1)
                        print(f"  - Right sidebar added")

            # 저장
            if content != original_content:
                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  SUCCESS: {target_file} updated\n")
            else:
                print(f"  SKIPPED: {target_file} (no changes)\n")

        except Exception as e:
            print(f"  ERROR: {target_file} - {e}\n")

    print("Complete!")

if __name__ == '__main__':
    main()
