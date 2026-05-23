#!/usr/bin/env python3
"""
Script para descargar e instalar ngrok automáticamente
ngrok permite acceder a tu app desde cualquier lugar del mundo
"""

import os
import sys
import platform
from pathlib import Path
import urllib.request
import zipfile

def descargar_ngrok():
    """Descargar ngrok según el SO"""
    
    sistema = platform.system()
    arquitectura = platform.machine()
    
    # Determinar URL de descarga según SO
    if sistema == "Windows":
        url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
        nombre_zip = "ngrok-windows.zip"
        nombre_exe = "ngrok.exe"
    elif sistema == "Darwin":  # macOS
        if "arm" in arquitectura:  # Apple Silicon
            url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-darwin-arm64.zip"
        else:
            url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-darwin-amd64.zip"
        nombre_zip = "ngrok-macos.zip"
        nombre_exe = "ngrok"
    elif sistema == "Linux":
        url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.zip"
        nombre_zip = "ngrok-linux.zip"
        nombre_exe = "ngrok"
    else:
        print(f"❌ SO no soportado: {sistema}")
        return False
    
    # Crear directorio
    ngrok_dir = Path("ngrok")
    ngrok_dir.mkdir(exist_ok=True)
    
    ngrok_path = ngrok_dir / nombre_exe
    
    # Verificar si ya existe
    if ngrok_path.exists():
        print(f"✅ ngrok ya existe en: {ngrok_path}")
        return True
    
    # Descargar
    zip_path = ngrok_dir / nombre_zip
    print(f"📥 Descargando ngrok ({sistema})...")
    print(f"   Desde: {url}")
    
    try:
        urllib.request.urlretrieve(url, str(zip_path))
        print(f"✅ Descarga completada: {zip_path}")
    except Exception as e:
        print(f"❌ Error al descargar: {e}")
        return False
    
    # Extraer
    print(f"📦 Extrayendo...")
    try:
        with zipfile.ZipFile(str(zip_path), 'r') as zip_ref:
            zip_ref.extractall(str(ngrok_dir))
        print(f"✅ Extracción completada")
    except Exception as e:
        print(f"❌ Error al extraer: {e}")
        return False
    
    # Hacer ejecutable en Linux/macOS
    if sistema in ["Linux", "Darwin"]:
        os.chmod(str(ngrok_path), 0o755)
        print(f"✅ Permisos establecidos")
    
    # Limpiar ZIP
    zip_path.unlink()
    
    print(f"✅ ngrok instalado en: {ngrok_path}")
    return True

if __name__ == "__main__":
    print()
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║              Instalador de ngrok - Acceso Global               ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print()
    
    if descargar_ngrok():
        print()
        print("🎉 ¡ngrok instalado exitosamente!")
        print()
        print("Próximo paso:")
        print("1. Crea una cuenta gratis en: https://dashboard.ngrok.com/signup")
        print("2. Copia tu token de autenticación")
        print("3. Ejecuta: python iniciar_global.py")
        print()
    else:
        print("❌ Error durante la instalación")
        sys.exit(1)
