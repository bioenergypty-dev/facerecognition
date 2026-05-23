# 🚀 Instrucciones para Conectar a GitHub y Render

## Cambios Realizados

✅ **Actualizado para Render:**
- Dependencias actualizadas a Python 3.11.7
- Script de descarga automática de modelos de IA
- Procfile configurado para descargar modelos antes de iniciar
- .gitignore optimizado

## Paso 1: Crear Repositorio en GitHub
1. Ve a https://github.com/new
2. Nombre: `faceRecognition` (o el que prefieras)
3. Descripción: `Face Recognition Anti-Spoofing System`
4. Selecciona **Private** o **Public**
5. Clic en "Create repository"

## Paso 2: Conectar Repositorio Local a GitHub

Copia y ejecuta en PowerShell (reemplaza `TU_USUARIO` y `REPO_NAME`):

```powershell
cd "c:\Users\maryr\OneDrive\Escritorio\faceRecognition AntiSpoofing"
& "C:\Program Files\Git\cmd\git.exe" remote add origin https://github.com/TU_USUARIO/REPO_NAME.git
& "C:\Program Files\Git\cmd\git.exe" branch -M main
& "C:\Program Files\Git\cmd\git.exe" push -u origin main
```

⚠️ Si GitHub pide autenticación, usa un **Personal Access Token** (PAT):
- Ve a: https://github.com/settings/tokens
- Crea token con scopes: `repo`, `workflow`
- Úsalo como contraseña cuando git lo pida

## Paso 3: Conectar GitHub a Render

1. Ve a https://dashboard.render.com
2. Click en **"New +"** → **"Web Service"**
3. Selecciona: **"Connect GitHub"**
4. Autoriza Render y selecciona tu repositorio
5. Configuración:
   - **Build Command**: `pip install -r requirements.txt` (dejar vacío o por defecto)
   - **Start Command**: `bash start.sh`
   - Python automaticamente usará 3.11.7 (definido en runtime.txt)
6. Click en **"Create Web Service"**

## Paso 4: Deploy Automático

Cada vez que hagas push a `main`, Render desplegará automáticamente:

```powershell
cd "c:\Users\maryr\OneDrive\Escritorio\faceRecognition AntiSpoofing"
& "C:\Program Files\Git\cmd\git.exe" add requirements.txt runtime.txt app.py Procfile
& "C:\Program Files\Git\cmd\git.exe" commit -m "Fix: Descargar modelos automáticamente en Render"
& "C:\Program Files\Git\cmd\git.exe" push origin main
```

## Paso 5: Verificar Logs en Render

En Render dashboard:
1. Selecciona tu servicio
2. Vaya a **"Logs"**
3. Observa el proceso de descarga del modelo
4. Cuando veas "Application loading..." completado = ✅ Listo

## Troubleshooting

**Error: "fatal: Authentication failed"**
- Usa token en lugar de contraseña

**Error: "fatal: remote already exists"**
```powershell
& "C:\Program Files\Git\cmd\git.exe" remote remove origin
& "C:\Program Files\Git\cmd\git.exe" remote add origin https://github.com/TU_USUARIO/REPO.git
```

**La app sigue en error 503 después de 2 minutos:**
1. Revisa Logs en Render
2. Busca mensaje de error (generalmente en descargar_modelos.py)
3. Si falla descarga del modelo, aumenta timeout en render.yaml

**Ver estado actual:**
```powershell
& "C:\Program Files\Git\cmd\git.exe" status
& "C:\Program Files\Git\cmd\git.exe" log --oneline -5
```

---
✅ Una vez configurado, Render desplegará automáticamente con:
- Python 3.11.7
- Dependencias compatibles
- Modelos de IA descargados automáticamente
- Tu app lista en https://tu-servicio.onrender.com

