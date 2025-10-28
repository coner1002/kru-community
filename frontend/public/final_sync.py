#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
최종 동기화: board-free.html의 모든 스타일을 다른 게시판에 정확히 복사
"""

import re

source = 'board-free.html'
targets = [
    'board-life.html',
    'board-admin.html',
    'board-job.html',
    'board-market.html',
    'board-startup.html',
    'board-notice.html'
]

def extract_and_apply():
    # 소스 파일 읽기
    with open(source, 'r', encoding='utf-8') as f:
        source_content = f.read()

    # 네비게이션 스타일 추출 (전체 블록)
    nav_pattern = r'\.nav-menu \{.*?width: 80%;\s*\}'
    nav_match = re.search(nav_pattern, source_content, re.DOTALL)

    if not nav_match:
        print("ERROR: Could not find navigation styles")
        return

    nav_css = nav_match.group(0)
    print(f"Extracted navigation CSS: {len(nav_css)} chars")

    # 각 파일에 적용
    for target in targets:
        try:
            with open(target, 'r', encoding='utf-8') as f:
                content = f.read()

            # 기존 네비게이션 스타일 찾기 및 교체
            old_nav_pattern = r'\.nav-menu \{.*?\.nav-menu a:hover \{[^}]+\}'

            if re.search(old_nav_pattern, content, re.DOTALL):
                content = re.sub(old_nav_pattern, nav_css, content, flags=re.DOTALL)

                with open(target, 'w', encoding='utf-8') as f:
                    f.write(content)

                print(f"SUCCESS: {target}")
            else:
                print(f"SKIPPED: {target} (pattern not found)")

        except Exception as e:
            print(f"ERROR: {target} - {e}")

if __name__ == '__main__':
    extract_and_apply()
