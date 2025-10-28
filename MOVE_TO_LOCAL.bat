@echo off
echo ========================================
echo Copy Project to D Drive
echo ========================================
echo.
echo Source: %~dp0
echo Target: D:\Projects\kru-community
echo.
echo This will copy the project to local D drive
echo to avoid Google Drive sync conflicts.
echo.
echo Estimated time: 5-10 minutes
echo.
pause

echo.
echo Copying project files...
echo.

REM Create target folder
if not exist "D:\Projects" mkdir "D:\Projects"

REM Copy project (excluding large folders)
xcopy "%~dp0*.*" "D:\Projects\kru-community\" /E /I /H /Y /EXCLUDE:%~dp0exclude_list.txt

echo.
echo ========================================
echo Copy Complete!
echo ========================================
echo.
echo New location: D:\Projects\kru-community
echo.
echo Next steps:
echo   1. cd D:\Projects\kru-community
echo   2. Run QUICK_START.bat
echo.
echo For frontend development:
echo   1. cd D:\Projects\kru-community\frontend
echo   2. npm install
echo   3. npm run dev
echo.
pause
