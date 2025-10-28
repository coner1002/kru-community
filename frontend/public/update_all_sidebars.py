#!/usr/bin/env python3
"""
모든 게시판 페이지의 사이드바를 표준 사이드바로 업데이트하는 스크립트
"""

import os
import re
from pathlib import Path

# 표준 사이드바 HTML
STANDARD_SIDEBAR = '''            <!-- 좌측 사이드바 -->
            <aside class="sidebar">
                <!-- 게시판 메뉴 -->
                <div class="sidebar-section">
                    <div class="sidebar-header">
                        <span class="korean-text">게시판</span>
                        <div class="russian-text">Доски объявлений</div>
                    </div>
                    <div class="sidebar-menu">
                        <a href="/board-notice.html" class="sidebar-item" data-category="notice">
                            <span class="korean-text">공지사항</span>
                            <div class="russian-text">Объявления</div>
                        </a>
                        <a href="/board-free.html" class="sidebar-item" data-category="free">
                            <span class="korean-text">자유게시판</span>
                            <div class="russian-text">Свободное общение</div>
                        </a>
                        <a href="/board-life.html" class="sidebar-item" data-category="life">
                            <span class="korean-text">생활정보</span>
                            <div class="russian-text">Жизнь в Корее</div>
                        </a>
                        <a href="/board-admin.html" class="sidebar-item" data-category="admin">
                            <span class="korean-text">행정정보</span>
                            <div class="russian-text">Админ. информация</div>
                        </a>
                        <a href="/board-job.html" class="sidebar-item" data-category="job">
                            <span class="korean-text">구인구직</span>
                            <div class="russian-text">Работа</div>
                        </a>
                        <a href="/board-market.html" class="sidebar-item" data-category="market">
                            <span class="korean-text">벼룩시장</span>
                            <div class="russian-text">Барахолка</div>
                        </a>
                        <a href="/board-business.html" class="sidebar-item" data-category="business">
                            <span class="korean-text">비즈니스</span>
                            <div class="russian-text">Бизнес</div>
                        </a>
                        <a href="/board-startup.html" class="sidebar-item" data-category="startup">
                            <span class="korean-text">스타트업</span>
                            <div class="russian-text">Стартап</div>
                        </a>
                        <a href="/board-partners.html" class="sidebar-item" data-category="partners">
                            <span class="korean-text">파트너스</span>
                            <div class="russian-text">Партнеры</div>
                        </a>
                        <a href="/board-trade.html" class="sidebar-item" data-category="trade">
                            <span class="korean-text">무역</span>
                            <div class="russian-text">Торговля</div>
                        </a>
                        <a href="/board-ad.html" class="sidebar-item" data-category="ad">
                            <span class="korean-text">광고</span>
                            <div class="russian-text">Реклама</div>
                        </a>
                        <a href="/board-suggest.html" class="sidebar-item" data-category="suggest">
                            <span class="korean-text">건의사항</span>
                            <div class="russian-text">Предложения</div>
                        </a>
                        <a href="/board-contact.html" class="sidebar-item" data-category="contact">
                            <span class="korean-text">문의</span>
                            <div class="russian-text">Контакты</div>
                        </a>
                    </div>
                </div>
            </aside>'''

# 자동 하이라이트 스크립트
AUTO_HIGHLIGHT_SCRIPT = '''
        // 사이드바 메뉴 active 상태 자동 설정
        (function() {
            const currentPage = window.location.pathname.split('/').pop();
            const urlParams = new URLSearchParams(window.location.search);

            // 페이지별 카테고리 매핑
            const pageToCategory = {
                'board-notice.html': 'notice',
                'board-free.html': 'free',
                'board-life.html': 'life',
                'board-admin.html': 'admin',
                'board-job.html': 'job',
                'board-market.html': 'market',
                'board-business.html': 'business',
                'board-startup.html': 'startup',
                'board-partners.html': 'partners',
                'board-trade.html': 'trade',
                'board-ad.html': 'ad',
                'board-suggest.html': 'suggest',
                'board-contact.html': 'contact'
            };

            // 현재 페이지의 카테고리 결정
            let categorySlug = pageToCategory[currentPage] || urlParams.get('category');

            if (categorySlug) {
                document.querySelectorAll('.sidebar-item').forEach(item => {
                    item.classList.remove('active');
                    if (item.dataset.category === categorySlug) {
                        item.classList.add('active');
                    }
                });
            }
        })();'''

def update_sidebar_in_file(filepath):
    """파일의 사이드바를 표준 사이드바로 교체"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 사이드바 패턴 매칭 (<!-- 좌측 사이드바 --> 부터 </aside> 까지)
        pattern = r'<!-- 좌측 사이드바 -->.*?</aside>'

        # 표준 사이드바로 교체
        new_content = re.sub(pattern, STANDARD_SIDEBAR, content, flags=re.DOTALL)

        # 이미 자동 하이라이트 스크립트가 있는지 확인
        if '사이드바 메뉴 active 상태' not in new_content:
            # </body> 태그 바로 전에 스크립트 추가
            script_tag = f'    <script>{AUTO_HIGHLIGHT_SCRIPT}    </script>\n</body>'
            new_content = new_content.replace('</body>', script_tag)

        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True
    except Exception as e:
        print(f"Error updating {filepath}: {e}")
        return False

def main():
    """메인 함수"""
    current_dir = Path(__file__).parent

    # 업데이트할 파일 목록
    board_files = [
        'board-notice.html',
        'board-free.html',
        'board-life.html',
        'board-admin.html',
        'board-job.html',
        'board-market.html',
        'board-business.html',
        'board-startup.html',
        'board-partners.html',
        'board-trade.html',
        'board-ad.html',
        'board-suggest.html',
        'board-contact.html'
    ]

    updated = 0
    failed = 0

    for filename in board_files:
        filepath = current_dir / filename
        if filepath.exists():
            print(f"Updating {filename}...")
            if update_sidebar_in_file(filepath):
                updated += 1
                print(f"  OK: {filename} updated successfully")
            else:
                failed += 1
                print(f"  FAIL: {filename} update failed")
        else:
            print(f"  - {filename} not found, skipping")

    print(f"\n완료: {updated}개 파일 업데이트, {failed}개 실패")

if __name__ == '__main__':
    main()
