# 데이터베이스 백업 및 복원 가이드

## 🔄 자동 백업 설정

### Windows (작업 스케줄러)

1. **작업 스케줄러 열기**
   - `Win + R` → `taskschd.msc` 입력

2. **새 작업 만들기**
   - 작업 만들기 → 일반 탭
   - 이름: `KRU Community DB Backup`
   - 설명: `매일 자동 백업`

3. **트리거 설정**
   - 트리거 탭 → 새로 만들기
   - 매일, 오전 3시

4. **동작 설정**
   - 동작 탭 → 새로 만들기
   - 프로그램: `C:\Program Files\Git\bin\bash.exe`
   - 인수 추가: `"G:\내 드라이브\#Python\러시아커뮤니티사이트\kru-community\scripts\backup_database.sh"`
   - 시작 위치: `G:\내 드라이브\#Python\러시아커뮤니티사이트\kru-community`

### Linux/Mac (cron)

```bash
# crontab 편집
crontab -e

# 매일 오전 3시 백업
0 3 * * * cd /path/to/kru-community && bash scripts/backup_database.sh >> logs/backup.log 2>&1
```

## 💾 수동 백업

### 백업 실행
```bash
cd "G:\내 드라이브\#Python\러시아커뮤니티사이트\kru-community"
bash scripts/backup_database.sh
```

### 백업 파일 위치
- Windows: `G:\내 드라이브\#Python\러시아커뮤니티사이트\kru-community\backups\`
- Linux/Mac: `/var/backups/postgres/`

### 백업 파일 형식
```
kru_community_20251001_150000.sql.gz
├── kru_community: 데이터베이스 이름
├── 20251001: 날짜 (YYYYMMDD)
├── 150000: 시간 (HHMMSS)
└── .sql.gz: 압축된 SQL 파일
```

## ♻️ 복원 방법

### 1. 백업 파일 목록 확인
```bash
bash scripts/restore_database.sh
```

### 2. 특정 백업 파일로 복원
```bash
bash scripts/restore_database.sh /var/backups/postgres/kru_community_20251001_150000.sql.gz
```

⚠️ **경고**: 복원 시 기존 데이터가 모두 삭제됩니다!

## 📊 백업 정책

- **백업 주기**: 매일 1회 (오전 3시)
- **보관 기간**: 최근 7일
- **백업 방식**: 압축 (gzip)
- **자동 정리**: 7일 이상 된 백업 자동 삭제

## 🔍 백업 확인

### 최근 백업 목록 보기
```bash
ls -lh backups/kru_community_*.sql.gz
```

### 백업 파일 크기 확인
```bash
du -sh backups/
```

### 백업 파일 내용 미리보기
```bash
gunzip -c backups/kru_community_20251001_150000.sql.gz | head -n 50
```

## 🚨 긴급 복구 절차

### 1. 최신 백업 찾기
```bash
ls -t backups/kru_community_*.sql.gz | head -1
```

### 2. 즉시 복원
```bash
LATEST=$(ls -t backups/kru_community_*.sql.gz | head -1)
bash scripts/restore_database.sh $LATEST
```

### 3. 데이터 확인
```bash
docker-compose exec postgres psql -U kru_user -d kru_community -c "SELECT COUNT(*) FROM users;"
docker-compose exec postgres psql -U kru_user -d kru_community -c "SELECT COUNT(*) FROM posts;"
```

## 💡 권장 사항

1. **외부 백업**: 중요한 데이터는 추가로 클라우드에 백업
   - Google Drive, Dropbox, AWS S3 등

2. **백업 테스트**: 정기적으로 복원 테스트 수행
   - 월 1회 테스트 환경에서 복원 확인

3. **모니터링**: 백업 실패 알림 설정
   - 백업 로그 확인
   - 디스크 용량 모니터링

4. **보안**: 백업 파일 암호화 고려
   - 민감한 개인정보 포함 시 필수

## 📝 백업 로그

백업 실행 시 로그가 자동으로 기록됩니다:

```bash
# 로그 확인
tail -f logs/backup.log

# 최근 백업 이력
grep "백업 성공" logs/backup.log | tail -10
```
