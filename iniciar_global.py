#!/usr/bin/env python3
"""
Script para iniciar la app con acceso global usando ngrok
Permite acceder desde cualquier lugar del mundo
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def cargar_token():
    """Cargar token de ngrok de archivo o entrada del usuario"""
    token_file = Path(".ngrok_token")
    
    if token_file.exists():
        with open(token_file, "r") as f:
            token = f.read().strip()
            if token:
                return token
    
    print()
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║                   Configuración de ngrok                       ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print()
    print("1️⃣  Ve a: https://dashboard.ngrok.com/signup")
    print("2️⃣  Crea una cuenta (es gratis)")
    print("3️⃣  Copia tu 'Authtoken'")
    print("4️⃣  Pégalo abajo")
    print()
    
    token = input("🔑 Ingresa tu token de ngrok: ").strip()
    
    if token:
        with open(token_file, "w") as f:
            f.write(token)
        print(f"✅ Token guardado en .ngrok_token")
    else:
        print("❌ Token vacío")
        sys.exit(1)
    
    return token

def iniciar_ngrok(token):
    """Iniciar ngrok con el token"""
    ngrok_path = Path("ngrok") / ("ngrok.exe" if sys.platform == "win32" else "ngrok")
    
    if not ngrok_path.exists():
        print(f"❌ ngrok no encontrado en {ngrok_path}")
        print("Ejecuta primero: python instalar_ngrok.py")
        sys.exit(1)
    
    print()
    print("🚀 Iniciando ngrok...")
    print()
    
    # Ejecutar ngrok
    cmd = [
        str(ngrok_path),
        "http",
        "5000",
        "--authtoken", token
    ]
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n🛑 ngrok detenido")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def main():
    print()
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║        FaceRecognition - Acceso Global con ngrok               ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print()
    
    # Verificar que Flask está corriendo
    print("⚠️  IMPORTANTE:")
    print("   El servidor Flask DEBE estar corriendo en otra terminal")
    print("   Ejecuta en otra ventana: python app.py")
    print()
    input("Presiona ENTER cuando el servidor esté corriendo...")
    print()
    
    # Cargar token
    token = cargar_token()
    
    # Iniciar ngrok
    print()
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║                    ngrok en ejecución                          ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print()
    print("📡 Tu app está siendo expuesta globalmente...")
    print("📍 Visita: https://dashboard.ngrok.com/endpoints/status")
    print("   Para ver tu URL pública")
    print()
    
    iniciar_ngrok(token)

if __name__ == "__main__":
    main()
