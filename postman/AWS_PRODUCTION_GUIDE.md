# 🚀 BTG Pactual API - Instrucciones de Producción (AWS)

## 📋 Resumen del Despliegue

✅ **Estado:** ¡Aplicación desplegada exitosamente en AWS EC2!  
🌐 **IP Pública:** 18.205.222.251  
🔗 **API Base:** http://18.205.222.251:8000  

## 🎯 URLs Importantes

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **API Principal** | http://18.205.222.251:8000 | Endpoint base de la API |
| **Documentación** | http://18.205.222.251:8000/docs | Swagger UI interactiva |
| **Health Check** | http://18.205.222.251:8000/health | Estado de la aplicación |
| **Mongo Express** | http://18.205.222.251:8081 | Interface MongoDB (admin/admin) |

## 🔧 Configuración de Postman

### 1. Importar Environment de Producción
1. Abrir Postman
2. Click en **Import**
3. Seleccionar el archivo: `BTG_Pactual_Production_Environment.postman_environment.json`
4. Confirmar importación

### 2. Seleccionar Environment
1. En la esquina superior derecha de Postman
2. Seleccionar **"BTG Pactual - Production Environment (AWS)"**
3. ✅ Verificar que `base_url` = `http://18.205.222.251:8000`

### 3. Testing Rápido
1. Ejecutar: **Health Check** → Debe responder `200 OK`
2. Ejecutar: **Register Client User** → Crear usuario de prueba
3. Ejecutar: **Login Client** → Obtener token de acceso
4. Ejecutar: **List All Funds** → Ver fondos disponibles
5. Ejecutar: **Subscribe to Fund** → Realizar suscripción

## 🛡️ Servicios Configurados

### ✅ Backend (FastAPI)
- **Puerto:** 8000
- **Estado:** ✅ Funcionando
- **Features:** Autenticación, Fondos, Transacciones, Notificaciones

### ✅ Base de Datos (MongoDB)
- **Puerto:** 27017
- **Estado:** ✅ Conectada
- **Datos:** Fondos iniciales cargados

### ✅ Notificaciones
- **Email:** ✅ Gmail SMTP configurado (gmkronox@gmail.com)
- **SMS:** ✅ Twilio configurado (+18573808541)

### ✅ Infraestructura (AWS)
- **Instancia:** EC2 t3.micro (Free Tier)
- **OS:** Amazon Linux 2
- **Docker:** ✅ Contenedores funcionando
- **SSH:** `ssh -i btg-pactual-key.pem ec2-user@18.205.222.251`

## 📊 Pruebas de Funcionalidad

### Flujo Completo Recomendado:
1. **Health Check** → Verificar API activa
2. **Registro de Usuario** → Crear cuenta cliente
3. **Login** → Autenticación y obtener JWT
4. **Listar Fondos** → Ver opciones disponibles
5. **Suscribirse a Fondo** → Realizar inversión
6. **Historial de Transacciones** → Verificar operación
7. **Cancelar Suscripción** → Probar cancelación

### Casos de Error:
- Login con credenciales inválidas
- Acceso sin token de autenticación
- Suscripción con fondos insuficientes
- Consultar fondo inexistente

## ⚡ Comandos Útiles

### Verificar Estado de la Aplicación:
```bash
curl http://18.205.222.251:8000/health
```

### Acceder por SSH:
```bash
ssh -i btg-pactual-key.pem ec2-user@18.205.222.251
```

### Ver Logs de la Aplicación:
```bash
ssh -i btg-pactual-key.pem ec2-user@18.205.222.251 'cd btg-pactual/backend && sudo docker-compose logs backend --tail=20'
```

## 🎉 ¡Listo para Testing!

Tu aplicación BTG Pactual está **completamente desplegada y funcional** en AWS. 

**Próximos pasos:**
1. Usar Postman con el environment de producción
2. Probar todos los endpoints de la API
3. Verificar notificaciones por email/SMS
4. Realizar testing completo de funcionalidades

---

**Fecha de despliegue:** 27 de Agosto 2025  
**Entorno:** AWS EC2 - Producción  
**Estado:** ✅ Operacional
