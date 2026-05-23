@echo off
chcp 65001 >nul
title FaceRecognition AntiSpoofing - Acceso Global
color 0F

cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║        FaceRecognition - Configurar Acceso Global              ║
echo ║                    (con ngrok)                                 ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Verificar si ngrok existe
if not exist "ngrok\ngrok.exe" (
    echo 📥 Descargando ngrok (primera vez)...
    echo.
    python instalar_ngrok.py
    if errorlevel 1 (
        echo ❌ Error durante la instalación de ngrok
        pause
        exit /b 1
    )
)

echo.
echo ✅ ngrok instalado
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║              INSTRUCCIONES DE CONFIGURACIÓN                    ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo 1️⃣  Abre una NUEVA terminal/cmd
echo 2️⃣  Ve a la carpeta del proyecto
echo 3️⃣  Ejecuta: python app.py
echo.
echo 4️⃣  Cuando veas "Running on http://0.0.0.0:5000", presiona ENTER aquí
echo.

pause

echo.
echo 🚀 Iniciando acceso global...
echo.

python iniciar_global.py

pause
