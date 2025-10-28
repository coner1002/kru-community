#!/bin/bash

# PostgreSQL 데이터베이스 복원 스크립트

# 사용법 체크
if [ $# -eq 0 ]; then
    echo "사용법: $0 <백업파일경로>"
    echo ""
    echo "예시:"
    echo "  $0 /var/backups/postgres/kru_community_20251001_120000.sql.gz"
    echo ""
    echo "백업 파일 목록:"
    ls -lh /var/backups/postgres/kru_community_*.sql.gz 2>/dev/null || echo "백업 파일 없음"
    exit 1
fi

BACKUP_FILE=$1
DB_NAME="kru_community"
DB_USER="kru_user"

# 백업 파일 존재 확인
if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ 오류: 백업 파일을 찾을 수 없습니다: $BACKUP_FILE"
    exit 1
fi

echo "==================================="
echo "PostgreSQL 복원 시작"
echo "시간: $(date)"
echo "백업 파일: $BACKUP_FILE"
echo "==================================="

# 사용자 확인
read -p "⚠️  경고: 기존 데이터가 모두 삭제됩니다. 계속하시겠습니까? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "복원 취소됨"
    exit 0
fi

echo ""
echo "1. 기존 데이터베이스 삭제 중..."
docker-compose exec -T postgres psql -U $DB_USER -d postgres -c "DROP DATABASE IF EXISTS $DB_NAME;"

echo "2. 새 데이터베이스 생성 중..."
docker-compose exec -T postgres psql -U $DB_USER -d postgres -c "CREATE DATABASE $DB_NAME;"

echo "3. 백업 데이터 복원 중..."
gunzip -c $BACKUP_FILE | docker-compose exec -T postgres psql -U $DB_USER -d $DB_NAME

# 복원 성공 여부 확인
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 복원 성공!"

    # 테이블 수 확인
    TABLE_COUNT=$(docker-compose exec -T postgres psql -U $DB_USER -d $DB_NAME -c "\dt" | grep -c "table")
    echo "복원된 테이블 수: $TABLE_COUNT"
else
    echo ""
    echo "❌ 복원 실패!"
    exit 1
fi

echo ""
echo "복원 완료: $(date)"
