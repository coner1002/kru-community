#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
index.html의 위젯 스타일을 모든 게시판 페이지에 복사하는 스크립트
"""

import re

# 소스 파일
source_file = 'index.html'

# 대상 파일 목록
target_files = [
    'board-free.html',
    'board-life.html',
    'board-admin.html',
    'board-job.html',
    'board-market.html',
    'board-startup.html',
    'board-notice.html',
]

def main():
    print("Reading source file: index.html\n")

    # 소스 파일 읽기
    with open(source_file, 'r', encoding='utf-8') as f:
        source_content = f.read()

    # 위젯 스타일 추출 (/* 우측 사이드바 */ ~ .widget-content)
    widget_pattern = r'/\* 우측 사이드바 \*/.*?\.widget-content\s*\{[^}]+\}'
    widget_match = re.search(widget_pattern, source_content, re.DOTALL)

    if not widget_match:
        print("Error: Could not extract widget styles from source file")
        return

    widget_css = widget_match.group(0)
    print(f"Extracted widget CSS: {len(widget_css)} characters\n")

    # 각 대상 파일에 적용
    updated_count = 0
    for target_file in target_files:
        try:
            print(f"Updating {target_file}...")

            with open(target_file, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # 기존 위젯 스타일 패턴 찾기
            old_pattern = r'/\* 우측 사이드바 \*/.*?\.widget-content\s*\{[^}]+\}'

            # 위젯 스타일 교체
            if re.search(old_pattern, content, re.DOTALL):
                content = re.sub(old_pattern, widget_css, content, flags=re.DOTALL)
            else:
                # 패턴을 찾지 못한 경우, .widget { 부분만 찾아서 교체 시도
                old_widget_pattern = r'\.widget\s*\{.*?\.widget-content\s*\{[^}]+\}'
                if re.search(old_widget_pattern, content, re.DOTALL):
                    content = re.sub(old_widget_pattern, widget_css, content, flags=re.DOTALL)

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
