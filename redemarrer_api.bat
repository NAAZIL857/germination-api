@echo off
chcp 65001 >nul
echo ========================================
echo   REDEMARRAGE DE L'API
echo ========================================
echo.
echo Arret de l'API en cours...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do taskkill /F /PID %%a >nul 2>&1
timeout /t 2 /nobreak >nul

echo Demarrage de l'API avec les nouvelles semences...
echo.
python api.py
