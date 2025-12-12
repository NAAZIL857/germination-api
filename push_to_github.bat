@echo off
echo ========================================
echo   PUSH VERS GITHUB
echo ========================================
echo.

cd /d "%~dp0"

echo Initialisation de Git...
git init

echo Ajout de tous les fichiers...
git add .

echo Commit des fichiers...
git commit -m "API de germination - 10 semences avec temperature, soil_humidity, air_humidity, light_level"

echo Configuration de la branche main...
git branch -M main

echo Ajout du remote origin...
git remote add origin https://github.com/NAAZIL857/germination-api.git

echo Push vers GitHub...
git push -u origin main

echo.
echo ========================================
echo   TERMINE!
echo ========================================
echo.
echo Votre code est maintenant sur GitHub!
echo Allez sur: https://github.com/NAAZIL857/germination-api
echo.
pause
