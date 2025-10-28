// 서버 환경 설정
const CONFIG = {
    // 로컬 개발 환경
    development: {
        API_URL: 'http://localhost:8000',
        BASE_URL: 'http://localhost:3000'
    },
    // 프로덕션 환경 (실제 서버)
    production: {
        API_URL: 'https://playground.io.kr/api',
        BASE_URL: 'https://playground.io.kr'
    }
};

// 현재 환경 감지
const isProduction = window.location.hostname !== 'localhost';
const currentConfig = isProduction ? CONFIG.production : CONFIG.development;

// 전역 설정 변수
window.APP_CONFIG = currentConfig;