#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
모든 게시판 페이지의 CSS 스타일을 통일된 러시아 테마로 업데이트하는 스크립트
"""

import re
import os

# 업데이트할 파일 목록
board_files = [
    'board-life.html',
    'board-admin.html',
    'board-job.html',
    'board-market.html',
    'board-startup.html',
    'board-notice.html',
]

# CSS 변수 업데이트
css_root_old = r':root\s*\{[^}]*--russian-red:\s*#DA020E;[^}]*--russian-blue:\s*#0039A6;[^}]*\}'
css_root_new = ''':root {
            --russian-red: #C1272D;
            --russian-blue: #0039A6;
            --russian-gold: #D4AF37;
            --russian-navy: #002B5C;
            --russian-white: #FFFFFF;
            --russian-light-blue: #4A90E2;
            --russian-cream: #F5F3EE;
            --gradient-primary: linear-gradient(135deg, var(--russian-blue) 0%, var(--russian-light-blue) 100%);
            --gradient-gold: linear-gradient(135deg, #D4AF37 0%, #F4E4B3 100%);
            --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.08);
            --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.12);
            --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.16);
        }'''

# body 스타일 업데이트
body_old = r'body\s*\{[^}]*background:\s*#f8f9fa;[^}]*\}'
body_new = '''body {
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
            font-size: 12px;
            line-height: 1.5;
            color: #2c3e50;
            background: linear-gradient(to bottom, #f8f9fa 0%, var(--russian-cream) 100%);
            min-height: 100vh;
        }'''

# 헤더 스타일 업데이트
header_old = r'\.header\s*\{[^}]*background:\s*white;[^}]*border-bottom:\s*1px\s+solid\s+#e0e0e0;[^}]*\}'
header_new = '''.header {
            background: var(--gradient-primary);
            box-shadow: var(--shadow-md);
            padding: 12px 0;
            position: sticky;
            top: 0;
            z-index: 1000;
        }'''

def update_file(filepath):
    """파일의 CSS를 업데이트"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # CSS 변수 업데이트
        content = re.sub(css_root_old, css_root_new, content, flags=re.DOTALL)

        # body 스타일 업데이트
        content = re.sub(body_old, body_new, content, flags=re.DOTALL)

        # 헤더 스타일 업데이트
        content = re.sub(header_old, header_new, content, flags=re.DOTALL)

        # 변경사항이 있으면 파일 저장
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {filepath}")
            return True
        else:
            print(f"No changes: {filepath}")
            return False

    except Exception as e:
        print(f"Error updating {filepath}: {e}")
        return False

def main():
    """메인 함수"""
    print("Updating board page styles to Russian theme...\n")

    updated_count = 0
    for filename in board_files:
        filepath = os.path.join(os.path.dirname(__file__), filename)
        if os.path.exists(filepath):
            if update_file(filepath):
                updated_count += 1
        else:
            print(f"File not found: {filepath}")

    print(f"\nComplete! Updated {updated_count} of {len(board_files)} files.")

if __name__ == '__main__':
    main()
