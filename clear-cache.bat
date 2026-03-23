@echo off
REM Clear Vite cache
echo Clearing Vite cache...
rmdir /s /q frontend\.vite 2>nul
rmdir /s /q frontend\dist 2>nul

REM Kill Node processes
echo Killing Node processes...
taskkill /F /IM node.exe 2>nul

REM Kill Python processes
echo Killing Python processes...
taskkill /F /IM python.exe 2>nul

echo Cache cleared! Restart the dev server now.
echo Run: npm run dev
pause
