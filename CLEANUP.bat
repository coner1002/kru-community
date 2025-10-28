@echo off
chcp 65001 > nul
echo ========================================
echo 프로젝트 정리 스크립트
echo ========================================
echo.
echo 불필요한 임시 파일들을 backup 폴더로 이동합니다.
echo.
echo 이동될 파일:
echo   - fix_*.py, update_*.py, add_*.py 등 임시 수정 스크립트
echo   - 중복/불필요한 배치 파일
echo.
echo 백업 위치: backup\(날짜시간)\
echo.
pause

python cleanup_project.py

echo.
pause