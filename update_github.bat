@echo off
echo ========================================
echo   MISE A JOUR GITHUB
echo ========================================
echo.

cd /d "%~dp0"

echo Ajout des modifications...
git add .

echo Commit des changements...
git commit -m "Adaptation IoT: light_level en pourcentage (0-100%) au lieu d'heures"

echo Push vers GitHub...
git push origin main

echo.
echo ========================================
echo   TERMINE!
echo ========================================
echo.
echo Modifications pushees sur GitHub!
echo Render va automatiquement redployer l'API.
echo.
pause
