# 🚀 CONFIGURACIÓN - FaceRecognition AntiSpoofing

## ✅ La aplicación ya está configurada para:

1. **Acceso desde múltiples dispositivos** ✓
   - Computadoras
   - iPhones
   - Tablets
   - Cualquier dispositivo con navegador

2. **Diseño Responsive** ✓
   - Se adapta automáticamente a cualquier tamaño de pantalla
   - Touch-friendly para móviles
   - Optimizado para todos los navegadores

## 📱 CÓMO USAR

### Opción 1: En tu computadora
```
http://localhost:5000
```

### Opción 2: Desde otro dispositivo en la MISMA RED WiFi

1. **Encuentra tu IP local:**
   - Abre PowerShell (Windows)
   - Escribe: `ipconfig`
   - Busca "IPv4 Address" (ej: 192.168.1.100)

2. **Comparte la URL:**
   ```
   http://TU_IP:5000
   http://TU_IP:5000/rrhh
   http://TU_IP:5000/vigilancia
   ```

## ⚙️ Script para obtener IP (Windows)

**Crea un archivo `obtener_ip.bat` con:**
```batch
@echo off
echo Tu IP local es:
for /f "tokens=2 delims=:" %%a in ('ipconfig^|find "IPv4"') do (
    echo %%a
    pause
)
```

**Luego ejecuta haciendo doble clic en el archivo**

## 📝 URLs Disponibles

| Página | URL |
|--------|-----|
| 🏠 Inicio | `/` |
| 👤 RRHH | `/rrhh` |
| 🛡️ Vigilancia | `/vigilancia` |
| ⚙️ Admin | `/admin` |

## 🔐 Notas de Seguridad

- ⚠️ Solo funciona en la **misma red WiFi**
- ⚠️ No accesible desde Internet por defecto (es seguro)
- ✅ HTTPS se recomienda para redes públicas

## 📱 iOS/iPhone Específicamente

La cámara funciona en iOS con:
- ✅ Safari (con acceso HTTPS)
- ✅ Chrome/Firefox (con HTTP local)

**Para guardar como app en iPhone:**
1. Abre en Safari
2. Pulsa el icono de compartir
3. "Añadir a pantalla de inicio"
4. ¡Listo! Aparecerá como una app

## 🐛 Troubleshooting

| Problema | Solución |
|----------|----------|
| No se ve desde otro dispositivo | ¿Están en la misma WiFi? ¿Firewall desactivado? |
| Cámara no pide permiso | Reinicia navegador, limpia caché |
| IP cambia cada vez | Asigna IP estática en el router (recomendado) |

## 🎯 Para Producción

Si quieres acceso desde Internet, necesitarás:
1. Configurar HTTPS con SSL
2. Abrir puerto 5000 en el router (⚠️ riesgo de seguridad)
3. Usar un servicio de tunelización (ngrok, Cloudflare Tunnel)

---

📞 **¿Necesitas ayuda?** Revisa ACCESO_MULTIDISPOSITIVO.md para instrucciones detalladas.
