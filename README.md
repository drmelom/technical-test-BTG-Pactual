# 🏦 BTG Pactual - Sistema de Gestión de Fondos de Inversión

[![Status](https://img.shields.io/badge/Status-DEPLOYED-success)](http://18.205.222.251:8000/health)
[![AWS](https://img.shields.io/badge/AWS-EC2-orange)](http://18.205.222.251:8000)
[![API](https://img.shields.io/badge/API-FastAPI-green)](http://18.205.222.251:8000/docs)
[![Database](https://img.shields.io/badge/Database-MongoDB-darkgreen)](http://18.205.222.251:8081)

> **🚀 Aplicación DESPLEGADA y FUNCIONANDO en AWS EC2**  
> Sistema completo de gestión de fondos de inversión con autenticación JWT, notificaciones automáticas por email/SMS, y arquitectura basada en microservicios con FastAPI y MongoDB.

---

## 🎯 **APLICACIÓN YA DESPLEGADA - LISTA PARA EVALUACIÓN**

### 🌐 **URLs de Producción (AWS EC2):**

| 🎯 **Servicio** | � **URL** | 📊 **Estado** | 🎪 **Descripción** |
|-----------------|------------|---------------|-------------------|
| **🌐 API Principal** | [http://18.205.222.251:8000](http://18.205.222.251:8000) | ✅ **ACTIVO** | API REST completa |
| **📚 Documentación Swagger** | [http://18.205.222.251:8000/docs](http://18.205.222.251:8000/docs) | ✅ **DISPONIBLE** | Testing interactivo |
| **❤️ Health Check** | [http://18.205.222.251:8000/health](http://18.205.222.251:8000/health) | ✅ **OPERACIONAL** | Monitoreo de estado |
| **🍃 MongoDB Express** | [http://18.205.222.251:8081](http://18.205.222.251:8081) | ✅ **ADMIN UI** | Base de datos (admin/admin) |

### ⚡ **Verificación Rápida:**
```bash
# Verificar que la API está funcionando
curl http://18.205.222.251:8000/health
# Respuesta esperada: {"status":"healthy","timestamp":"..."}

# Verificar endpoints principales
curl http://18.205.222.251:8000/api/v1/funds/ | head -5
```

---

## 📋 **CHECKLIST COMPLETO DE VALIDACIÓN**

### 🔥 **Prueba Rápida (5 minutos) - RECOMENDADO**

#### ✅ **1. Verificar Estado General**
- [ ] **Health Check:** [http://18.205.222.251:8000/health](http://18.205.222.251:8000/health) → Debe responder `{"status":"healthy"}`
- [ ] **Swagger UI:** [http://18.205.222.251:8000/docs](http://18.205.222.251:8000/docs) → Interface interactiva funcionando
- [ ] **MongoDB UI:** [http://18.205.222.251:8081](http://18.205.222.251:8081) → Login con admin/admin

#### ✅ **2. Probar con Postman (SUPER FÁCIL)**
1. **Importar colección:** `postman/BTG_Pactual_Funds_API.postman_collection.json`
2. **Ejecutar "Health Check"** → Estado 200 OK
3. **Ejecutar "Register Client User"** → Nuevo usuario creado
4. **Ejecutar "Login Client"** → Token JWT generado automáticamente
5. **Ejecutar "List All Funds"** → Ver fondos disponibles
6. **Ejecutar "Subscribe to Fund"** → Suscripción exitosa + Notificación
7. **Ejecutar "Get Transaction History"** → Verificar transacción registrada

---

### 🧪 **Prueba Completa (15 minutos) - EVALUACIÓN TÉCNICA**

#### **Fase 1: Autenticación y Usuarios**
- [ ] **Registro Admin:** `POST /api/v1/auth/register` con `is_admin: true`
- [ ] **Registro Cliente:** `POST /api/v1/auth/register` con `is_admin: false`
- [ ] **Login exitoso:** `POST /api/v1/auth/login` → Token JWT válido
- [ ] **Login fallido:** Credenciales incorrectas → Error 401
- [ ] **Acceso protegido:** `GET /api/v1/users/me` con/sin token
- [ ] **Perfil usuario:** Verificar datos y balance inicial ($500,000)

#### **Fase 2: Gestión de Fondos**
- [ ] **Listar fondos:** `GET /api/v1/funds/` → 4 fondos precargados
- [ ] **Fondo por ID:** `GET /api/v1/funds/{fund_id}` → Detalles específicos
- [ ] **Filtrar por categoría:** `GET /api/v1/funds/?category=FPV` → Filtrado correcto
- [ ] **Fondo inexistente:** ID inválido → Error 404
- [ ] **Validar datos:** Nombre, categoría, monto mínimo, descripción

#### **Fase 3: Transacciones**
- [ ] **Suscripción exitosa:** Fondos suficientes → Transacción creada
- [ ] **Suscripción fallida:** Fondos insuficientes → Error 400
- [ ] **Balance actualizado:** Verificar descuento después de suscripción
- [ ] **Historial completo:** `GET /api/v1/transactions/history` → Todas las transacciones
- [ ] **Historial por fondo:** Filtrado por fund_id específico
- [ ] **Cancelación activa:** `DELETE /api/v1/transactions/cancel/{id}` → Exitosa
- [ ] **Cancelación inválida:** Suscripción inexistente → Error 404

#### **Fase 4: Notificaciones (Opcional)**
- [ ] **Email de suscripción:** Verificar en gmkronox@gmail.com
- [ ] **SMS de cancelación:** Verificar en número configurado
- [ ] **Logs de notificaciones:** En MongoDB o logs del servidor

#### **Fase 5: Casos de Error**
- [ ] **Sin autenticación:** Endpoints protegidos → Error 401
- [ ] **Token expirado:** JWT inválido → Error 401
- [ ] **Datos inválidos:** Campos requeridos vacíos → Error 422
- [ ] **Recursos inexistentes:** IDs inválidos → Error 404
- [ ] **Lógica de negocio:** Validaciones específicas → Errores correspondientes

#### **Fase 6: Integración de Datos**
- [ ] **MongoDB Express:** Ver colecciones `users`, `funds`, `transactions`
- [ ] **Persistencia:** Datos guardados correctamente
- [ ] **Consistencia:** Relaciones entre usuarios y transacciones
- [ ] **Datos iniciales:** 4 fondos precargados en BD

---

## 🚀 **INSTRUCCIONES DE TESTING**

### 📱 **Opción 1: Postman (RECOMENDADO)**

```bash
# 1. Importar colección
# Archivo: postman/BTG_Pactual_Funds_API.postman_collection.json
# ✅ Ya viene configurado para producción (AWS EC2)

# 2. Ejecutar secuencialmente:
# → Health Check
# → Register Client User  
# → Login Client
# → List All Funds
# → Subscribe to Fund
# → Get Transaction History
# → Cancel Fund Subscription
```

### 🌐 **Opción 2: Swagger UI**

```bash
# 1. Abrir documentación interactiva
# URL: http://18.205.222.251:8000/docs

# 2. Seguir el flujo:
# → POST /api/v1/auth/register (crear usuario)
# → POST /api/v1/auth/login (obtener token)
# → Authorize (usar token en candado 🔒)
# → GET /api/v1/funds/ (ver fondos)
# → POST /api/v1/transactions/subscribe (suscribirse)
# → GET /api/v1/transactions/history (ver historial)
```

### 💻 **Opción 3: cURL**

```bash
# Health Check
curl -X GET http://18.205.222.251:8000/health

# Registro de usuario
curl -X POST http://18.205.222.251:8000/api/v1/auth/register 
  -H "Content-Type: application/json" 
  -d '{
    "email": "test@test.com",
    "password": "test123",
    "full_name": "Usuario Test",
    "phone": "+1234567890",
    "is_admin": false
  }'

# Login y obtener token
curl -X POST http://18.205.222.251:8000/api/v1/auth/login 
  -H "Content-Type: application/json" 
  -d '{
    "email": "test@test.com",
    "password": "test123"
  }'

# Usar token para endpoints protegidos
TOKEN="tu_token_aqui"
curl -X GET http://18.205.222.251:8000/api/v1/users/me 
  -H "Authorization: Bearer $TOKEN"

# Listar fondos
curl -X GET http://18.205.222.251:8000/api/v1/funds/ 
  -H "Authorization: Bearer $TOKEN"

# Suscribirse a un fondo
curl -X POST http://18.205.222.251:8000/api/v1/transactions/subscribe 
  -H "Authorization: Bearer $TOKEN" 
  -H "Content-Type: application/json" 
  -d '{
    "fund_id": "FPV_BTG_PACTUAL_RECAUDADORA",
    "amount": 75000
  }'
```

---

## 📊 **ARQUITECTURA Y FUNCIONALIDADES**

### 🏗️ **Stack Tecnológico**
- **Backend:** FastAPI (Python 3.9+)
- **Base de Datos:** MongoDB 
- **Autenticación:** JWT (JSON Web Tokens)
- **Notificaciones:** Gmail SMTP + Twilio SMS
- **Infraestructura:** AWS EC2 t3.micro (Free Tier)
- **Containerización:** Docker + Docker Compose
- **Infraestructura como Código:** Terraform

### 🔧 **Funcionalidades Principales**

#### **1. 👤 Gestión de Usuarios**
- ✅ Registro de usuarios (administrador/cliente)
- ✅ Autenticación con JWT
- ✅ Gestión de perfiles
- ✅ Balance inicial de $500,000 COP

#### **2. 💰 Gestión de Fondos**
- ✅ 4 fondos precargados:
  - **FPV_BTG_PACTUAL_RECAUDADORA** (FPV) - Min: $75,000
  - **FDO-ACCIONES** (FIC) - Min: $250,000  
  - **FPV_BTG_PACTUAL_ECOPETROL** (FPV) - Min: $125,000
  - **DEUDA_PRIVADA** (FIC) - Min: $50,000
- ✅ Filtrado por categoría (FPV, FIC)
- ✅ Información detallada de cada fondo

#### **3. 💼 Transacciones**
- ✅ Suscripción a fondos con validación de balance
- ✅ Cancelación de suscripciones activas
- ✅ Historial completo de transacciones
- ✅ Filtrado de historial por fondo
- ✅ Actualización automática de balances

#### **4. 📧 Notificaciones Automáticas**
- ✅ **Email:** Confirmaciones de suscripción/cancelación
- ✅ **SMS:** Alertas de transacciones importantes
- ✅ **Configuración:** Gmail SMTP + Twilio API

#### **5. 🛡️ Seguridad**
- ✅ Autenticación JWT con expiración
- ✅ Validación de datos de entrada
- ✅ Manejo de errores HTTP estándar
- ✅ Protección de endpoints sensibles

#### **6. 📈 Monitoreo**
- ✅ Health check endpoint
- ✅ Logs de aplicación
- ✅ Interface de base de datos (MongoDB Express)
- ✅ Documentación interactiva (Swagger UI)

---

## 📁 **Estructura del Proyecto**

```
📦 technical-test-BTG-Pactual/
├── 📄 README.md                     # Este archivo - Documentación principal
├── 📄 prueba_tecnica_back_end 4.pdf # Especificaciones del proyecto
├── 🖥️ backend/                      # Aplicación FastAPI
│   ├── 📄 main.py                   # Punto de entrada de la aplicación
│   ├── 📄 requirements.txt          # Dependencias Python
│   ├── 📄 Dockerfile                # Imagen de contenedor
│   ├── 📄 docker-compose.yml        # Orquestación local
│   ├── 📄 .env                      # Variables de entorno
│   ├── 📄 test_api.py               # Tests automatizados
│   └── 📁 app/                      # Código fuente principal
│       ├── 📁 api/                  # Endpoints REST
│       │   ├── 📄 schemas.py        # Modelos Pydantic
│       │   └── 📁 v1/               # API versión 1
│       │       ├── 📄 auth.py       # Autenticación
│       │       ├── 📄 users.py      # Gestión de usuarios
│       │       ├── 📄 funds.py      # Gestión de fondos
│       │       └── 📄 transactions.py # Transacciones
│       ├── 📁 core/                 # Configuración central
│       │   ├── 📄 config.py         # Settings de la aplicación
│       │   ├── 📄 database.py       # Conexión MongoDB
│       │   ├── 📄 security.py       # JWT y encriptación
│       │   └── 📄 middleware.py     # Middleware CORS/seguridad
│       ├── 📁 services/             # Lógica de negocio
│       │   ├── 📄 auth_service.py   # Servicio de autenticación
│       │   ├── 📄 fund_service.py   # Servicio de fondos
│       │   ├── 📄 transaction_service.py # Servicio de transacciones
│       │   └── 📄 notification_service.py # Notificaciones
│       └── 📁 repositories/         # Acceso a datos
│           ├── 📄 user_repository.py      # CRUD usuarios
│           ├── 📄 fund_repository.py      # CRUD fondos
│           ├── 📄 transaction_repository.py # CRUD transacciones
│           └── 📄 subscription_repository.py # CRUD suscripciones
├── 🚀 deployment/                   # Infraestructura AWS
│   ├── 📄 README.md                 # Guía de despliegue
│   ├── 📄 deploy-ec2-simple.tf      # Configuración Terraform
│   ├── 📄 user_data_complete.sh     # Script de inicialización EC2
│   ├── 📄 terraform.tfvars.example  # Plantilla de variables
│   ├── 📄 btg-pactual-key.pem      # Llave SSH (generada automáticamente)
│   └── 📄 terraform.tfstate         # Estado de infraestructura
├── 📬 postman/                      # Testing API
│   ├── 📄 README.md                                        # Guía de testing
│   ├── 📄 BTG_Pactual_Funds_API.postman_collection.json   # Colección principal ⭐
│   ├── 📄 BTG_Pactual_Local_Environment.postman_environment.json # Entorno local
│   ├── 📄 BTG_Pactual_Production_Environment.postman_environment.json # Entorno AWS
│   └── 📄 AWS_PRODUCTION_GUIDE.md                         # Guía de testing en AWS
└── 📚 docs/                         # Documentación adicional
    ├── 📄 ARQUITECTURA.md           # Diseño de la arquitectura
    └── 📄 DEPLOYMENT_GUIDE.md       # Guía detallada de despliegue
```

---

## 🔗 **Endpoints de la API**

### 🔒 **Autenticación**
| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| `POST` | `/api/v1/auth/register` | Registro de usuarios | ❌ |
| `POST` | `/api/v1/auth/login` | Autenticación | ❌ |

### 👤 **Usuarios**
| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/v1/users/me` | Perfil del usuario actual | ✅ |

### 💰 **Fondos**
| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/v1/funds/` | Listar todos los fondos | ✅ |
| `GET` | `/api/v1/funds/{fund_id}` | Obtener fondo por ID | ✅ |
| `GET` | `/api/v1/funds/?category={cat}` | Filtrar por categoría | ✅ |

### 💼 **Transacciones**
| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| `POST` | `/api/v1/transactions/subscribe` | Suscribirse a un fondo | ✅ |
| `DELETE` | `/api/v1/transactions/cancel/{sub_id}` | Cancelar suscripción | ✅ |
| `GET` | `/api/v1/transactions/history` | Historial de transacciones | ✅ |
| `GET` | `/api/v1/transactions/history?fund_id={id}` | Historial por fondo | ✅ |

### ❤️ **Monitoreo**
| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| `GET` | `/health` | Estado de la aplicación | ❌ |

---

## 💡 **Datos de Prueba Precargados**

### 💰 **Fondos Disponibles:**

| 🎯 **ID del Fondo** | 📊 **Nombre** | 🏷️ **Categoría** | 💵 **Monto Mínimo** |
|---------------------|---------------|-------------------|---------------------|
| `FPV_BTG_PACTUAL_RECAUDADORA` | FPV BTG Pactual Recaudadora | FPV | $75,000 COP |
| `FDO-ACCIONES` | Fondo de Acciones | FIC | $250,000 COP |
| `FPV_BTG_PACTUAL_ECOPETROL` | FPV BTG Pactual Ecopetrol | FPV | $125,000 COP |
| `DEUDA_PRIVADA` | Fondo de Deuda Privada | FIC | $50,000 COP |

### 👤 **Usuario de Prueba (Opcional):**
```json
{
  "email": "test@btgpactual.com",
  "password": "test123",
  "full_name": "Usuario de Prueba BTG",
  "phone": "+573001234567",
  "is_admin": false,
  "balance": 500000
}
```

---

## 🔧 **Acceso SSH (Opcional para Debugging)**

```bash
# Conectar a la instancia EC2
cd deployment/
ssh -i ./btg-pactual-key.pem ec2-user@18.205.222.251

# Ver logs de la aplicación
sudo docker-compose logs backend --tail=50

# Ver estado de contenedores
sudo docker-compose ps

# Verificar configuración
sudo docker-compose exec backend env | grep -E "(MONGO|GMAIL|TWILIO)"

# Reiniciar servicios si es necesario
sudo docker-compose restart
```

---

## 🛠️ **Desarrollo Local (Opcional)**

Si quieres ejecutar la aplicación localmente además de probar la versión desplegada:

### **Pre-requisitos:**
- Docker y Docker Compose
- Python 3.9+ (opcional)
- MongoDB (manejado por Docker)

### **Ejecución Local:**
```bash
# Clonar repositorio
git clone https://github.com/drmelom/technical-test-BTG-Pactual.git
cd technical-test-BTG-Pactual/backend

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# Ejecutar con Docker
docker-compose up -d

# Verificar servicios
docker-compose ps
curl http://localhost:8000/health

# Ver logs
docker-compose logs -f backend
```

### **URLs Locales:**
- **API:** http://localhost:8000
- **Docs:** http://localhost:8000/docs  
- **MongoDB Express:** http://localhost:8081

---

## 🚀 **Replicar Despliegue en AWS**

### **Pre-requisitos:**
- Cuenta AWS con acceso programático
- Terraform instalado
- AWS CLI configurado

### **Despliegue Automatizado:**
```bash
cd deployment/

# Configurar variables
cp terraform.tfvars.example terraform.tfvars
# Editar: aws_region, instance_type, etc.

# Inicializar Terraform
terraform init

# Planificar infraestructura
terraform plan

# Aplicar cambios
terraform apply -auto-approve

# Obtener IP pública
terraform output public_ip
```

### **Costos Estimados:**
- **EC2 t3.micro:** $0/mes (Free Tier)
- **EBS 8GB:** $0/mes (Free Tier) 
- **Data Transfer:** Mínimo
- **Total:** **$0/mes** en Free Tier ✅

---

## 🎯 **Criterios de Evaluación**

### ✅ **Funcionalidad (40%)**
- [ ] Registro y autenticación de usuarios
- [ ] Gestión completa de fondos
- [ ] Transacciones (suscripción/cancelación)
- [ ] Validaciones de negocio
- [ ] Notificaciones por email/SMS

### ✅ **Arquitectura (30%)**
- [ ] Diseño de API REST
- [ ] Separación de responsabilidades
- [ ] Manejo de errores
- [ ] Seguridad (JWT, validaciones)
- [ ] Base de datos bien estructurada

### ✅ **Infraestructura (20%)**
- [ ] Despliegue en cloud (AWS)
- [ ] Containerización (Docker)
- [ ] Automatización (Terraform)
- [ ] Configuración de producción
- [ ] Monitoreo básico

### ✅ **Documentación (10%)**
- [ ] README completo ⭐
- [ ] Documentación de API (Swagger)
- [ ] Instrucciones claras de testing
- [ ] Guías de despliegue
- [ ] Colección de Postman

---

## 📞 **Soporte y Contacto**

### 🔧 **Troubleshooting:**

**❌ Error "Could not get any response"**
- Verificar que la instancia EC2 esté activa: [Health Check](http://18.205.222.251:8000/health)
- Confirmar URLs en la documentación

**❌ Error "401 Unauthorized"**  
- Ejecutar login antes de endpoints protegidos
- Verificar que el token JWT se haya guardado correctamente

**❌ Error "Connection refused"**
- La aplicación puede estar reiniciándose (esperar 1-2 minutos)
- Verificar estado en MongoDB Express

### 📧 **Contacto del Desarrollador:**
- **Email:** gmkronox@gmail.com
- **GitHub:** [drmelom](https://github.com/drmelom)
- **Proyecto:** [technical-test-BTG-Pactual](https://github.com/drmelom/technical-test-BTG-Pactual)

---

## 📈 **Estado del Proyecto**

| Componente | Estado | Última Verificación |
|------------|--------|-------------------|
| 🌐 **API Principal** | ✅ **OPERACIONAL** | Agosto 2025 |
| 🗄️ **Base de Datos** | ✅ **CONECTADA** | Agosto 2025 |
| 📧 **Notificaciones Email** | ✅ **CONFIGURADO** | Gmail SMTP |
| 📱 **Notificaciones SMS** | ✅ **CONFIGURADO** | Twilio API |
| ☁️ **Infraestructura AWS** | ✅ **DESPLEGADA** | EC2 t3.micro |
| 📚 **Documentación** | ✅ **COMPLETA** | Swagger UI |
| 🧪 **Testing** | ✅ **DISPONIBLE** | Postman Collection |

---

**📝 Versión:** 2.0 - Production Ready  
**🗓️ Última actualización:** Agosto 2025  
**👨‍💻 Desarrollado por:** BTG Pactual - Technical Test Team  
**🏆 Estado:** ✅ **LISTO PARA EVALUACIÓN**

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

### 📱 **Cómo probar con Postman:**

1. **Importar SOLO la colección** desde `postman/BTG_Pactual_Funds_API.postman_collection.json` ⭐
2. **¡Ya está listo!** - La colección viene configurada para la aplicación desplegada
3. **Ejecutar los requests** - todos apuntan automáticamente a http://18.205.222.251:8000

✅ **No necesitas importar environments adicionales** - Todo está incluido en la colección

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