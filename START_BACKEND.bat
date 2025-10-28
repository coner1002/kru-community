@echo off
echo ========================================
echo Russian.Town Backend Starting...
echo ========================================
echo.

cd backend

echo Setting environment variables...
set DATABASE_URL=postgresql://kru_user:password@localhost:5432/kru_community
set REDIS_URL=redis://localhost:6379/0
set SECRET_KEY=dev-secret-key
set ENVIRONMENT=development

echo.
echo Starting backend server on http://localhost:8000
echo Press Ctrl+C to stop
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
