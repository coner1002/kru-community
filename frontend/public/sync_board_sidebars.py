#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
모든 board-*.html 파일의 사이드바를 동적 로딩으로 변경하는 스크립트
"""
import re
import glob
import os
import sys

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def update_sidebar(file_path):
    """파일의 사이드바 부분을 동적 로딩으로 변경"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 현재 게시판의 slug를 파일명에서 추출
    filename = os.path.basename(file_path)
    current_slug = filename.replace('board-', '').replace('.html', '')

    # 게시판 메뉴 섹션을 찾아서 교체
    old_pattern = r'(<!-- 게시판 메뉴 -->.*?<div class="sidebar-section">.*?<div class="sidebar-header">.*?<span class="korean-text">게시판</span>.*?<div class="russian-text">Доски объявлений</div>.*?</div>.*?<div class="sidebar-menu">)(.*?)(</div>\s*</div>)'

    new_sidebar = f'''<!-- 게시판 메뉴 (동적 생성) -->
                <div class="sidebar-section">
                    <div class="sidebar-header">
                        <span class="korean-text">게시판</span>
                        <div class="russian-text">Доски объявлений</div>
                    </div>
                    <div class="sidebar-menu" id="boardMenuList">
                        <!-- 카테고리가 로드될 때까지 로딩 표시 -->
                        <div style="padding: 20px; text-align: center; color: #999;">
                            <span class="korean-text">게시판 로딩 중...</span><br>
                            <span class="russian-text">Загрузка досок...</span>
                        </div>
                    </div>
                </div>'''

    # 정규식 패턴 매칭
    match = re.search(old_pattern, content, re.DOTALL)

    if match:
        # 교체
        content = content[:match.start()] + new_sidebar + content[match.end():]

        # JavaScript 함수 추가 (페이지 끝부분에)
        js_code = f'''
    <script>
        // API에서 게시판 메뉴 동적 생성
        const API_BASE_URL = 'http://localhost:8000';
        const CURRENT_SLUG = '{current_slug}';

        async function loadBoardMenu() {{
            try {{
                const response = await fetch(`${{API_BASE_URL}}/api/categories/`);
                if (!response.ok) {{
                    console.error('카테고리 로드 실패:', response.status);
                    return;
                }}

                const categories = await response.json();
                const menuList = document.getElementById('boardMenuList');

                if (categories && categories.length > 0) {{
                    // 활성화된 카테고리만 필터링하고 sort_order로 정렬
                    const activeCategories = categories
                        .filter(cat => cat.is_active)
                        .sort((a, b) => a.sort_order - b.sort_order);

                    menuList.innerHTML = activeCategories.map(cat => {{
                        const isActive = cat.slug === CURRENT_SLUG ? ' active' : '';
                        return `
                            <a href="/board-${{cat.slug}}.html" class="sidebar-item${{isActive}}">
                                <span class="korean-text">${{cat.icon || '📋'}} ${{cat.name_ko || cat.slug}}</span>
                                <div class="russian-text">${{cat.name_ru || ''}}</div>
                            </a>
                        `;
                    }}).join('');
                }} else {{
                    menuList.innerHTML = `
                        <div style="padding: 20px; text-align: center; color: #999;">
                            <span class="korean-text">게시판이 없습니다</span><br>
                            <span class="russian-text">Нет досок</span>
                        </div>
                    `;
                }}
            }} catch (error) {{
                console.error('게시판 메뉴 로드 오류:', error);
                const menuList = document.getElementById('boardMenuList');
                menuList.innerHTML = `
                    <div style="padding: 20px; text-align: center; color: #f44336;">
                        <span class="korean-text">로드 실패</span><br>
                        <span class="russian-text">Ошибка загрузки</span>
                    </div>
                `;
            }}
        }}

        // 페이지 로드 시 실행
        document.addEventListener('DOMContentLoaded', function() {{
            loadBoardMenu();
        }});
    </script>
</body>
</html>'''

        # 기존 </body></html> 태그를 찾아서 교체
        content = re.sub(r'</body>\s*</html>\s*$', js_code, content, flags=re.MULTILINE)

        # 파일 저장
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f'✅ Updated: {filename}')
        return True
    else:
        print(f'⚠️  Pattern not found in: {filename}')
        return False

def main():
    # board-*.html 파일 찾기 (board-write.html, board-view.html 제외)
    pattern = 'board-*.html'
    exclude = ['board-write.html', 'board-view.html', 'board-job-old.html']

    files = glob.glob(pattern)
    files = [f for f in files if os.path.basename(f) not in exclude]

    print(f'Found {len(files)} board files to update')
    print('=' * 50)

    success_count = 0
    for file_path in files:
        if update_sidebar(file_path):
            success_count += 1

    print('=' * 50)
    print(f'✅ Successfully updated {success_count}/{len(files)} files')

if __name__ == '__main__':
    main()
