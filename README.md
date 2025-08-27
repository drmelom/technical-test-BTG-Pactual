# 🏦 BTG Pactual Funds Management API

Sistema de gestión de fondos de inversión con FastAPI, Mongo## 📁 Estructura del Proyecto

```
├── backend/                 # FastAPI application
│   ├── app/                # Application code
│   ├── docker-compose.yml  # Local development
│   ├── Dockerfile          # Container definition
│   └── .env               # Environment variables
├── deployment/              # AWS deployment files
│   ├── deploy-ec2-simple.tf    # Terraform configuration
│   ├── user_data_complete.sh   # EC2 setup script
│   ├── terraform.tfvars.example # Config template
│   └── README.md               # Deployment guide
├── postman/                # API testing
│   ├── BTG_Pactual_Funds_API.postman_collection.json
│   ├── BTG_Pactual_Production_Environment.postman_environment.json ⭐ 
│   └── AWS_PRODUCTION_GUIDE.md    # Guía de testing en AWS
└── docs/                   # Documentation
```

## 🔍 **Acceso SSH a la Instancia (Opcional)**

Si necesitas acceder al servidor para debugging:
```bash
# Desde el directorio deployment/
ssh -i ./btg-pactual-key.pem ec2-user@18.205.222.251

# Ver logs de la aplicación
sudo docker-compose logs backend --tail=20

# Ver estado de contenedores
sudo docker-compose ps
```

## � Despliegue en Producción (Replicar)

Si quieres replicar el despliegue en tu propia cuenta AWS:

1. **Ir a la carpeta de deployment:**
   ```bash
   cd deployment
   ```

2. **Seguir las instrucciones** en `deployment/README.md`

## 🌐 URLs después del despliegue
- API: `http://TU-IP:8000`
- Docs: `http://TU-IP:8000/docs`
- MongoDB Express: `http://TU-IP:8081`

## 💰 Costos
**$0** - Todo ejecutándose en AWS Free Tier

---

## ⚠️ **IMPORTANTE PARA EVALUADORES**

**La aplicación está DESPLEGADA y FUNCIONANDO** en las URLs mostradas arriba. 

✅ **Para validar la prueba técnica:**
1. Usar las URLs de producción: http://18.205.222.251:8000
2. Importar la colección de Postman con environment de producción
3. Probar los endpoints desde Swagger UI: http://18.205.222.251:8000/docs
4. Verificar funcionalidades completas según los casos de uso

**Estado actual:** ✅ **OPERACIONAL** - Listo para evaluaciónnes por email/SMS.

## 🎯 **APLICACIÓN YA DESPLEGADA - LISTA PARA PROBAR**

### 🚀 **URLs de la aplicación en producción (AWS EC2):**

| Servicio | URL | Estado |
|----------|-----|--------|
| **🌐 API Principal** | http://18.205.222.251:8000 | ✅ Funcionando |
| **📚 Documentación Swagger** | http://18.205.222.251:8000/docs | ✅ Disponible |
| **❤️ Health Check** | http://18.205.222.251:8000/health | ✅ Operacional |
| **🍃 MongoDB Express** | http://18.205.222.251:8081 | ✅ Admin UI |

### ⚡ **Prueba rápida de la API:**
```bash
# Verificar que la API está funcionando
curl http://18.205.222.251:8000/health

# Ver documentación interactiva
# Abrir en navegador: http://18.205.222.251:8000/docs
```

### 📱 **Testing con Postman:**
1. Importar archivos de `postman/`:
   - `BTG_Pactual_Funds_API.postman_collection.json`
   - `BTG_Pactual_Production_Environment.postman_environment.json`
2. Seleccionar environment: **"BTG Pactual - Production Environment (AWS)"**
3. Ejecutar la colección completa o endpoints individuales

### 🔧 **Servicios configurados:**
- ✅ **Backend:** FastAPI con autenticación JWT
- ✅ **Base de datos:** MongoDB con datos iniciales
- ✅ **Notificaciones:** Gmail SMTP + Twilio SMS
- ✅ **Infraestructura:** AWS EC2 t3.micro (Free Tier)

## 🚀 Desarrollo Local (Opcional)

Si quieres ejecutar la aplicación localmente además de probar la versión desplegada:

### Desarrollo Local
```bash
cd backend
docker-compose up -d
```

### Producción en AWS (Ya desplegado)
La aplicación ya está desplegada y funcionando en AWS. Ver URLs arriba ⬆️

Para replicar el despliegue:
```bash
cd deployment
cp terraform.tfvars.example terraform.tfvars
# Editar: key_name y repo_url
terraform init
terraform apply
```

## 🧪 **Funcionalidades para Validar**

### 1. **Autenticación y Usuarios** 
- Registro de usuarios (admin/cliente)
- Login con JWT tokens
- Gestión de perfiles

### 2. **Gestión de Fondos**
- Listado de fondos disponibles
- Filtrado por categoría
- Información detallada de cada fondo

### 3. **Transacciones**
- Suscripción a fondos
- Cancelación de suscripciones
- Historial de transacciones
- Validación de balance mínimo

### 4. **Notificaciones**
- Email: Confirmación de suscripciones/cancelaciones
- SMS: Alertas de transacciones
- Configurado con Gmail SMTP y Twilio

### 5. **Casos de Prueba**
- ✅ Suscripción exitosa con fondos suficientes
- ❌ Suscripción fallida con fondos insuficientes
- ✅ Cancelación de suscripción activa
- ❌ Acceso sin autenticación
- ✅ Validación de datos de entrada

## 📊 **Flujo de Testing Recomendado**

1. **Health Check** → `GET /health`
2. **Registro** → `POST /api/v1/auth/register`
3. **Login** → `POST /api/v1/auth/login`
4. **Listar Fondos** → `GET /api/v1/funds/`
5. **Suscribirse** → `POST /api/v1/transactions/subscribe`
6. **Ver Historial** → `GET /api/v1/transactions/history`
7. **Cancelar** → `DELETE /api/v1/transactions/cancel/{subscription_id}`

## � Despliegue en Producción

1. **Ir a la carpeta de deployment:**
   ```bash
   cd deployment
   ```

2. **Seguir las instrucciones** en `deployment/README.md`

## 🌐 URLs después del despliegue
- API: `http://TU-IP:8000`
- Docs: `http://TU-IP:8000/docs`
- MongoDB Express: `http://TU-IP:8000:8081`

## 💰 Costos
$0 - Todo en AWS Free Tier