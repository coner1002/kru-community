// 토큰 관리 및 자동 갱신 스크립트

(function() {
    const API_BASE = 'http://localhost:8000';

    // 토큰 만료 확인 함수
    function isTokenExpired(token) {
        if (!token) return true;

        try {
            // JWT 토큰 디코딩 (payload 부분)
            const parts = token.split('.');
            if (parts.length !== 3) return true;

            const payload = JSON.parse(atob(parts[1]));
            const exp = payload.exp;

            if (!exp) return true;

            // 현재 시간과 비교 (5분 여유)
            const now = Math.floor(Date.now() / 1000);
            return exp < (now + 300); // 5분 이내 만료 예정이면 true
        } catch (e) {
            console.error('토큰 디코딩 오류:', e);
            return true;
        }
    }

    // 토큰 갱신 함수
    async function refreshToken() {
        const refreshToken = localStorage.getItem('refresh_token');

        if (!refreshToken) {
            console.log('[Token] Refresh token 없음, 로그아웃 처리');
            logout();
            return null;
        }

        try {
            console.log('[Token] Access token 갱신 시도...');
            const response = await fetch(`${API_BASE}/api/auth/refresh`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ refresh_token: refreshToken })
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('access_token', data.access_token);

                // userInfo 업데이트
                const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}');
                userInfo.access_token = data.access_token;
                localStorage.setItem('userInfo', JSON.stringify(userInfo));

                console.log('[Token] Access token 갱신 성공');
                return data.access_token;
            } else {
                console.error('[Token] Refresh token 만료 또는 무효');
                logout();
                return null;
            }
        } catch (error) {
            console.error('[Token] 갱신 오류:', error);
            logout();
            return null;
        }
    }

    // 로그아웃 처리
    function logout() {
        console.log('[Token] 로그아웃 처리');
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('userInfo');

        // 로그인 페이지가 아니면 리다이렉트
        if (!window.location.pathname.includes('login.html') &&
            !window.location.pathname.includes('index.html')) {
            alert('로그인 세션이 만료되었습니다. 다시 로그인해주세요.\n\nСессия истекла. Пожалуйста, войдите снова.');
            window.location.href = '/login.html';
        }
    }

    // 주기적으로 토큰 확인 (5분마다)
    function startTokenCheck() {
        setInterval(async function() {
            const accessToken = localStorage.getItem('access_token');

            if (accessToken && isTokenExpired(accessToken)) {
                console.log('[Token] Access token 만료 감지, 갱신 시도');
                await refreshToken();
            }
        }, 5 * 60 * 1000); // 5분
    }

    // API 요청 인터셉터 (fetch 래퍼)
    window.authenticatedFetch = async function(url, options = {}) {
        let accessToken = localStorage.getItem('access_token');

        // 토큰 만료 확인
        if (accessToken && isTokenExpired(accessToken)) {
            console.log('[Token] 만료된 토큰 감지, 갱신 중...');
            accessToken = await refreshToken();

            if (!accessToken) {
                throw new Error('Token refresh failed');
            }
        }

        // Authorization 헤더 추가
        options.headers = options.headers || {};
        if (accessToken) {
            options.headers['Authorization'] = `Bearer ${accessToken}`;
        }

        return fetch(url, options);
    };

    // 페이지 로드 시 토큰 확인
    document.addEventListener('DOMContentLoaded', async function() {
        const accessToken = localStorage.getItem('access_token');

        if (accessToken && isTokenExpired(accessToken)) {
            console.log('[Token] 페이지 로드 시 만료된 토큰 감지');
            await refreshToken();
        }

        // 주기적 체크 시작
        startTokenCheck();
    });

    console.log('[Token Manager] 초기화 완료');
})();
