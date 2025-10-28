#!/bin/bash

# PostgreSQL 데이터베이스 자동 백업 스크립트
# 매일 실행되며 최근 7일 백업만 보관

# 설정
BACKUP_DIR="/var/backups/postgres"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DB_NAME="kru_community"
DB_USER="kru_user"
RETENTION_DAYS=7

# 백업 디렉토리 생성
mkdir -p $BACKUP_DIR

# 백업 파일명
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.sql.gz"

echo "==================================="
echo "PostgreSQL 백업 시작"
echo "시간: $(date)"
echo "==================================="

# pg_dump로 백업 (압축)
docker-compose exec -T postgres pg_dump -U $DB_USER -d $DB_NAME | gzip > $BACKUP_FILE

# 백업 성공 여부 확인
if [ $? -eq 0 ]; then
    echo "✅ 백업 성공: $BACKUP_FILE"

    # 파일 크기 확인
    FILESIZE=$(du -h $BACKUP_FILE | cut -f1)
    echo "파일 크기: $FILESIZE"

    # 7일 이상 된 백업 파일 삭제
    echo ""
    echo "오래된 백업 파일 정리 중..."
    find $BACKUP_DIR -name "${DB_NAME}_*.sql.gz" -type f -mtime +$RETENTION_DAYS -delete

    # 남은 백업 파일 목록
    echo ""
    echo "현재 백업 파일 목록:"
    ls -lh $BACKUP_DIR/${DB_NAME}_*.sql.gz 2>/dev/null || echo "백업 파일 없음"
else
    echo "❌ 백업 실패!"
    exit 1
fi

echo ""
echo "백업 완료: $(date)"
