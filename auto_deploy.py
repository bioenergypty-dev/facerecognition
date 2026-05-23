#!/usr/bin/env python3
"""
Script para hacer commit y push automático a GitHub
Uso: python auto_deploy.py <repositorio_github> <rama>
Ejemplo: python auto_deploy.py https://github.com/usuario/repo.git main
"""
import subprocess
import sys
import os

def run_cmd(cmd, description=""):
    """Ejecuta comando y retorna el resultado"""
    print(f"[*] {description}..." if description else f"[*] {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=os.getcwd())
        if result.stdout:
            print(f"    {result.stdout.strip()}")
        if result.returncode != 0 and result.stderr:
            print(f"    ERROR: {result.stderr.strip()}")
            return False
        return True
    except Exception as e:
        print(f"    ERROR: {e}")
        return False

def main():
    git_exe = r'"C:\Program Files\Git\cmd\git.exe"'
    
    print("\n" + "="*60)
    print("  DEPLOY AUTOMÁTICO A RENDER")
    print("="*60)
    
    # Verificar si es un repositorio Git
    print("\n[1/4] Verificando repositorio Git...")
    is_git_repo = subprocess.run(
        f'{git_exe} rev-parse --git-dir',
        shell=True, capture_output=True, text=True
    ).returncode == 0
    
    if not is_git_repo:
        print("    ❌ No es un repositorio Git")
        print("\n    Opciones:")
        print("    1. Clona el repo: git clone https://github.com/bioenergypty-dev/facerecognition")
        print("    2. Inicializa: git init && git remote add origin <URL>")
        return False
    
    print("    ✓ Repositorio Git detectado")
    
    # Mostrar archivos modificados
    print("\n[2/4] Archivos modificados:")
    run_cmd(f'{git_exe} status --short', "Estado actual")
    
    # Hacer add
    print("\n[3/4] Preparando cambios...")
    if run_cmd(f'{git_exe} add requirements.txt runtime.txt', "Agregando archivos"):
        print("    ✓ Archivos agregados")
    else:
        return False
    
    # Hacer commit
    print("\n[4/4] Creando commit...")
    commit_msg = "Fix: Actualizar dependencias para Python 3.11 - scipy, Flask, numpy, opencv"
    if run_cmd(f'{git_exe} commit -m "{commit_msg}"', "Commitiendo cambios"):
        print("    ✓ Commit creado")
    else:
        print("    ⚠️  Sin cambios nuevos (ya estaban commiteados)")
    
    # Hacer push
    print("\n[PUSH] Enviando a GitHub...")
    if run_cmd(f'{git_exe} push origin main', "Push a main"):
        print("\n" + "="*60)
        print("  ✅ EXITO: Cambios enviados a GitHub")
        print("  Render detectará automáticamente y desplegará...")
        print("  Monitor: https://dashboard.render.com")
        print("="*60 + "\n")
        return True
    else:
        print("\n[ERROR] No se pudo hacer push. Intenta:")
        print("  1. git config --global user.email 'tu@email.com'")
        print("  2. git config --global user.name 'Tu Nombre'")
        print("  3. Verificar acceso a GitHub (SSH keys o token)")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
