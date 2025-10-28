#!/usr/bin/env python3
"""
사이드바 메뉴에서 layout_type을 사용하도록 업데이트
"""
import os
import re

# 업데이트할 파일 목록
files_to_update = [
    'board-ad.html',
    'board-admin.html',
    'board-business.html',
    'board-contact.html',
    'board-free.html',
    'board-job.html',
    'board-life.html',
    'board-market.html',
    'board-notice.html',
    'board-partners.html',
    'board-startup.html',
    'board-suggest.html',
    'board-trade.html',
]

# 찾을 패턴
old_pattern = r'// 문의 양식 페이지 \(ad, suggest\)는 contact- 페이지로 링크\s+const isContactForm = cat\.slug === \'ad\' \|\| cat\.slug === \'suggest\';'

# 새로운 코드
new_code = "// layout_type에 따라 페이지 URL 결정\n                        const isContactForm = cat.layout_type === 'form';"

updated_count = 0
skipped_count = 0

for filename in files_to_update:
    if not os.path.exists(filename):
        print(f'[SKIP] {filename} - 파일이 존재하지 않습니다')
        skipped_count += 1
        continue

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # 패턴 검색 및 교체
        if re.search(old_pattern, content):
            new_content = re.sub(old_pattern, new_code, content)

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f'[OK] {filename} - 업데이트 완료')
            updated_count += 1
        else:
            print(f'[SKIP] {filename} - 패턴을 찾을 수 없습니다')
            skipped_count += 1

    except Exception as e:
        print(f'[ERROR] {filename} - {e}')
        skipped_count += 1

print(f'\n=== 결과 ===')
print(f'업데이트됨: {updated_count}개')
print(f'건너뜀: {skipped_count}개')
print(f'총: {len(files_to_update)}개')
