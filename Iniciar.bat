@echo off
title FaceRecognition AntiSpoofing - Inicio Rápido
color 0A
cls

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                   ¡INICIO RÁPIDO EN 3 PASOS!                   ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo 📋 PASO 1: Generar certificados SSL (primera vez)
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if exist "certs\cert.pem" (
    echo ✅ Certificados ya existen
) else (
    echo 🔐 Ejecutando: python generar_certificados.py
    python generar_certificados.py
    if errorlevel 1 (
        echo ❌ Error al generar certificados
        pause
        exit /b 1
    )
)

echo.
echo 📋 PASO 2: Iniciar servidor Flask
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 🚀 Ejecutando: python app.py
echo.

python app.py

pause
