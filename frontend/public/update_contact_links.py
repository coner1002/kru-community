#!/usr/bin/env python3
"""
광고 및 협력 요청, 운영자에게 건의 페이지를 게시판에서 양식 페이지로 변경
"""
import re
from pathlib import Path

# 수정할 파일 목록
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
    'board-trade.html'
]

# 찾을 패턴
old_pattern = r'''                        \/\/ 일반 게시판인 경우
                        return `
                            <a href="/board-\${cat\.slug}\.html" class="sidebar-item">
                                <span class="korean-text">\${cat\.icon \|\| '📋'} \${cat\.name_ko \|\| cat\.slug}</span>
                                <div class="russian-text">\${cat\.name_ru \|\| ''}</div>
                            </a>
                        `;'''

# 교체할 패턴
new_pattern = '''                        // 문의 양식 페이지 (ad, suggest)는 contact- 페이지로 링크
                        const isContactForm = cat.slug === 'ad' || cat.slug === 'suggest';
                        const pageUrl = isContactForm ? `/contact-${cat.slug}.html` : `/board-${cat.slug}.html`;

                        // 일반 게시판 또는 문의 양식
                        return `
                            <a href="${pageUrl}" class="sidebar-item">
                                <span class="korean-text">${cat.icon || '📋'} ${cat.name_ko || cat.slug}</span>
                                <div class="russian-text">${cat.name_ru || ''}</div>
                            </a>
                        `;'''

updated_count = 0
skipped_count = 0

for filename in files_to_update:
    filepath = Path(filename)

    if not filepath.exists():
        print(f"[SKIP] {filename} - file not found")
        skipped_count += 1
        continue

    # 파일 읽기
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"[ERROR] {filename} - read error: {e}")
        skipped_count += 1
        continue

    # 패턴 검색 및 교체
    # 정규식 패턴을 더 유연하게 만들기
    pattern = r"// 일반 게시판인 경우\s+return `\s+<a href=\"/board-\$\{cat\.slug\}\.html\" class=\"sidebar-item\">\s+<span class=\"korean-text\">\$\{cat\.icon \|\| '📋'\} \$\{cat\.name_ko \|\| cat\.slug\}</span>\s+<div class=\"russian-text\">\$\{cat\.name_ru \|\| ''\}</div>\s+</a>\s+`;"

    if re.search(pattern, content):
        # 교체
        new_content = re.sub(
            pattern,
            new_pattern,
            content
        )

        # 파일 쓰기
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"[OK] {filename} - updated successfully")
            updated_count += 1
        except Exception as e:
            print(f"[ERROR] {filename} - write error: {e}")
            skipped_count += 1
    else:
        print(f"[SKIP] {filename} - pattern not found")
        skipped_count += 1

print(f"\n=== Summary ===")
print(f"Updated: {updated_count}")
print(f"Skipped: {skipped_count}")
print(f"Total: {len(files_to_update)}")
