#!/usr/bin/env python3
"""
Script para subir cambios a GitHub automáticamente
"""
import subprocess
import sys
import os

def run_cmd(cmd, description=""):
    """Ejecuta comando Git"""
    print(f"\n[*] {description}..." if description else f"[*] {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=os.getcwd())
        if result.stdout:
            print(f"    {result.stdout.strip()}")
        if result.returncode != 0:
            if result.stderr:
                print(f"    ⚠️  {result.stderr.strip()}")
            return False
        return True
    except Exception as e:
        print(f"    ❌ {e}")
        return False

def main():
    git_exe = r'"C:\Program Files\Git\cmd\git.exe"'
    
    print("\n" + "="*60)
    print("  SUBIR CAMBIOS A GITHUB")
    print("="*60)
    
    # Verificar repo Git
    print("\n[1/4] Verificando repositorio...")
    is_git_repo = subprocess.run(
        f'{git_exe} rev-parse --git-dir',
        shell=True, capture_output=True, text=True
    ).returncode == 0
    
    if not is_git_repo:
        print("    ❌ No es un repositorio Git")
        print("\n    Inicializa primero con:")
        print("    & git init")
        print("    & git remote add origin https://github.com/TU_USUARIO/REPO.git")
        return False
    
    print("    ✓ Repositorio detectado")
    
    # Mostrar cambios
    print("\n[2/4] Cambios pendientes:")
    run_cmd(f'{git_exe} status --short')
    
    # Agregar cambios
    print("\n[3/4] Agregando cambios...")
    archivos = [
        "requirements.txt",
        "runtime.txt", 
        "app.py",
        "Procfile",
        "start.sh",
        "descargar_modelos.py",
        ".gitignore",
        "INSTRUCCIONES_GITHUB_RENDER.md"
    ]
    
    for archivo in archivos:
        if os.path.exists(archivo):
            run_cmd(f'{git_exe} add {archivo}', f"Agregando {archivo}")
    
    # Hacer commit
    print("\n[4/4] Commitiendo cambios...")
    commit_msg = "Fix: Descargar modelos automáticamente en Render"
    if run_cmd(f'{git_exe} commit -m "{commit_msg}"', "Commitiendo"):
        print("    ✓ Commit creado")
    else:
        print("    ⚠️  Sin cambios nuevos para commitear")
    
    # Hacer push
    print("\n[PUSH] Enviando a GitHub...")
    if run_cmd(f'{git_exe} push origin main', "Push"):
        print("\n" + "="*60)
        print("  ✅ EXITO: Cambios enviados a GitHub")
        print("  Render detectará automáticamente y desplegará...")
        print("="*60 + "\n")
        return True
    else:
        print("\n⚠️  Verifica estos comandos:")
        print("    & git config --global user.email 'tu@email.com'")
        print("    & git config --global user.name 'Tu Nombre'")
        print("    & git remote -v (verificar remote)")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
