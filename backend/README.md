# 🏦 BTG Pactual - Sistema de Gestión de Fondos de Inversión

## 📋 Descripción del Proyecto

Sistema backend desarrollado en FastAPI para la gestión de fondos de inversión de BTG Pactual. Permite a los usuarios suscribirse a fondos, cancelar suscripciones, consultar historial de transacciones y recibir notificaciones.

## ✨ Funcionalidades Principales

### 🔐 Autenticación y Autorización
- Registro e inicio de sesión de usuarios
- Autenticación JWT con roles (Admin/Cliente)
- Protección de endpoints por roles

### 💰 Gestión de Fondos
- **Suscripción a fondos**: Los usuarios pueden suscribirse con validación de saldo
- **Cancelación de suscripciones**: Permite cancelar y obtener reembolso
- **Consulta de fondos disponibles**: Lista de fondos con información detallada

### 📊 Historial de Transacciones
- Consulta completa del historial de transacciones
- Filtrado por tipo de transacción y fechas
- Detalle de suscripciones y cancelaciones

### 📱 Sistema de Notificaciones
- Notificaciones por email (Gmail SMTP)
- Notificaciones por SMS (Twilio)
- Simulación para desarrollo sin servicios externos

## 🛠 Tecnologías Utilizadas

- **Framework**: FastAPI 0.104.1
- **Base de Datos**: MongoDB con Beanie ODM
- **Autenticación**: JWT con python-jose
- **Validación**: Pydantic v2
- **Servidor**: Uvicorn
- **Containerización**: Docker & Docker Compose
- **Cloud**: AWS (preparado para deployment)

## 🏗 Arquitectura del Proyecto

```
backend/
├── app/
│   ├── api/v1/          # Endpoints REST API
│   ├── core/            # Configuración y utilidades
│   ├── models/          # Modelos de datos (Beanie)
│   ├── repositories/    # Capa de acceso a datos
│   └── services/        # Lógica de negocio
├── infrastructure/      # Terraform para AWS
├── main.py             # Aplicación principal
├── requirements.txt    # Dependencias Python
└── docker-compose.yml  # Orquestación de servicios
```

## 🚀 Instalación y Ejecución

### Prerrequisitos
- Python 3.11+
- Docker y Docker Compose
- MongoDB (incluido en docker-compose)

### 1. Clonar y preparar el proyecto
```bash
# Clonar el repositorio
cd backend

# Crear archivo .env desde el ejemplo
copy .env.example .env

# Editar .env con tus configuraciones
```

### 2. Ejecutar con Docker (Recomendado)
```bash
# Ejecutar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f backend

# Detener servicios
docker-compose down
```

### 3. Ejecutar en desarrollo local
```bash
# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar MongoDB (requiere Docker)
docker-compose up -d mongodb

# Ejecutar aplicación
python main.py
```

## 📡 Endpoints API

### Autenticación
- `POST /api/v1/auth/register` - Registro de usuario
- `POST /api/v1/auth/login` - Inicio de sesión
- `POST /api/v1/auth/refresh` - Renovar token

### Gestión de Usuarios
- `GET /api/v1/users/me` - Obtener perfil actual
- `PUT /api/v1/users/me` - Actualizar perfil

### Fondos de Inversión
- `GET /api/v1/funds/` - Listar fondos disponibles
- `POST /api/v1/funds/subscribe` - Suscribirse a un fondo
- `POST /api/v1/funds/cancel` - Cancelar suscripción
- `GET /api/v1/funds/subscriptions` - Mis suscripciones

### Transacciones
- `GET /api/v1/transactions/history` - Historial de transacciones
- `GET /api/v1/transactions/{transaction_id}` - Detalle de transacción

## 🎯 Datos de Prueba

### Usuario Administrador (creado automáticamente)
- **Email**: admin@btgpactual.com
- **Password**: Admin123!

### Fondos Disponibles
1. **FPV_BTG_PACTUAL_RECAUDADORA** - COP $75,000 mínimo
2. **FPV_BTG_PACTUAL_ECOPETROL** - COP $125,000 mínimo  
3. **DEUDAPRIVADA** - COP $50,000 mínimo
4. **FDO-ACCIONES** - COP $250,000 mínimo
5. **FPV_BTG_PACTUAL_DINAMICA** - COP $100,000 mínimo

### Usuarios de Prueba
Puedes registrar usuarios que automáticamente tendrán COP $500,000 de saldo inicial.

## 🔧 Configuración de Servicios

### MongoDB
- URL: `mongodb://admin:password123@localhost:27017`
- Base de datos: `btg_pactual`
- Admin UI: http://localhost:8081 (admin/admin)

### Email (Gmail)
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu-email@gmail.com
SMTP_PASSWORD=tu-app-password  # No tu contraseña regular
```

### SMS (Twilio)
```env
TWILIO_ACCOUNT_SID=tu-account-sid
TWILIO_AUTH_TOKEN=tu-auth-token
TWILIO_PHONE_NUMBER=+1234567890
```

## 📖 Documentación API

Una vez ejecutando la aplicación:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🧪 Pruebas de Endpoints

### 1. Registrar Usuario
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "cliente@test.com",
    "password": "Test123!",
    "full_name": "Cliente de Prueba",
    "phone_number": "+57300123456"
  }'
```

### 2. Iniciar Sesión
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "cliente@test.com", 
    "password": "Test123!"
  }'
```

### 3. Suscribirse a Fondo
```bash
curl -X POST "http://localhost:8000/api/v1/funds/subscribe" \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "fund_id": "ID_DEL_FONDO",
    "amount": 100000
  }'
```

## 🔒 Seguridad

- Autenticación JWT obligatoria para endpoints protegidos
- Encriptación de contraseñas con bcrypt
- Validación estricta de datos de entrada
- Headers de seguridad configurados
- Logs de todas las operaciones

## 📊 Monitoreo y Logs

- Logs estructurados en formato JSON
- Middleware de logging para requests/responses
- Health check endpoint: `/health`
- Métricas de tiempo de respuesta en headers

## 🌐 Despliegue en AWS

El proyecto incluye configuración Terraform para despliegue en AWS:

```bash
cd infrastructure/
terraform init
terraform plan
terraform apply
```

### Recursos AWS incluidos:
- EC2 para FastAPI
- DocumentDB (MongoDB compatible)
- ALB (Application Load Balancer)  
- SES para emails
- SNS para SMS
- CloudWatch para logs

## 🤝 Contribución

1. Fork del proyecto
2. Crear rama de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📝 Licencia

Este proyecto es parte de una prueba técnica para BTG Pactual.

## 📞 Soporte

Para preguntas o soporte técnico, contactar al equipo de desarrollo.

---

**Desarrollado con ❤️ para BTG Pactual**
