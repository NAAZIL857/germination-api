@echo off
chcp 65001 >nul
cls
echo ================================================================================
echo                    REDEMARRAGE DE L'API
echo                    Mise a jour vers 10 semences
echo ================================================================================
echo.
echo Etape 1: Arret de l'API en cours...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo    Arret du processus %%a...
    taskkill /F /PID %%a >nul 2>&1
)
timeout /t 2 /nobreak >nul
echo    [OK] API arretee
echo.

echo Etape 2: Verification des fichiers...
if exist main.py (
    echo    [OK] main.py trouve
) else (
    echo    [ERREUR] main.py introuvable
    pause
    exit
)

if exist sensors_data.csv (
    echo    [OK] sensors_data.csv trouve
) else (
    echo    [ERREUR] sensors_data.csv introuvable
    pause
    exit
)
echo.

echo Etape 3: Demarrage de l'API avec 10 semences...
echo.
echo ================================================================================
echo.
python api.py
