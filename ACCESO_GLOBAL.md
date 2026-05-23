# 🌍 Acceso Global - Desde Cualquier Lugar del Mundo

## ¿Qué es Acceso Global?

Tu aplicación estará disponible **públicamente en Internet** con una URL como:
```
https://abc-123-def.ngrok-free.app
```

Cualquiera en el mundo puede acceder desde:
- 🖥️ Computadora (Windows, Mac, Linux)
- 📱 iPhone/iPad
- 🤖 Android
- 📊 Tablets

## 🚀 Configuración en 5 Minutos

### Paso 1: Crear Cuenta ngrok (GRATIS)
1. Ve a: **https://dashboard.ngrok.com/signup**
2. Crea una cuenta con email o GitHub
3. Verifica tu email

### Paso 2: Obtener Token
1. En el dashboard de ngrok
2. Click en "Your Authtoken" (lado izquierdo)
3. Copia el token (algo como: `2y3C8pJ9...`)

### Paso 3: Instalar ngrok
```bash
python instalar_ngrok.py
```

**Resultado:**
- ✅ ngrok se descarga automáticamente
- ✅ Se extraer en carpeta `ngrok/`
- ✅ Listo para usar

### Paso 4: Iniciar en 2 Terminales

**Terminal 1 - Servidor Flask:**
```bash
python app.py
```
Espera hasta ver: `Running on http://0.0.0.0:5000`

**Terminal 2 - ngrok (Acceso Global):**
```bash
python iniciar_global.py
```
Te pedirá el token que copiaste en Paso 2

### Paso 5: Compartir URL

ngrok te muestra una URL pública como:
```
https://abc-123-def.ngrok-free.app
```

**Comparte esta URL:**
```
https://abc-123-def.ngrok-free.app/rrhh
https://abc-123-def.ngrok-free.app/vigilancia
```

¡Y listo! Cualquiera puede acceder desde el mundo.

## 🪟 Método Rápido (Windows)

Simplemente haz **doble clic** en `Acceso_Global.bat` y sigue las instrucciones.

## 📱 Acceder desde iPhone

1. Copia la URL: `https://abc-123-def.ngrok-free.app`
2. En Safari o Chrome, pega la URL
3. ¡Listo! Funciona igual que en PC

**Para guardar como app:**
- Safari: Compartir → "Añadir a pantalla de inicio"

## ⚙️ Arquitectura

```
Tu PC (puerto 5000)
       ↓ (conexión local)
   ngrok (en tu PC)
       ↓ (encriptado por Internet)
  Servidores ngrok
       ↓ (encriptado por Internet)
 Otros dispositivos
```

## 🔒 Seguridad

### ✅ Seguro
- 🔐 HTTPS encriptado end-to-end
- 🔑 Token de autenticación en ngrok
- 🌐 URL única y aleatoria
- 📡 Datos cifrados en tránsito

### ⚠️ Consideraciones
- 👁️ La URL es pública (no compartas en redes públicas)
- 📸 Las imágenes viajan por Internet (¡protegidas!)
- 🔄 La URL cambia cada vez que reinicia ngrok (plan free)
- ⏱️ Sesiones máximo 2 horas (plan free)

## 💰 Planes ngrok

| Feature | Free | Pro |
|---------|------|-----|
| URL pública | ✅ | ✅ |
| HTTPS | ✅ | ✅ |
| Sesiones | 2h max | Ilimitado |
| URL fija | ❌ | ✅ |
| Custom domain | ❌ | ✅ |
| Usuarios concurrentes | 1 | Ilimitado |
| Precio | Gratis | $12/mes |

Para **producción**, recomendamos **Plan Pro**.

## 📝 Monitorar Conexiones

### Dashboard en tiempo real

1. Ve a: https://dashboard.ngrok.com/endpoints/status
2. Verás en vivo:
   - 📍 URL pública actual
   - 📊 Conexiones activas
   - 📈 Tráfico de datos
   - 🕐 Tiempo restante (plan free)

### En tu PC

ngrok muestra en la consola:
```
Session Status: online
Session Expires: 1h 59m 45s from now

Web Interface: http://127.0.0.1:4040

Forwarding: https://abc-123-def.ngrok-free.app -> http://localhost:5000
```

## 🛠️ Solucionar Problemas

### ❌ "Invalid authtoken"
```
❌ Solución: Copia bien el token desde https://dashboard.ngrok.com
```

### ❌ "No internet connection"
```
❌ Solución: Verifica tu conexión a Internet
```

### ❌ "Connection refused"
```
❌ Solución: Asegúrate que `python app.py` está corriendo en otra terminal
```

### ❌ "Session expired"
```
❌ Solución: Plan free = máximo 2 horas. Reinicia ngrok (genera nueva URL)
```

## 📱 Ejemplos de URLs Reales

```
https://abc-123-def.ngrok-free.app           ← Inicio
https://abc-123-def.ngrok-free.app/rrhh      ← RRHH
https://abc-123-def.ngrok-free.app/vigilancia ← Vigilancia
https://abc-123-def.ngrok-free.app/admin     ← Admin
```

## 🌐 Alternativas a ngrok

Si ngrok no te funciona, existen otras opciones:

| Opción | Free | Ventajas |
|--------|------|----------|
| ngrok | ✅ | Fácil, popular, confiable |
| Cloudflare Tunnel | ✅ | Más barato, mejor para producción |
| localtunnel | ✅ | Simple, sin registro |
| serveo.net | ✅ | Ultra-simple, sin configuración |

## 🎯 Usar Cloudflare Tunnel (alternativa)

```bash
# Descargar cloudflared
# Instalar según tu SO

# Ejecutar
cloudflared tunnel --url http://localhost:5000
```

## 📊 Monitoreo en Producción

Para estadísticas detalladas:
```
https://dashboard.ngrok.com/endpoints/status
```

Te muestra:
- 📈 Gráficos de tráfico
- 📊 Conexiones por día
- 🕐 Uptime
- 🌍 Ubicaciones de usuarios

## ⚡ Rendimiento

- 🚀 Latencia: ~50-100ms adicionales
- 💾 Ancho de banda: Ilimitado (plan free)
- 🔄 Conexiones simultáneas: 1 (plan free)

## 🔄 Mantener Sesión Abierta

Para desarrollo:
```bash
# Terminal 1
python app.py

# Terminal 2  
python iniciar_global.py

# Mantén ambas abiertas
```

Para producción, recomendamos:
- ✅ Plan Pro de ngrok
- ✅ O usar Cloudflare/Railway/Heroku
- ✅ Dominio personalizado

## 📞 Soporte

- ngrok: https://ngrok.com/support
- Documentación: https://ngrok.com/docs
- Estado: https://status.ngrok.com

---

✅ **¡Tu app está lista para ser compartida globalmente! 🌍**
