@echo off
echo ========================================
echo Next.js Development Server
echo ========================================
cd /d "%~dp0"

REM Check if node_modules exists
if not exist "node_modules\" (
    echo node_modules not found. Installing dependencies...
    echo.
    call npm install
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
    echo.
    echo Dependencies installed successfully!
    echo.
)

echo Starting Next.js development server...
echo Server will be available at: http://localhost:3000
echo Press Ctrl+C to stop
echo.

call npm run dev
pause