#!/usr/bin/env python3
"""
광고 및 협력 요청, 운영자에게 건의 페이지를 게시판에서 양식 페이지로 변경
"""
from pathlib import Path

# 수정할 파일 목록 (board-free.html은 이미 수정됨)
files_to_update = [
    'board-notice.html',
    'board-life.html',
    'board-job.html',
    'board-market.html',
    'board-admin.html',
    'board-business.html',
    'board-partners.html',
    'board-trade.html',
    'board-ad.html',
    'board-suggest.html',
    'board-contact.html',
    'board-startup.html'
]

# 찾을 텍스트 (정확히 일치하는 블록)
old_text = '''                        // 일반 게시판인 경우
                        return `
                            <a href="/board-${cat.slug}.html" class="sidebar-item${isActive}">
                                <span class="korean-text">${cat.icon || '📋'} ${cat.name_ko || cat.slug}</span>
                                <div class="russian-text">${cat.name_ru || ''}</div>
                            </a>
                        `;'''

# 교체할 텍스트
new_text = '''
                        // 문의 양식 페이지 (ad, suggest)는 contact- 페이지로 링크
                        const isContactForm = cat.slug === 'ad' || cat.slug === 'suggest';
                        const pageUrl = isContactForm ? `/contact-${cat.slug}.html` : `/board-${cat.slug}.html`;

                        // 일반 게시판 또는 문의 양식
                        return `
                            <a href="${pageUrl}" class="sidebar-item${isActive}">
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

    # 텍스트 검색 및 교체
    if old_text in content:
        # 교체
        new_content = content.replace(old_text, new_text)

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
