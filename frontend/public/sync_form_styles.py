#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
contact-ad.html의 폼 스타일을 contact-suggest.html에 복사
"""

import re

source_file = 'contact-ad.html'
target_file = 'contact-suggest.html'

def main():
    print(f"Reading source file: {source_file}\n")

    # 소스 파일 읽기
    with open(source_file, 'r', encoding='utf-8') as f:
        source_content = f.read()

    # 폼 스타일 추출
    form_pattern = r'\.form-container \{.*?\.btn-cancel:hover \{[^}]+\}'
    form_match = re.search(form_pattern, source_content, re.DOTALL)

    if not form_match:
        print("Error: Could not extract form styles from source file")
        return

    form_styles = form_match.group(0)
    print(f"Extracted form styles: {len(form_styles)} characters\n")

    # 대상 파일 읽기
    print(f"Updating {target_file}...")
    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 기존 폼 스타일 교체
    if re.search(form_pattern, content, re.DOTALL):
        content = re.sub(form_pattern, form_styles, content, flags=re.DOTALL)
        print(f"  - Form styles replaced")
    else:
        print(f"  - WARNING: Form styles pattern not found")

    # 변경사항이 있으면 저장
    if content != original_content:
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  SUCCESS: {target_file} updated\n")
    else:
        print(f"  SKIPPED: {target_file} (no changes)\n")

if __name__ == '__main__':
    main()
