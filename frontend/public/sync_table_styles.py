#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
board-free.html의 업데이트된 테이블 스타일을 모든 게시판 페이지에 복사하는 스크립트
"""

import re

# 소스 파일
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

def main():
    print("Reading source file: board-free.html\n")

    # 소스 파일 읽기
    with open(source_file, 'r', encoding='utf-8') as f:
        source_content = f.read()

    # 테이블 스타일 추출 (/* 게시글 목록 테이블 */ ~ .notice-row .post-number)
    table_pattern = r'/\* 게시글 목록 테이블.*?\}(?=\s*/\* 공지글)'
    table_match = re.search(table_pattern, source_content, re.DOTALL)

    notice_pattern = r'/\* 공지글 스타일.*?font-weight: 700 !important;\s*\}'
    notice_match = re.search(notice_pattern, source_content, re.DOTALL)

    if not table_match or not notice_match:
        print("Error: Could not extract table or notice styles from source file")
        return

    table_css = table_match.group(0)
    notice_css = notice_match.group(0)

    print(f"Extracted table CSS: {len(table_css)} characters")
    print(f"Extracted notice CSS: {len(notice_css)} characters\n")

    # 각 대상 파일에 적용
    updated_count = 0
    for target_file in target_files:
        try:
            print(f"Updating {target_file}...")

            with open(target_file, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # 기존 테이블 스타일 교체
            old_table_pattern = r'/\* 게시글 목록 테이블.*?\}(?=\s*/\* 공지글)'
            if re.search(old_table_pattern, content, re.DOTALL):
                content = re.sub(old_table_pattern, table_css, content, flags=re.DOTALL)
                print(f"  - Table styles replaced")
            else:
                print(f"  - WARNING: Table styles pattern not found")

            # 기존 공지글 스타일 교체
            old_notice_pattern = r'/\* 공지글 스타일.*?font-weight: 700 !important;\s*\}'
            if re.search(old_notice_pattern, content, re.DOTALL):
                content = re.sub(old_notice_pattern, notice_css, content, flags=re.DOTALL)
                print(f"  - Notice styles replaced")
            else:
                print(f"  - WARNING: Notice styles pattern not found")

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
