@echo off
echo ========================================
echo KRU Community - Quick Start (D Drive)
echo ========================================
echo.
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Website: http://localhost:8000
echo.
echo Press any key to start backend server...
pause > nul

cd backend

echo.
echo Setting environment variables...
set DATABASE_URL=sqlite:///./kru_community.db
set SECRET_KEY=dev-secret-key-change-in-production
set ENVIRONMENT=development

echo.
echo Starting backend server...
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
