@echo off
chcp 65001 >nul
title Selector de Acceso - FaceRecognition AntiSpoofing
color 0A
cls

:menu
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║        FaceRecognition AntiSpoofing - Selector de Acceso       ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo 🖥️  OPCIÓN 1: SOLO TU COMPUTADORA
echo ─────────────────────────────────
echo   URL: http://localhost:5000
echo   Comando: python app.py
echo   Uso: Solo en tu PC
echo.
echo 📱 OPCIÓN 2: RED LOCAL (WiFi)
echo ─────────────────────────────────
echo   URL: https://192.168.X.X:5000
echo   Otros dispositivos deben estar en tu WiFi
echo   Comando: Iniciar_HTTPS.bat o python app.py
echo.
echo 🌍 OPCIÓN 3: ACCESO GLOBAL (Desde cualquier lugar del mundo)
echo ─────────────────────────────────
echo   URL: https://abc-123-def.ngrok-free.app
echo   Cualquier dispositivo en el mundo
echo   Comando: Acceso_Global.bat
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo Selecciona una opción:
echo [1] Solo mi computadora (simple)
echo [2] Red WiFi local (recomendado para oficina)
echo [3] Acceso global (recomendado para distribuir)
echo [0] Salir
echo.

set /p opcion="Ingresa tu opción [0-3]: "

if "%opcion%"=="0" goto salir
if "%opcion%"=="1" goto opcion1
if "%opcion%"=="2" goto opcion2
if "%opcion%"=="3" goto opcion3

echo ❌ Opción no válida
timeout /t 2 >nul
goto menu

:opcion1
cls
echo.
echo 🖥️  OPCIÓN 1: SOLO TU COMPUTADORA
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo Iniciando servidor en modo simple...
echo.
python app.py
goto menu

:opcion2
cls
echo.
echo 📱 OPCIÓN 2: RED LOCAL (WiFi)
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo Para HTTPS seguro en tu red WiFi:
echo.
call Iniciar_HTTPS.bat
goto menu

:opcion3
cls
echo.
echo 🌍 OPCIÓN 3: ACCESO GLOBAL
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo Iniciando con acceso global...
echo.
call Acceso_Global.bat
goto menu

:salir
exit /b 0
