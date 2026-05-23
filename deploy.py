#!/usr/bin/env python3
# Script de Deploy Automatizado para Render
import subprocess
import sys
import os

def run_command(cmd, description):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n[*] {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"ERROR: {result.stderr}")
            return False
        print(f"OK: {result.stdout.strip()}")
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    print("\n" + "="*50)
    print("  DEPLOY AUTOMATIZADO A RENDER")
    print("="*50)
    
    # 1. Validar Python
    if not run_command("python --version", "Verificando Python"):
        sys.exit(1)
    
    # 2. Validar requirements.txt
    print("\n[*] Contenido de requirements.txt:")
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r") as f:
            for line in f:
                print(f"    - {line.strip()}")
    else:
        print("ERROR: requirements.txt no encontrado")
        sys.exit(1)
    
    # 3. Validar runtime.txt
    print("\n[*] Verificando runtime.txt:")
    if os.path.exists("runtime.txt"):
        with open("runtime.txt", "r") as f:
            runtime = f.read().strip()
            print(f"    Runtime: {runtime}")
            if "3.11" not in runtime and "3.12" not in runtime:
                print("    ADVERTENCIA: Se recomienda Python 3.11+")
    else:
        print("ERROR: runtime.txt no encontrado")
        sys.exit(1)
    
    # 4. Git commit y push
    print("\n[*] Preparando cambios para GitHub...")
    run_command("git add requirements.txt runtime.txt", "Agregando cambios")
    run_command('git commit -m "Fix: Actualizar dependencias para Python 3.11"', "Commiteando cambios")
    
    print("\n[*] Haciendo push a GitHub...")
    if run_command("git push origin main", "Push a GitHub"):
        print("\n" + "="*50)
        print("  EXITO: Deploy iniciado en Render")
        print("  Monitor: https://dashboard.render.com")
        print("="*50)
    else:
        print("\nERROR: No se pudo hacer push")
        sys.exit(1)

if __name__ == "__main__":
    main()
