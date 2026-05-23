# 🎥 FaceRecognition AntiSpoofing - Sistema Facial Distribuido

## 🌟 Características Principales

- ✅ **Reconocimiento facial** con detección de suplantación (antispoofing)
- ✅ **Multi-dispositivo**: PC, Mac, Linux, iPhone, iPad, Tablets
- ✅ **Responsive**: Se adapta automáticamente a cualquier tamaño de pantalla
- ✅ **HTTPS seguro** en red local
- ✅ **Acceso desde red WiFi** - No requiere Internet

## 📱 Plataformas Soportadas

| Plataforma | Estado | Navegador |
|-----------|--------|-----------|
| 🖥️ Windows | ✅ Full | Chrome, Edge, Firefox |
| 🍎 macOS | ✅ Full | Safari, Chrome, Firefox |
| 🐧 Linux | ✅ Full | Chrome, Firefox |
| 📱 iPhone/iPad | ✅ Full | Safari, Chrome |
| 🤖 Android | ✅ Full | Chrome, Firefox |

## 🚀 Inicio Rápido

### Opción 1: HTTPS (Recomendado - Seguro)

**Primera vez:**
```bash
python generar_certificados.py
```

**Luego:**
```bash
python app.py
```

O simplemente haz doble clic en `Iniciar_HTTPS.bat`

### Opción 2: HTTP (Simple)

```bash
python app.py
```

## 📍 Acceder a la Aplicación

### 🖥️ En tu Computadora
```
HTTP:   http://localhost:5000
HTTPS:  https://localhost:5000
```

### 📱 Desde otro Dispositivo (misma WiFi)

1. Obtén tu IP:
   - Windows: Ejecuta `Obtener_IP.bat`
   - Resultado: `192.168.1.100`

2. En el otro dispositivo:
   ```
   https://192.168.1.100:5000
   https://192.168.1.100:5000/rrhh
   https://192.168.1.100:5000/vigilancia
   ```

### 🌍 Desde Cualquier Lugar del Mundo (Acceso Global)

1. **Una sola vez - Crear cuenta gratis en ngrok:**
   ```
   https://dashboard.ngrok.com/signup
   ```

2. **Instalar ngrok:**
   ```bash
   python instalar_ngrok.py
   ```

3. **Iniciar con acceso global:**
   ```bash
   # Terminal 1: Servidor
   python app.py
   
   # Terminal 2: Acceso global
   python iniciar_global.py
   ```

4. **Compartir URL pública:**
   ```
   https://abc-123-def.ngrok-free.app/rrhh
   https://abc-123-def.ngrok-free.app/vigilancia
   ```

👉 Ver guía completa: [ACCESO_GLOBAL.md](ACCESO_GLOBAL.md)

## 📖 Guías Disponibles

| Archivo | Descripción |
|---------|-----------|
| [ACCESO_GLOBAL.md](ACCESO_GLOBAL.md) | 🌍 Acceso desde cualquier lugar del mundo |
| [HTTPS_GUIA.md](HTTPS_GUIA.md) | 🔒 Configuración de HTTPS seguro |
| [ACCESO_MULTIDISPOSITIVO.md](ACCESO_MULTIDISPOSITIVO.md) | 📱 Acceso desde red local |
| [CONFIGURACION.md](CONFIGURACION.md) | ⚙️ Configuración general |

## 🎯 Módulos Principales

### 🏠 Página de Inicio (`/`)
- Panel de selección de módulos
- Links rápidos a RRHH, Vigilancia y Admin

### 👤 RRHH (`/rrhh`)
- Registro facial de empleados
- Captura 5 fotos después de 3 parpadeos
- Almacena datos en CSV
- Detección de vida (antispoofing)

### 🛡️ Vigilancia (`/vigilancia`)
- Registro de entrada/salida
- Reconocimiento de rostros
- Log de eventos

### ⚙️ Admin (`/admin`)
- Panel administrativo
- Descarga de registros CSV
- Visualización de datos

## 🔐 Seguridad

### ✅ Implementado
- HTTPS con certificados autofirmados
- Encriptación de datos en tránsito
- Headers de seguridad
- Validación de cámara
- Anti-suplantación (detección de parpadeos)

### ⚠️ Recomendaciones
- Usa HTTPS siempre (local o Internet)
- Mantén los certificados privados seguros
- Solo accesible en red local (más seguro)

## 📁 Estructura de Archivos

```
faceRecognition AntiSpoofing/
├── 📄 app.py                        ← Servidor Flask
├── 📄 faceid_engine.py              ← Lógica de reconocimiento facial
├── 
├── 🗂️  templates/
│   ├── index.html                   ← Página inicio
│   ├── rrhh.html                    ← Módulo RRHH
│   ├── vigilancia.html              ← Módulo vigilancia
│   └── admin.html                   ← Panel admin
├──
├── 🗂️  certs/                       ← Certificados SSL (se genera)
│   ├── cert.pem                     ← Certificado público
│   └── key.pem                      ← Clave privada
├──
├── 🗂️  capturas/                    ← Fotos capturadas
│   ├── rrhh/                        ← Fotos de RRHH
│   └── vigilancia/                  ← Fotos de vigilancia
├──
├── 🗂️  data/                        ← Base de datos CSV
│   ├── empleados.csv                ← Registro de empleados
│   └── registros_vigilancia.csv     ← Registro de vigilancia
├──
├── 📄 generar_certificados.py       ← Genera certificados SSL
├── 🚀 Iniciar_HTTPS.bat             ← Script para iniciar (Windows)
├── 📋 Obtener_IP.bat                ← Obtiene IP local (Windows)
├── 📖 HTTPS_GUIA.md                 ← Guía de HTTPS
├── 📖 ACCESO_MULTIDISPOSITIVO.md   ← Guía de acceso remoto
└── 📖 CONFIGURACION.md              ← Configuración general
```

## 🛠️ Requisitos

### Python
```bash
Python 3.9+
```

### Paquetes
```
Flask
opencv-python
dlib
numpy
scipy
cryptography (para HTTPS)
```

### Hardware
- 💻 Computadora con Python
- 🎥 Cámara (integrada o USB)
- 📡 Red WiFi (para multi-dispositivo)

## ⚡ Instalación Completa

```bash
# 1. Clonar o descargar el proyecto
cd faceRecognition_AntiSpoofing

# 2. Crear entorno virtual
python -m venv .venv39
.venv39\Scripts\activate  # Windows

# 3. Instalar dependencias
pip install flask opencv-python dlib numpy scipy cryptography

# 4. Descargar modelos de dlib
# (Si no están, descargar shape_predictor_68_face_landmarks.dat)

# 5. Generar certificados SSL
python generar_certificados.py

# 6. Ejecutar
python app.py
```

## 🔧 Troubleshooting

### ❌ "Cámara no funciona"
```
1. ¿Tienes una cámara conectada?
2. ¿Diste permisos de cámara al navegador?
3. Prueba reiniciando el navegador
```

### ❌ "No puedo acceder desde otro dispositivo"
```
1. ¿Están en la misma red WiFi?
2. ¿El servidor está corriendo? (ves "Running on...")
3. ¿Desactivaste el Firewall?
```

### ❌ "Advertencia de seguridad en HTTPS"
```
✅ NORMAL - Es un certificado autofirmado
   Haz clic en "Continuar de todos modos"
```

### ❌ "El puerto 5000 está en uso"
```bash
# Cambiar puerto en app.py:
# Modificar la línea: app.run(..., port=5001, ...)
```

## 📊 Estructura de Datos

### Registro de Empleados (CSV)
```csv
usuario,contraseña,nombre,apellidos,fecha_nacimiento,fecha_alta,cargo,hora,coordenadas
juan.lopez,pass123,Juan,López,1990-05-15,2024-01-01,Ingeniero,09:30:45,"[(x,y),...(x,y)]"
```

### Registro de Vigilancia (CSV)
```csv
usuario,evento,fecha
juan.lopez,ENTRADA,2024-05-23 08:45:30
juan.lopez,SALIDA,2024-05-23 17:30:15
```

## 🎨 Personalización

### Cambiar colores
Edita los archivos `.html` en `templates/`:
```html
background: limegreen;  ← Color RRHH
background: cyan;       ← Color Vigilancia
```

### Cambiar puerto
En `app.py`:
```python
app.run(host="0.0.0.0", port=5001)  # Cambiar 5000 por 5001
```

## 📞 Soporte

- 📖 Lee las guías Markdown incluidas
- 🐛 Revisa la consola del navegador (F12)
- 💾 Revisa los logs de Python

## 📜 Licencia

MIT - Uso libre y modificación permitida

---

**¡Tu sistema de reconocimiento facial está listo para usar! 🎉**

Para más detalles, consulta:
- [HTTPS_GUIA.md](HTTPS_GUIA.md) - Seguridad
- [ACCESO_MULTIDISPOSITIVO.md](ACCESO_MULTIDISPOSITIVO.md) - Acceso remoto
- [CONFIGURACION.md](CONFIGURACION.md) - Configuración
