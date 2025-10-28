@echo off
echo ========================================
echo Next.js Frontend Development Server
echo ========================================
echo.
echo Frontend: http://localhost:3000
echo.
echo Press any key to start...
pause > nul

cd frontend

echo.
echo Starting Next.js development server...
echo.

npm run dev

pause
