# 배포 가이드

이 문서는 Russki.Center 웹사이트를 playground.io.kr 서버에 배포하는 방법을 설명합니다.

## 1. SSL 인증서 설정

서버에서 다음 명령어를 실행하여 SSL 인증서를 설정하세요:

```bash
chmod +x ssl_setup.sh
sudo ./ssl_setup.sh
```

이 스크립트는 다음 작업을 수행합니다:
- Let's Encrypt SSL 인증서 발급
- Nginx 설정 자동화
- HTTPS 리다이렉션 설정
- 자동 갱신 설정

## 2. 프론트엔드 파일 업로드

### 방법 1: FTP 업로드 (권장)

```bash
# FTP 정보 설정
export FTP_USER="your_username"
export FTP_PASS="your_password"

# 업로드 실행
python ftp_upload.py
```

### 방법 2: SCP/SFTP 업로드

```bash
# 프론트엔드 파일 복사
scp -r ../frontend/public/* user@playground.io.kr:/var/www/playground.io.kr/
```

### 방법 3: 서버에서 직접 복사

서버에 직접 접속하여 파일을 복사할 수 있습니다:

```bash
# 서버에서 실행
sudo cp /path/to/frontend/public/* /var/www/playground.io.kr/
sudo chown -R www-data:www-data /var/www/playground.io.kr
```

## 3. 백엔드 서버 설정

백엔드 서버를 프로덕션 모드로 실행:

```bash
cd ../backend
pip install -r requirements.txt

# 환경변수 설정
export ENVIRONMENT=production
export DATABASE_URL="postgresql://user:pass@localhost/kru_community"
export SECRET_KEY="your-secret-key"

# 서버 시작 (systemd 서비스로 설정 권장)
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 4. 도메인 설정 확인

- DNS A 레코드가 서버 IP를 가리키는지 확인
- `dig playground.io.kr` 명령어로 DNS 설정 확인

## 5. 테스트

배포 후 다음을 확인하세요:

1. **HTTPS 접속**: https://playground.io.kr
2. **HTTP→HTTPS 리다이렉션**: http://playground.io.kr
3. **API 엔드포인트**: https://playground.io.kr/api/
4. **정적 파일 로딩**: CSS, JavaScript 파일들이 정상 로드되는지 확인

## 6. 모니터링

- Nginx 로그: `/var/log/nginx/access.log`, `/var/log/nginx/error.log`
- SSL 인증서 만료: `sudo certbot certificates`
- 백엔드 서버 상태: `systemctl status your-backend-service`

## 7. 유지보수

### SSL 인증서 수동 갱신
```bash
sudo certbot renew
sudo systemctl reload nginx
```

### 로그 정리
```bash
sudo logrotate -f /etc/logrotate.d/nginx
```

### 캐시 정리 (필요시)
```bash
# 브라우저 캐시를 무력화하려면 CSS/JS 파일명에 버전 추가
# 예: style.css?v=1.0.1
```

## 문제 해결

### SSL 인증서 문제
- `sudo nginx -t`: Nginx 설정 검증
- `sudo certbot certificates`: 인증서 상태 확인
- `sudo systemctl status nginx`: Nginx 서비스 상태

### 파일 권한 문제
```bash
sudo chown -R www-data:www-data /var/www/playground.io.kr
sudo chmod -R 755 /var/www/playground.io.kr
```

### API 연결 문제
- 백엔드 서버가 실행 중인지 확인
- 방화벽에서 8000 포트가 열려있는지 확인
- Nginx 프록시 설정 확인