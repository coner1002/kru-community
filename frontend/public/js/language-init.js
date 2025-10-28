// 언어 설정 즉시 적용 (페이지 로드 전)
(function() {
    // localStorage에서 언어 설정 가져오기
    let savedLang = localStorage.getItem('preferredLang');

    // 없으면 기본값 한국어로 설정
    if (!savedLang) {
        savedLang = 'ko';
        localStorage.setItem('preferredLang', savedLang);
    }

    // 즉시 body에 속성 설정
    document.documentElement.setAttribute('data-lang', savedLang);
    if (document.body) {
        document.body.setAttribute('data-lang', savedLang);
    }

    console.log('[Language Init] 언어 설정:', savedLang);

    // 언어 강제 적용 (100ms마다 체크)
    setInterval(function() {
        const lang = localStorage.getItem('preferredLang') || 'ko';
        if (lang === 'ko') {
            // 한국어만 표시 - 러시아어 숨김
            document.querySelectorAll('.russian-text, .russian-label, .russian-subtitle, .russian-title').forEach(el => {
                el.style.display = 'none';
                el.style.visibility = 'hidden';
                el.style.height = '0';
                el.style.overflow = 'hidden';
                el.style.margin = '0';
                el.style.padding = '0';
            });
            // 한국어 표시
            document.querySelectorAll('.korean-text, .korean-label, .korean-subtitle, .korean-title').forEach(el => {
                el.style.display = '';
                el.style.visibility = '';
                el.style.height = '';
                el.style.overflow = '';
                el.style.margin = '';
                el.style.padding = '';
            });
        } else if (lang === 'ru') {
            // 러시아어만 표시 - 한국어 숨김
            document.querySelectorAll('.korean-text, .korean-label, .korean-subtitle, .korean-title').forEach(el => {
                el.style.display = 'none';
                el.style.visibility = 'hidden';
                el.style.height = '0';
                el.style.overflow = 'hidden';
                el.style.margin = '0';
                el.style.padding = '0';
            });
            // 러시아어 표시
            document.querySelectorAll('.russian-text, .russian-label, .russian-subtitle, .russian-title').forEach(el => {
                el.style.display = '';
                el.style.visibility = '';
                el.style.height = '';
                el.style.overflow = '';
                el.style.margin = '';
                el.style.padding = '';
            });
        } else {
            // both - 둘 다 표시
            document.querySelectorAll('.korean-text, .korean-label, .korean-subtitle, .korean-title, .russian-text, .russian-label, .russian-subtitle, .russian-title').forEach(el => {
                el.style.display = '';
                el.style.visibility = '';
                el.style.height = '';
                el.style.overflow = '';
                el.style.margin = '';
                el.style.padding = '';
            });
        }
    }, 100);

    // DOM 로드 후 언어 적용 강제 실행
    function applyLanguageStyles() {
        const lang = document.body.getAttribute('data-lang') || 'ko';

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

        console.log('[Language Init] 스타일 적용 완료:', lang);
    }

    // DOM 로드 후 실행
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', applyLanguageStyles);
    } else {
        applyLanguageStyles();
    }

    // 사이드바 로드 후에도 다시 적용
    document.addEventListener('sidebarLoaded', applyLanguageStyles);

    // 여러 시점에 적용 (확실하게)
    setTimeout(applyLanguageStyles, 100);
    setTimeout(applyLanguageStyles, 500);
    setTimeout(applyLanguageStyles, 1000);
    setTimeout(applyLanguageStyles, 2000);

    // MutationObserver로 DOM 변경 감지
    if (typeof MutationObserver !== 'undefined') {
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.addedNodes.length > 0) {
                    // 새로운 노드가 추가되면 언어 스타일 적용
                    applyLanguageStyles();
                }
            });
        });

        // body 감시 시작
        setTimeout(() => {
            if (document.body) {
                observer.observe(document.body, {
                    childList: true,
                    subtree: true
                });
                console.log('[Language Init] MutationObserver 시작');
            }
        }, 100);
    }
})();
