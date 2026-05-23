@echo off
chcp 65001 >nul
title Obtener IP Local - FaceRecognition AntiSpoofing
color 0A

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║     TU DIRECCIÓN IP LOCAL (para acceso desde otros dispositivos)║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

for /f "tokens=2 delims=:" %%a in ('ipconfig ^| find "IPv4"') do (
    set "ip=%%a"
    REM Eliminar espacios en blanco
    for /f "tokens=*" %%b in ("!ip!") do set "ip=%%b"
    echo   📍 IP LOCAL: !ip!
    echo.
    echo   📱 URLS PARA COMPARTIR:
    echo   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    echo   🏠 Inicio:      http://!ip!:5000
    echo   👤 RRHH:        http://!ip!:5000/rrhh
    echo   🛡️  Vigilancia: http://!ip!:5000/vigilancia
    echo   ⚙️  Admin:      http://!ip!:5000/admin
    echo.
    echo   💡 INSTRUCCIONES:
    echo   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    echo   1️⃣  Copia una de las URLs de arriba
    echo   2️⃣  En otro dispositivo (iPhone, tablet, PC), abre el navegador
    echo   3️⃣  Pega la URL en la barra de direcciones
    echo   4️⃣  ¡IMPORTANTE! Deben estar en la MISMA red WiFi
    echo   5️⃣  Permite acceso a cámara cuando te lo pida
    echo.
)

echo   ⚠️  NOTAS IMPORTANTES:
echo   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   • Asegúrate de que el servidor Flask está corriendo
echo   • Ambos dispositivos DEBEN estar en la misma red WiFi
echo   • Si cambias de WiFi, la IP podría cambiar
echo   • Desactiva el Firewall si tienes problemas
echo.
echo   ℹ️  GUARDAR IP (en iPhone como app):
echo   1. Abre Safari
echo   2. Ve a http://IP:5000
echo   3. Pulsa compartir → "Añadir a pantalla de inicio"
echo.

pause
