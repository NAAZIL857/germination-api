@echo off
chcp 65001 >nul
echo ========================================
echo   API de Prediction de Germination
echo ========================================
echo.
echo L'API va demarrer...
echo.
echo Apres le demarrage, ouvrez votre navigateur:
echo   http://localhost:8000
echo.
echo Documentation interactive:
echo   http://localhost:8000/docs
echo.
echo Appuyez sur CTRL+C pour arreter l'API
echo ========================================
echo.
python api.py
echo.
echo L'API a ete arretee.
pause
