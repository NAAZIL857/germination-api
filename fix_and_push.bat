@echo off
echo ========================================
echo   CORRECTION ET PUSH VERS GITHUB
echo ========================================
echo.

cd /d "%~dp0"

echo Configuration de Git...
git config --global user.email "naazil857@gmail.com"
git config --global user.name "NAAZIL857"

echo Suppression de l'ancien remote...
git remote remove origin 2>nul

echo Ajout du nouveau remote...
git remote add origin https://github.com/NAAZIL857/germination-api.git

echo Ajout de tous les fichiers...
git add .

echo Commit des fichiers...
git commit -m "API de germination - 10 semences avec parametres mis a jour"

echo Push vers GitHub...
git push -u origin main

echo.
echo ========================================
echo   TERMINE!
echo ========================================
echo.
echo Allez sur: https://github.com/NAAZIL857/germination-api
echo.
pause
