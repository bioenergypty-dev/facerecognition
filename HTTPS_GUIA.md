# 🔒 HTTPS - Guía de Configuración

## ✅ ¿Por qué HTTPS?

HTTPS encripta los datos mientras viajan por la red:
- ✅ La contraseña está protegida
- ✅ Las imágenes de la cámara se transfieren de forma segura
- ✅ Nadie puede interceptar los datos en la red WiFi

## 🚀 Configuración Rápida (3 pasos)

### Paso 1: Generar Certificados (UNA SOLA VEZ)
```bash
python generar_certificados.py
```

**Resultado:** Se crearán dos archivos en `certs/`:
- `cert.pem` → Certificado público
- `key.pem` → Clave privada

### Paso 2: Iniciar el servidor con HTTPS
**Opción A (recomendado):** Haz doble clic en `Iniciar_HTTPS.bat`

**Opción B (manual):**
```bash
python app.py
```

### Paso 3: Acceder desde navegador
```
https://localhost:5000        (en tu PC)
https://192.168.1.100:5000   (desde otro dispositivo)
```

## ⚠️ Advertencia de Seguridad del Navegador

Cuando accedas por HTTPS, verás algo así:

```
🔐 La conexión no es segura
⚠️  Tu conexión a 192.168.1.100 no es privada
```

**¡ESTO ES NORMAL!** Aparece porque el certificado está autofirmado.

### Cómo continuar:
1. **Chrome/Edge:** Click en "Avanzado" → "Continuar a 192.168.1.100 (inseguro)"
2. **Firefox:** Click en "Avanzado" → "Aceptar el riesgo y continuar"
3. **Safari:** Click en "Mostrar detalles" → "Visitar este sitio web"

## 📱 En iPhone/iPad

### Safari:
1. Ve a `https://IP:5000`
2. Verás ⚠️ advertencia
3. Pulsa "Visitar este sitio web"
4. Permite acceso a cámara

### Guardar como app:
1. Pulsa compartir 
2. "Añadir a pantalla de inicio"
3. ¡Listo! Se abre con HTTPS automáticamente

## 🔐 Seguridad Técnica

### ¿Es realmente seguro?

**En red LOCAL (mismo WiFi):**
- ✅ SÍ - El certificado autofirmado es SEGURO
- ✅ Nadie en Internet puede interceptar (no es accesible desde Internet)
- ✅ La encriptación funciona igual que HTTPS normal

**En Internet:**
- ❌ NO - Los navegadores mostrarán advertencia permanente
- ⚠️ Se recomienda usar Let's Encrypt para Internet

### Detalles técnicos:
```
Algoritmo: RSA 2048 bits
Hash: SHA256
Validez: 365 días
Tipo: Autofirmado (self-signed)
```

## 📋 Archivos Generados

```
proyecto/
├── certs/
│   ├── cert.pem          ← Certificado público
│   └── key.pem           ← Clave privada (¡PROTEGIDA!)
├── generar_certificados.py
├── Iniciar_HTTPS.bat
└── app.py                ← Automáticamente usa HTTPS si existe
```

## 🔄 Renovar Certificados

Los certificados expiran después de 365 días. Para renovar:

```bash
# Elimina los antiguos
rmdir certs /s /q

# Genera nuevos
python generar_certificados.py
```

## 🛠️ Troubleshooting

| Problema | Solución |
|----------|----------|
| "No se puede acceder al servidor" | ¿Ejecutaste `Iniciar_HTTPS.bat`? |
| "Certificado no válido" | Espera 5-10 seg a que cargue el certificado |
| "Cámara no funciona" | Algunos navegadores en iOS necesitan permitir acceso en Settings |
| "Connection refused" | ¿El puerto 5000 está en uso? Cambia en app.py |

## ℹ️ HTTP vs HTTPS

| Feature | HTTP | HTTPS |
|---------|------|-------|
| Encriptación | ❌ | ✅ |
| Datos visibles en WiFi | ❌ Sí | ✅ No |
| Certificado necesario | ❌ | ✅ |
| Velocidad | ⚡⚡ | ⚡ |
| Recomendado para producción | ❌ | ✅ |

## 📖 Para más información

- [Mozilla - HTTPS Explained](https://developer.mozilla.org/es/docs/Glossary/HTTPS)
- [Python SSL Documentation](https://docs.python.org/3/library/ssl.html)
- [Flask SSL Context](https://flask.palletsprojects.com/en/latest/ssl/)

---

✅ **Tu aplicación está lista para HTTPS seguro en red local**
