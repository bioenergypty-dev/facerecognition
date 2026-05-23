@echo off
chcp 65001 >nul
title FaceRecognition AntiSpoofing - Inicio con HTTPS
color 0F

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║          FaceRecognition AntiSpoofing - Setup HTTPS            ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Verificar si está activado el entorno virtual
if not exist ".venv39\Scripts\activate.bat" (
    echo ❌ Entorno virtual no encontrado (.venv39)
    echo Crea el entorno virtual primero:
    echo   python -m venv .venv39
    pause
    exit /b 1
)

REM Activar entorno virtual
echo 🔧 Activando entorno virtual...
call .venv39\Scripts\activate.bat

REM Verificar si existen los certificados
echo.
echo 🔐 Verificando certificados SSL...
if exist "certs\cert.pem" (
    echo ✅ Certificados encontrados
) else (
    echo ⚠️  Generando certificados autofirmados (primera vez)...
    echo.
    %PYTHON% generar_certificados.py
    if errorlevel 1 (
        echo ❌ Error al generar certificados
        pause
        exit /b 1
    )
)

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                  Iniciando servidor Flask                      ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Mostrar IP local
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| find "IPv4"') do (
    set "ip=%%a"
    for /f "tokens=*" %%b in ("!ip!") do set "ip=%%b"
)

echo 📍 Servidor iniciado:
echo.
echo 🏠 Página de inicio:
echo    https://localhost:5000
echo    https://!ip!:5000
echo.
echo 👤 RRHH:
echo    https://localhost:5000/rrhh
echo    https://!ip!:5000/rrhh
echo.
echo 🛡️  Vigilancia:
echo    https://localhost:5000/vigilancia
echo    https://!ip!:5000/vigilancia
echo.
echo ⚙️  Admin:
echo    https://localhost:5000/admin
echo    https://!ip!:5000/admin
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ⚠️  NOTA: El navegador mostrará advertencia de seguridad
echo    Haz clic en "Continuar de todos modos" (es seguro en red local)
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 🛑 Presiona Ctrl+C para detener el servidor
echo.

%PYTHON% app.py

pause
