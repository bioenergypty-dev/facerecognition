# 📱 Acceso desde Múltiples Dispositivos

## 🖥️ Desde tu Computadora
- **URL Local**: http://localhost:5000
- **Desde otra PC en la red**: http://TU_IP:5000

## 📱 Desde iPhone/iPad
1. Obtén tu dirección IP de Windows:
   - Abre PowerShell/CMD
   - Escribe: `ipconfig`
   - Busca "IPv4 Address" (ejemplo: 192.168.1.100)

2. En iPhone/iPad:
   - Abre Safari
   - Ve a: http://192.168.1.100:5000
   - Permite acceso a cámara cuando te pida

3. **Guardar como app (opcional)**:
   - Toca compartir → "Añadir a pantalla de inicio"
   - Se verá como una app nativa

## 💻 Desde otra Computadora en la Red
1. En la otra PC, obtén la IP de esta computadora:
   - PowerShell: `ipconfig` → busca IPv4 Address

2. Ve a: http://IP_DE_TU_COMPUTADORA:5000

## 🔧 Encontrar tu IP

**Windows PowerShell:**
```powershell
ipconfig
```
Busca la línea que dice `IPv4 Address: 192.168.X.X`

**Atajos rápidos:**
- Pulsa `Windows + R`
- Escribe: `cmd`
- Escribe: `ipconfig`

## ⚠️ Problemas Comunes

### "No puedo acceder desde otro dispositivo"
1. ¿Están en la **misma red WiFi**?
2. ¿El servidor Python está corriendo? Verifica que ves `Running on http://0.0.0.0:5000`
3. Prueba: `ping TU_IP` desde el otro dispositivo
4. Desactiva temporalmente el Firewall de Windows

### "Cámara no funciona en iPhone"
1. iPhone solo permite cámara en **HTTPS** desde Safari
2. Solución: Usa la app nativa (Chrome, Firefox) en iPhone
3. O accede desde la misma computadora

### Permiso de cámara denegado
1. iPhone: Settings → Safari → Camera → Permitir
2. Computadora: Comprueba permisos en settings del navegador

## 🚀 Para Usuarios Finales

**Comparte esta URL a los usuarios:**
```
http://192.168.1.100:5000/rrhh    (para RRHH)
http://192.168.1.100:5000/vigilancia (para Vigilancia)
```

Reemplaza `192.168.1.100` con tu IP real.

---

✅ La app ahora es **100% responsive** en móviles y tablets
