# KRU Community 배포 가이드

## 목차
1. [사전 준비](#사전-준비)
2. [환경 설정](#환경-설정)
3. [Docker 배포](#docker-배포)
4. [프로덕션 배포](#프로덕션-배포)
5. [모니터링 설정](#모니터링-설정)
6. [백업 전략](#백업-전략)
7. [트러블슈팅](#트러블슈팅)

## 사전 준비

### 필수 요구사항
- Docker 20.10+ 및 Docker Compose 2.0+
- PostgreSQL 15+
- Redis 7+
- Node.js 18+ (개발용)
- Python 3.11+ (개발용)
- 도메인 및 SSL 인증서

### 추천 서버 사양
- **최소**: 2 vCPU, 4GB RAM, 20GB SSD
- **권장**: 4 vCPU, 8GB RAM, 50GB SSD
- **프로덕션**: 8 vCPU, 16GB RAM, 100GB SSD

### 필수 API 키
- Google Cloud Translation API
- Google OAuth 2.0
- Kakao OAuth
- VK OAuth
- AWS S3 (파일 저장용)
- SMTP 서버 (이메일 발송용)

## 환경 설정

### 1. 저장소 클론
```bash
git clone https://github.com/your-repo/kru-community.git
cd kru-community
```

### 2. 환경 변수 설정

#### Backend (.env)
```bash
cp backend/.env.example backend/.env
```

필수 환경 변수:
```env
# 데이터베이스
DATABASE_URL=postgresql://kru_user:strong_password@localhost:5432/kru_community
REDIS_URL=redis://localhost:6379/0

# 보안
SECRET_KEY=your-very-long-random-secret-key-minimum-32-chars
ALGORITHM=HS256

# OAuth 설정
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
KAKAO_CLIENT_ID=your-kakao-client-id
KAKAO_CLIENT_SECRET=your-kakao-client-secret
VK_APP_ID=your-vk-app-id
VK_APP_SECRET=your-vk-app-secret

# Google Cloud Translation
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/google-cloud-key.json

# AWS S3
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_S3_BUCKET_NAME=kru-community-files
AWS_S3_REGION=ap-northeast-2

# 이메일
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# 프로덕션 설정
ENVIRONMENT=production
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

#### Frontend (.env.local)
```bash
cp frontend/.env.example frontend/.env.local
```

```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_SITE_URL=https://yourdomain.com
```

### 3. SSL 인증서 설정

Let's Encrypt를 사용한 무료 SSL:
```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## Docker 배포

### 1. Docker 이미지 빌드
```bash
docker-compose build
```

### 2. 데이터베이스 초기화
```bash
# PostgreSQL 컨테이너 시작
docker-compose up -d postgres

# 데이터베이스 마이그레이션
docker-compose run backend alembic upgrade head

# 초기 데이터 시드 (카테고리, 관리자 계정 등)
docker-compose run backend python scripts/seed_data.py
```

### 3. 전체 서비스 시작
```bash
docker-compose up -d
```

### 4. 상태 확인
```bash
docker-compose ps
docker-compose logs -f
```

## 프로덕션 배포

### AWS EC2 배포

#### 1. EC2 인스턴스 생성
- Ubuntu 22.04 LTS
- t3.medium 이상
- 보안 그룹: 80, 443, 22 포트 열기

#### 2. 서버 설정
```bash
# Docker 설치
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Docker Compose 설치
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 프로젝트 클론 및 설정
git clone https://github.com/your-repo/kru-community.git
cd kru-community
```

#### 3. Nginx 설정
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    client_max_body_size 10M;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/kru-community/static;
        expires 30d;
    }

    location /media {
        alias /var/www/kru-community/media;
        expires 30d;
    }
}
```

### Kubernetes 배포 (선택사항)

#### Helm Chart 사용
```bash
helm install kru-community ./k8s/helm \
  --set image.tag=latest \
  --set ingress.hosts[0].host=yourdomain.com \
  --set postgresql.auth.password=your-db-password
```

## 모니터링 설정

### 1. Prometheus + Grafana
```yaml
# docker-compose.monitoring.yml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana:latest
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
    ports:
      - "3001:3000"
```

### 2. 로그 수집 (ELK Stack)
```bash
docker-compose -f docker-compose.elk.yml up -d
```

### 3. 헬스체크 설정
```bash
# 헬스체크 스크립트
curl -f http://localhost:8000/health || exit 1
curl -f http://localhost:3000/api/health || exit 1
```

### 4. Uptime 모니터링
- UptimeRobot 또는 Pingdom 설정
- 알림: Slack, Email, SMS

## 백업 전략

### 1. 데이터베이스 백업
```bash
# 일일 백업 스크립트 (cron)
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker exec kru_postgres pg_dump -U kru_user kru_community | gzip > /backups/db_$DATE.sql.gz

# S3 업로드
aws s3 cp /backups/db_$DATE.sql.gz s3://your-backup-bucket/db/

# 7일 이상 된 백업 삭제
find /backups -name "db_*.sql.gz" -mtime +7 -delete
```

### 2. 파일 백업
```bash
# S3 동기화
aws s3 sync /var/www/kru-community/media s3://your-backup-bucket/media/
```

### 3. 복구 절차
```bash
# 데이터베이스 복구
gunzip < /backups/db_20250127.sql.gz | docker exec -i kru_postgres psql -U kru_user kru_community

# 파일 복구
aws s3 sync s3://your-backup-bucket/media/ /var/www/kru-community/media/
```

## 트러블슈팅

### 일반적인 문제 해결

#### 1. Docker 컨테이너 재시작
```bash
docker-compose restart backend
docker-compose restart frontend
```

#### 2. 로그 확인
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

#### 3. 데이터베이스 연결 문제
```bash
# 연결 테스트
docker exec -it kru_postgres psql -U kru_user -d kru_community

# 연결 수 확인
SELECT count(*) FROM pg_stat_activity;
```

#### 4. Redis 연결 문제
```bash
docker exec -it kru_redis redis-cli ping
```

#### 5. 디스크 공간 확인
```bash
df -h
docker system df
docker system prune -a
```

### 성능 최적화

#### 1. PostgreSQL 튜닝
```sql
-- postgresql.conf
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
```

#### 2. Redis 최적화
```conf
# redis.conf
maxmemory 512mb
maxmemory-policy allkeys-lru
```

#### 3. Next.js 최적화
```javascript
// next.config.js
module.exports = {
  images: {
    domains: ['your-s3-bucket.s3.amazonaws.com'],
    minimumCacheTTL: 60,
  },
  compress: true,
  poweredByHeader: false,
}
```

## 보안 체크리스트

- [ ] 모든 환경 변수가 안전하게 설정됨
- [ ] SSL/TLS 인증서 설치 및 자동 갱신 설정
- [ ] 방화벽 규칙 설정 (필요한 포트만 열기)
- [ ] 정기적인 보안 업데이트
- [ ] 비밀번호 정책 적용
- [ ] Rate limiting 설정
- [ ] WAF (Web Application Firewall) 설정
- [ ] 정기적인 백업 및 복구 테스트
- [ ] 로그 모니터링 및 이상 탐지
- [ ] OWASP Top 10 대응

## 지원 및 문의

- 기술 지원: tech@kru-community.com
- 문서: https://docs.kru-community.com
- GitHub Issues: https://github.com/your-repo/kru-community/issues