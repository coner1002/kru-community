#!/bin/bash

# Let's Encrypt SSL 인증서 설정 스크립트
# playground.io.kr 도메인용

echo "=== Let's Encrypt SSL 인증서 설정 ==="

# 필수 패키지 설치
echo "1. 필수 패키지 설치 중..."
sudo apt update
sudo apt install -y certbot python3-certbot-nginx nginx

# Nginx 설정 확인
echo "2. Nginx 설정 확인 중..."
sudo nginx -t

# 방화벽 설정
echo "3. 방화벽 설정 중..."
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh

# Let's Encrypt 인증서 발급
echo "4. SSL 인증서 발급 중..."
echo "도메인: playground.io.kr"

# 웹루트 방식으로 인증서 발급
sudo certbot --nginx -d playground.io.kr --email admin@playground.io.kr --agree-tos --no-eff-email

# 자동 갱신 설정
echo "5. 자동 갱신 설정 중..."
sudo crontab -l > current_cron 2>/dev/null || true
echo "0 12 * * * /usr/bin/certbot renew --quiet" >> current_cron
sudo crontab current_cron
rm current_cron

# Nginx 설정 파일 생성
echo "6. Nginx 설정 파일 업데이트 중..."
sudo tee /etc/nginx/sites-available/playground.io.kr > /dev/null <<EOF
server {
    listen 80;
    server_name playground.io.kr www.playground.io.kr;
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name playground.io.kr www.playground.io.kr;

    # SSL 설정
    ssl_certificate /etc/letsencrypt/live/playground.io.kr/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/playground.io.kr/privkey.pem;

    # SSL 보안 설정
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA:ECDHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES256-SHA256:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:DES-CBC3-SHA;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # HSTS 설정
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # 정적 파일 서빙
    root /var/www/playground.io.kr;
    index index.html index.htm;

    # 정적 파일 캐싱
    location ~* \.(css|js|jpg|jpeg|png|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # API 프록시 (백엔드 서버로 전달)
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }

    # 메인 페이지
    location / {
        try_files \$uri \$uri/ /index.html;
    }

    # Gzip 압축
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;
}
EOF

# 웹 루트 디렉토리 생성
echo "7. 웹 루트 디렉토리 설정 중..."
sudo mkdir -p /var/www/playground.io.kr
sudo chown -R www-data:www-data /var/www/playground.io.kr
sudo chmod -R 755 /var/www/playground.io.kr

# 사이트 활성화
echo "8. 사이트 활성화 중..."
sudo ln -sf /etc/nginx/sites-available/playground.io.kr /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Nginx 재시작
echo "9. Nginx 재시작 중..."
sudo nginx -t && sudo systemctl reload nginx

echo "=== SSL 설정 완료 ==="
echo "브라우저에서 https://playground.io.kr 로 접속해보세요."
echo ""
echo "참고사항:"
echo "- 인증서는 90일마다 자동 갱신됩니다"
echo "- 프론트엔드 파일은 /var/www/playground.io.kr 에 업로드하세요"
echo "- 백엔드 API는 자동으로 /api/ 경로로 프록시됩니다"