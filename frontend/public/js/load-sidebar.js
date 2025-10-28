// 공통 사이드바 로드 및 메뉴 생성 스크립트
async function initSidebar() {
    const API_BASE_URL = 'http://localhost:8000';

    // 현재 페이지의 slug 추출
    function getCurrentSlug() {
        const currentPage = window.location.pathname.split('/').pop();
        // board-*.html 또는 contact-*.html 패턴 매칭
        const boardMatch = currentPage.match(/board-(\w+)\.html/);
        const contactMatch = currentPage.match(/contact-(\w+)\.html/);
        return boardMatch ? boardMatch[1] : (contactMatch ? contactMatch[1] : '');
    }

    const CURRENT_SLUG = getCurrentSlug();

    // 사이드바 HTML 생성
    function createSidebarHTML() {
        return `
            <aside class="sidebar">
                <!-- 게시판 메뉴 -->
                <div class="sidebar-section">
                    <div class="sidebar-header">
                        <span class="korean-text">게시판</span>
                        <div class="russian-text">Доски объявлений</div>
                    </div>
                    <div class="sidebar-menu" id="boardMenuList">
                        <!-- 동적으로 로드됨 -->
                    </div>
                </div>
            </aside>
        `;
    }

    // 게시판 메뉴 로드
    async function loadBoardMenu() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/categories/`);
            if (!response.ok) {
                console.error('카테고리 로드 실패:', response.status);
                return;
            }

            const categories = await response.json();
            const menuList = document.getElementById('boardMenuList');

            if (!menuList) {
                console.error('boardMenuList 요소를 찾을 수 없습니다');
                return;
            }

            if (categories && categories.length > 0) {
                // 활성화된 카테고리만 필터링하고 sort_order로 정렬
                const activeCategories = categories
                    .filter(cat => cat.is_active)
                    .sort((a, b) => a.sort_order - b.sort_order);

                menuList.innerHTML = activeCategories.map(cat => {
                    const isActive = cat.slug === CURRENT_SLUG ? ' active' : '';
                    // 그룹 헤더인 경우
                    if (cat.is_group) {
                        return `
                            <div class="sidebar-header" style="margin-top: 20px;">
                                <span class="korean-text">${cat.name_ko || cat.slug}</span>
                                <div class="russian-text">${cat.name_ru || ''}</div>
                            </div>
                        `;
                    }

                    // layout_type에 따라 페이지 URL 결정
                    const isContactForm = cat.layout_type === 'form';
                    const pageUrl = isContactForm ? `/contact-${cat.slug}.html` : `/board-${cat.slug}.html`;

                    // 일반 게시판 또는 문의 양식
                    return `
                        <a href="${pageUrl}" class="sidebar-item${isActive}">
                            <span class="korean-text">${cat.icon || '📋'} ${cat.name_ko || cat.slug}</span>
                            <div class="russian-text">${cat.name_ru || ''}</div>
                        </a>
                    `;
                }).join('');
            } else {
                menuList.innerHTML = `
                    <div style="padding: 20px; text-align: center; color: #999;">
                        <span class="korean-text">게시판이 없습니다</span><br>
                        <span class="russian-text">Нет досок</span>
                    </div>
                `;
            }
        } catch (error) {
            console.error('게시판 메뉴 로드 오류:', error);
            const menuList = document.getElementById('boardMenuList');
            if (menuList) {
                menuList.innerHTML = `
                    <div style="padding: 20px; text-align: center; color: #f44336;">
                        <span class="korean-text">로드 실패</span><br>
                        <span class="russian-text">Ошибка загрузки</span>
                    </div>
                `;
            }
        }
    }

    // 현재 언어 설정 적용 (강제 적용)
    function applyCurrentLanguage() {
        let savedLang = localStorage.getItem('preferredLang');

        // localStorage에 없으면 기본값 설정하고 저장
        if (!savedLang) {
            savedLang = 'ko'; // 기본값을 한국어로 변경
            localStorage.setItem('preferredLang', savedLang);
            console.log('[Sidebar] 언어 설정 초기화:', savedLang);
        }

        // 강제로 body 속성 설정
        document.body.setAttribute('data-lang', savedLang);

        // 다시 한번 확인하고 설정 (확실하게)
        setTimeout(() => {
            document.body.setAttribute('data-lang', savedLang);
        }, 50);

        console.log('[Sidebar] 언어 설정 적용:', savedLang, '→', document.body.getAttribute('data-lang'));

        // 언어 버튼에도 active 클래스 적용
        document.querySelectorAll('.lang-btn').forEach(btn => {
            btn.classList.remove('active');
            if (btn.dataset.lang === savedLang) {
                btn.classList.add('active');
            }
        });
    }

    // 언어 전환 버튼 이벤트 리스너 추가 (기존 리스너 제거 후 추가)
    function setupLanguageListeners() {
        const buttons = document.querySelectorAll('.lang-btn');
        console.log('[Sidebar] 언어 버튼 개수:', buttons.length);

        buttons.forEach((btn, index) => {
            // 기존 이벤트 복제본 생성 (기존 리스너 제거 위해)
            const newBtn = btn.cloneNode(true);
            btn.parentNode.replaceChild(newBtn, btn);

            // 새 이벤트 리스너 추가
            newBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();

                const lang = this.dataset.lang;
                console.log('[Sidebar] 언어 버튼 클릭:', lang);

                // 모든 버튼에서 active 제거
                document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));

                // 클릭된 버튼에 active 추가
                this.classList.add('active');

                // body에 data-lang 속성 설정
                document.body.setAttribute('data-lang', lang);

                // localStorage에 저장
                localStorage.setItem('preferredLang', lang);

                // 스타일 즉시 적용
                applyLanguageStylesDirect(lang);

                console.log('[Sidebar] 언어 변경 완료:', lang, '→', document.body.getAttribute('data-lang'));
            }, true);
        });

        console.log('[Sidebar] 언어 버튼 이벤트 리스너 설정 완료');
    }

    // 언어 스타일 직접 적용
    function applyLanguageStylesDirect(lang) {
        if (lang === 'ko') {
            // 한국어만 표시
            document.querySelectorAll('.russian-text, .russian-label, .russian-subtitle, .russian-title').forEach(el => {
                el.style.display = 'none';
            });
            document.querySelectorAll('.korean-text, .korean-label, .korean-subtitle, .korean-title').forEach(el => {
                el.style.display = '';
            });
        } else if (lang === 'ru') {
            // 러시아어만 표시
            document.querySelectorAll('.korean-text, .korean-label, .korean-subtitle, .korean-title').forEach(el => {
                el.style.display = 'none';
            });
            document.querySelectorAll('.russian-text, .russian-label, .russian-subtitle, .russian-title').forEach(el => {
                el.style.display = '';
            });
        } else {
            // 둘 다 표시
            document.querySelectorAll('.korean-text, .korean-label, .korean-subtitle, .korean-title, .russian-text, .russian-label, .russian-subtitle, .russian-title').forEach(el => {
                el.style.display = '';
            });
        }
        console.log('[Sidebar] 언어 스타일 적용:', lang);
    }

    // 메인 실행
    try {
        console.log('[Sidebar] 초기화 시작...');
        const sidebarContainer = document.getElementById('sidebar-container');
        if (!sidebarContainer) {
            console.error('[Sidebar] sidebar-container 요소를 찾을 수 없습니다');
            return;
        }

        console.log('[Sidebar] sidebar-container 발견, HTML 삽입 중...');
        // 사이드바 HTML 삽입
        sidebarContainer.innerHTML = createSidebarHTML();

        console.log('[Sidebar] 메뉴 로드 시작...');
        // 메뉴 로드
        await loadBoardMenu();

        // 언어 설정 적용
        applyCurrentLanguage();

        // 사이드바에 언어 스타일 즉시 적용
        const currentLang = localStorage.getItem('preferredLang') || 'ko';
        applyLanguageStylesDirect(currentLang);

        // 언어 전환 버튼 이벤트 리스너 설정
        setupLanguageListeners();

        // 사이드바 로드 완료 이벤트 발생
        document.dispatchEvent(new Event('sidebarLoaded'));

        console.log('[Sidebar] 초기화 완료!');
    } catch (error) {
        console.error('[Sidebar] 초기화 오류:', error);
    }
}

// DOMContentLoaded 이벤트 후 실행
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSidebar);
} else {
    // 이미 DOM이 로드된 경우 즉시 실행
    initSidebar();
}
