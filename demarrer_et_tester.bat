@echo off
chcp 65001 >nul
echo ================================================================================
echo                    DEMARRAGE ET TEST DE L'API
echo ================================================================================
echo.
echo Ce script va:
echo   1. Demarrer l'API en arriere-plan
echo   2. Attendre qu'elle soit prete
echo   3. Tester l'API
echo   4. Ouvrir la documentation dans votre navigateur
echo.
echo ================================================================================
echo.

echo [1/4] Demarrage de l'API...
start /B python api.py > api_log.txt 2>&1

echo [2/4] Attente du demarrage (10 secondes)...
timeout /t 10 /nobreak >nul

echo [3/4] Test de l'API...
python verifier_api.py

echo.
echo [4/4] Ouverture de la documentation...
start http://localhost:8000/docs

echo.
echo ================================================================================
echo L'API est maintenant en cours d'execution!
echo.
echo Pour arreter l'API:
echo   Fermez cette fenetre OU appuyez sur une touche
echo ================================================================================
echo.
pause

echo.
echo Arret de l'API...
taskkill /F /FI "WINDOWTITLE eq python api.py" >nul 2>&1
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do taskkill /F /PID %%a >nul 2>&1
echo API arretee.
