# 데이터베이스 관리 가이드

## 📊 pgAdmin 접속

웹 브라우저에서 데이터베이스를 GUI로 관리할 수 있습니다.

### 접속 정보
- **URL**: http://localhost:5050
- **Email**: admin@russki.center
- **Password**: admin1234

### 서버 등록

1. **pgAdmin 접속** 후 `Add New Server` 클릭

2. **General 탭**
   - Name: `KRU Community`

3. **Connection 탭**
   - Host: `postgres` (Docker 내부 네트워크)
   - Port: `5432`
   - Database: `kru_community`
   - Username: `kru_user`
   - Password: `password` (또는 .env의 DB_PASSWORD)

4. **Save** 클릭

## 🌱 초기 데이터 생성

### 1. 최소 데이터 (관리자 + 카테고리)
```bash
cd "G:\내 드라이브\#Python\러시아커뮤니티사이트\kru-community"
python scripts/seed_data.py --minimal
```

### 2. 전체 필수 데이터
```bash
python scripts/seed_data.py
```

### 3. 테스트 데이터 포함
```bash
python scripts/seed_data.py --test-data
```

생성되는 데이터:
- ✅ 관리자 계정 (admin1234 / kuro##@@)
- ✅ 기본 카테고리 8개
- ✅ 테스트 사용자 3명 (--test-data)
- ✅ 샘플 파트너 2개 (--test-data)

## 📋 데이터베이스 테이블 구조

### 사용자 관련
- `users` - 회원 정보
- `sessions` - 로그인 세션
- `email_verifications` - 이메일 인증
- `sms_verifications` - SMS 인증

### 게시판 관련
- `categories` - 카테고리
- `posts` - 게시글
- `comments` - 댓글
- `post_likes` - 게시글 좋아요
- `comment_likes` - 댓글 좋아요
- `bookmarks` - 북마크
- `reports` - 신고

### 파트너 관련
- `partners` - 파트너 정보
- `partner_reviews` - 파트너 리뷰

### 시스템 관련
- `audit_logs` - 감사 로그
- `banners` - 배너
- `blocked_keywords` - 금지어
- `system_notices` - 시스템 공지

## 🔍 유용한 SQL 쿼리

### 사용자 통계
```sql
-- 전체 사용자 수
SELECT COUNT(*) FROM users;

-- 역할별 사용자 수
SELECT role, COUNT(*) FROM users GROUP BY role;

-- 최근 가입자 10명
SELECT username, nickname, created_at
FROM users
ORDER BY created_at DESC
LIMIT 10;
```

### 게시판 통계
```sql
-- 카테고리별 게시글 수
SELECT c.name_ko, COUNT(p.id) as post_count
FROM categories c
LEFT JOIN posts p ON c.id = p.category_id
GROUP BY c.id, c.name_ko
ORDER BY post_count DESC;

-- 인기 게시글 (조회수 기준)
SELECT title, view_count, like_count, comment_count
FROM posts
WHERE status = 'published'
ORDER BY view_count DESC
LIMIT 10;

-- 최근 댓글
SELECT u.nickname, c.content, c.created_at
FROM comments c
JOIN users u ON c.user_id = u.id
WHERE c.is_deleted = false
ORDER BY c.created_at DESC
LIMIT 10;
```

### 활동 통계
```sql
-- 일별 게시글 수
SELECT DATE(created_at) as date, COUNT(*) as posts
FROM posts
WHERE created_at > CURRENT_DATE - INTERVAL '30 days'
GROUP BY DATE(created_at)
ORDER BY date DESC;

-- 활동적인 사용자 TOP 10
SELECT u.username, u.nickname,
       COUNT(DISTINCT p.id) as post_count,
       COUNT(DISTINCT c.id) as comment_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
LEFT JOIN comments c ON u.id = c.user_id
GROUP BY u.id, u.username, u.nickname
ORDER BY (post_count + comment_count) DESC
LIMIT 10;
```

## 🛠️ 데이터베이스 유지보수

### VACUUM 실행 (디스크 공간 최적화)
```sql
VACUUM ANALYZE;
```

### 인덱스 재구축
```sql
REINDEX DATABASE kru_community;
```

### 연결 확인
```sql
SELECT * FROM pg_stat_activity;
```

### 데이터베이스 크기 확인
```sql
SELECT pg_size_pretty(pg_database_size('kru_community'));
```

### 테이블별 크기 확인
```sql
SELECT
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

## 🚨 문제 해결

### 연결 실패
```bash
# PostgreSQL 컨테이너 상태 확인
docker-compose ps postgres

# 로그 확인
docker-compose logs postgres --tail 50

# 재시작
docker-compose restart postgres
```

### 테이블 누락
```bash
# 백엔드 재시작 (테이블 자동 생성)
docker-compose restart backend

# 로그 확인
docker-compose logs backend | grep -i "table\|error"
```

### 데이터 초기화
```bash
# ⚠️ 경고: 모든 데이터 삭제됨
docker-compose exec postgres psql -U kru_user -d kru_community -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# 백엔드 재시작 (테이블 재생성)
docker-compose restart backend

# 초기 데이터 생성
python scripts/seed_data.py --test-data
```

## 📈 모니터링

### 느린 쿼리 로깅 활성화
```sql
ALTER SYSTEM SET log_min_duration_statement = 1000; -- 1초 이상
SELECT pg_reload_conf();
```

### 쿼리 통계
```sql
-- pg_stat_statements 확장 설치 (한 번만)
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- 느린 쿼리 TOP 10
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
```

### 연결 수 모니터링
```sql
SELECT max_conn, used, res_for_super, max_conn-used-res_for_super AS res_for_normal
FROM
  (SELECT count(*) used FROM pg_stat_activity) t1,
  (SELECT setting::int res_for_super FROM pg_settings WHERE name='superuser_reserved_connections') t2,
  (SELECT setting::int max_conn FROM pg_settings WHERE name='max_connections') t3;
```

## 🔐 보안

### 비밀번호 변경
```sql
ALTER USER kru_user WITH PASSWORD 'new_password';
```

### 권한 확인
```sql
\du  -- 사용자 목록
\dp  -- 테이블 권한
```

### SSL 연결 (프로덕션 권장)
```yaml
# docker-compose.yml
postgres:
  command:
    - -c
    - ssl=on
    - -c
    - ssl_cert_file=/var/lib/postgresql/server.crt
    - -c
    - ssl_key_file=/var/lib/postgresql/server.key
```

## 💾 백업/복원

자세한 내용은 [README_BACKUP.md](./README_BACKUP.md) 참고
