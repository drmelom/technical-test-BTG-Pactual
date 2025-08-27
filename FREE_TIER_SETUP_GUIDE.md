# 🆓 Guía Completa - BTG Pactual Funds 100% GRATUITO
## Configuración paso a paso usando solo servicios gratuitos

---

## 📧 **PASO 1: Configurar Gmail SMTP (100% GRATIS)**

### 🎯 **Beneficios:**
- ✅ **$0 USD/mes** - Completamente gratis
- ✅ **500 emails/día** - Suficiente para desarrollo y pruebas
- ✅ **Sin límite de tiempo** - No expira como otros free tiers

### 📝 **Instrucciones detalladas:**

#### **1.1. Habilitar autenticación de 2 factores en Gmail**
1. Ve a [Gmail](https://mail.google.com) con tu cuenta
2. Click en tu foto de perfil → **"Gestionar tu cuenta de Google"**
3. Ve a **"Seguridad"** en el menú lateral
4. En **"Iniciar sesión en Google"**, habilita la **"Verificación en 2 pasos"**
5. Sigue las instrucciones para configurar con tu teléfono

#### **1.2. Generar contraseña de aplicación**
1. En la misma página de **"Seguridad"**
2. Busca **"Contraseñas de aplicaciones"** (aparece después de habilitar 2FA)
3. Click en **"Contraseñas de aplicaciones"**
4. Selecciona **"Correo"** y **"Otro (nombre personalizado)"**
5. Escribe: **"BTG Pactual Funds API"**
6. **¡IMPORTANTE!** Copia la contraseña de 16 caracteres que aparece
   - Formato: `abcd efgh ijkl mnop`

#### **1.3. Configurar variables de entorno**

**En desarrollo local (.env):**
```bash
# Email GRATUITO con Gmail SMTP
GMAIL_SMTP_USER=tu-email@gmail.com
GMAIL_SMTP_PASSWORD=abcd efgh ijkl mnop  # La contraseña de aplicación generada
```

**En AWS EC2 (variables de entorno):**
```bash
export GMAIL_SMTP_USER="tu-email@gmail.com"
export GMAIL_SMTP_PASSWORD="abcd efgh ijkl mnop"
```

#### **1.4. Verificar configuración**
Ejecuta el sistema y busca en logs:
```bash
✅ Email GRATUITO enviado exitosamente a: cliente@example.com vía Gmail SMTP
📊 Límite diario Gmail: 500 emails (100% gratis)
```

---

## 📱 **PASO 2: Configurar Twilio SMS FREE ($15 USD de crédito GRATIS)**

### 🎯 **Beneficios:**
- ✅ **$15 USD gratis** al registrarte
- ✅ **~265 SMS gratuitos** en Colombia ($0.057 USD/SMS)
- ✅ **Números virtuales** incluidos

### 📝 **Instrucciones detalladas:**

#### **2.1. Crear cuenta Twilio**
1. Ve a [Twilio.com](https://www.twilio.com)
2. Click en **"Try Twilio free"** o **"Start building for free"**
3. Completa el registro con:
   - Email válido
   - Contraseña fuerte
   - Número de teléfono para verificación

#### **2.2. Verificar teléfono y obtener créditos**
1. Verifica tu número de teléfono con el código SMS
2. **¡Automáticamente recibes $15 USD de crédito!**
3. En el dashboard verás: **"Trial Balance: $15.00"**

#### **2.3. Obtener credenciales**
1. En el **Twilio Console**, ve a **"Account"** → **"Account Info"**
2. Copia estos valores:
   - **Account SID**: `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - **Auth Token**: Click en **"Show"** y copia el token

#### **2.4. Comprar número telefónico (GRATIS con crédito)**
1. Ve a **"Phone Numbers"** → **"Manage"** → **"Buy a number"**
2. Selecciona país: **"United States"** (más barato)
3. Busca números disponibles
4. Selecciona uno y click **"Buy"**
5. **Costo:** ~$1 USD/mes (se descuenta de tu crédito de $15)

#### **2.5. Configurar variables de entorno**

**En desarrollo local (.env):**
```bash
# SMS GRATUITO con Twilio ($15 USD de crédito)
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=tu_auth_token_aqui
TWILIO_PHONE_NUMBER=+1234567890  # El número que compraste
```

**En AWS EC2:**
```bash
export TWILIO_ACCOUNT_SID="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export TWILIO_AUTH_TOKEN="tu_auth_token_aqui"
export TWILIO_PHONE_NUMBER="+1234567890"
```

#### **2.6. Verificar configuración**
Ejecuta el sistema y busca en logs:
```bash
✅ SMS GRATUITO enviado exitosamente a: +573001234567
📊 SID: SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
💰 Usando crédito FREE TIER de Twilio ($15 USD gratis)
```

#### **2.7. Monitorear crédito restante**
- Ve al **Twilio Console** → **"Billing"**
- Verifica tu **"Account Balance"**
- Con $15 USD tienes ~265 SMS en Colombia

---

## ☁️ **PASO 3: Configurar AWS Free Tier (12 meses GRATIS)**

### 🎯 **Beneficios:**
- ✅ **t2.micro EC2** - 750 horas/mes (24/7 durante 1 año)
- ✅ **30 GB EBS** - Almacenamiento gratis
- ✅ **1 Elastic IP** - IP pública fija gratis
- ✅ **5 GB CloudWatch** - Logs y métricas
- ✅ **MongoDB containerizado** - Base de datos gratis

### 📝 **Instrucciones detalladas:**

#### **3.1. Crear cuenta AWS (si no tienes)**
1. Ve a [AWS](https://aws.amazon.com)
2. Click **"Crear cuenta de AWS"**
3. **IMPORTANTE:** Necesitas tarjeta de crédito para verificación
   - No te cobrarán si te mantienes en Free Tier
   - AWS te notifica si vas a exceder límites

#### **3.2. Configurar credenciales AWS**
1. Ve al **IAM Console**
2. **"Users"** → **"Add user"**
3. Nombre: `btg-terraform-user`
4. **"Programmatic access"** ✅
5. **"Attach existing policies"** → **"AdministratorAccess"**
6. Copia **Access Key ID** y **Secret Access Key**

#### **3.3. Instalar herramientas**
```bash
# Instalar Terraform
# Windows (usando Chocolatey):
choco install terraform

# O descargar desde: https://www.terraform.io/downloads

# Instalar AWS CLI
# Windows:
choco install awscli

# Configurar credenciales
aws configure
# AWS Access Key ID: tu-access-key
# AWS Secret Access Key: tu-secret-key  
# Default region: us-east-1
# Default output format: json
```

#### **3.4. Clonar y desplegar infraestructura**
```bash
# Clonar proyecto
cd "C:\Users\tu-usuario\Desktop"
git clone https://github.com/tu-usuario/btg-pactual-funds

# Ir a directorio de infraestructura
cd btg-pactual-funds\infrastructure\terraform

# Inicializar Terraform
terraform init

# Planificar despliegue (revisar qué se va a crear)
terraform plan

# Aplicar cambios (crear recursos)
terraform apply
```

#### **3.5. Verificar recursos creados**
1. Ve al **EC2 Console**
2. Verifica que tienes:
   - ✅ 1 instancia **t2.micro** ejecutándose
   - ✅ 1 **Elastic IP** asignada
   - ✅ **Security Group** con puertos abiertos
   - ✅ **VPC** y **subnets** creadas

#### **3.6. Acceder a tu servidor**
```bash
# Obtener IP pública
aws ec2 describe-instances --query 'Reservations[*].Instances[*].PublicIpAddress'

# Acceder a Mongo Express (interfaz web de MongoDB)
# http://TU-IP-PUBLICA:8081
# Usuario: admin
# Contraseña: btgpactual123
```

---

## 🚀 **PASO 4: Deployar la aplicación BTG Pactual**

### 📝 **Deploy en servidor AWS:**

#### **4.1. Conectar al servidor**
```bash
# Generar key pair en AWS EC2 Console
# Descargar archivo .pem

# Conectar vía SSH (desde terminal local)
ssh -i "tu-key.pem" ec2-user@TU-IP-PUBLICA
```

#### **4.2. Verificar servicios base**
```bash
# En el servidor EC2:
cd /opt/btg-pactual
./status.sh

# Deberías ver:
# ✅ MongoDB corriendo
# ✅ Mongo Express disponible
# ✅ Docker funcionando
```

#### **4.3. Clonar y deployar aplicación**
```bash
# En el servidor EC2:
cd /opt/btg-pactual
git clone https://github.com/tu-usuario/btg-pactual-funds.git app

# Copiar archivos de aplicación
cp app/backend/* .
cp app/backend/docker-compose.yml ./docker-compose-app.yml

# Configurar variables de entorno
nano .env
# Agregar:
MONGO_URI=mongodb://btguser:BtgUser123!@mongodb:27017/btg_funds_db
GMAIL_SMTP_USER=tu-email@gmail.com
GMAIL_SMTP_PASSWORD=tu-app-password
TWILIO_ACCOUNT_SID=tu-account-sid
TWILIO_AUTH_TOKEN=tu-auth-token
TWILIO_PHONE_NUMBER=tu-phone-number

# Deployar aplicación
docker-compose -f docker-compose-app.yml up -d

# Verificar logs
docker-compose logs -f
```

#### **4.4. Probar aplicación**
```bash
# Verificar que la API responde
curl http://localhost:8000/health

# Verificar externamente
curl http://TU-IP-PUBLICA:8000/health

# Deberías ver:
# {"status": "healthy", "database": "connected"}
```

---

## 💰 **PASO 5: Monitoreo de costos (TODO GRATIS)**

### 📊 **Resumen de costos:**
- **Gmail SMTP:** $0 USD/mes
- **Twilio SMS:** $0 USD (primeros $15 gratis)
- **AWS Free Tier:**
  - **EC2 t2.micro:** $0 USD (750 horas/mes)
  - **EBS 30GB:** $0 USD
  - **Elastic IP:** $0 USD
  - **Data Transfer:** $0 USD (primeros 15GB)

### 🎯 **Total estimado primer año: $0 USD**

### ⚠️ **Alertas de facturación AWS:**
1. Ve a **AWS Billing Console**
2. **"Billing preferences"**
3. Habilita **"Receive Free Tier Usage Alerts"**
4. Habilita **"Receive Billing Alerts"**
5. Configura alerta para **$1 USD** (por seguridad)

---

## 🔍 **PASO 6: Testing y validación**

### 📋 **Verificar funcionalidad completa:**

#### **6.1. Probar API localmente**
```bash
# Ejecutar tests
cd backend
python test_api.py

# Deberías ver:
# ✅ 8/8 tests passed
# ✅ All endpoints working
```

#### **6.2. Probar notificaciones**
```bash
# Registro de usuario y suscripción
curl -X POST http://TU-IP:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!",
    "full_name": "Test User",
    "phone_number": "+573001234567",
    "notification_preference": "both"
  }'

# Login
curl -X POST http://TU-IP:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test@example.com", 
    "password": "Test123!"
  }'

# Suscribirse a fondo (debería enviar email Y SMS)
curl -X POST http://TU-IP:8000/api/v1/transactions/subscribe \
  -H "Authorization: Bearer TU-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"fund_id": 1, "amount": 100000}'
```

#### **6.3. Verificar logs**
```bash
# En servidor EC2:
docker-compose logs | grep -E "(Email|SMS|GRATUITO)"

# Deberías ver:
# ✅ Email GRATUITO enviado exitosamente
# ✅ SMS GRATUITO enviado exitosamente
# 💰 Usando crédito FREE TIER
```

---

## 🎉 **¡FELICIDADES! Sistema completamente GRATUITO funcionando**

### ✅ **Lo que tienes ahora:**
1. **API FastAPI** completa en AWS Free Tier
2. **Base de datos MongoDB** containerizada (gratis)
3. **Notificaciones email** vía Gmail SMTP (gratis)
4. **Notificaciones SMS** vía Twilio ($15 crédito)
5. **Interfaz Mongo Express** para gestión de BD
6. **Monitoreo CloudWatch** básico
7. **IP pública fija** con Elastic IP

### 📈 **Escalabilidad futura:**
- **Free Tier dura 12 meses**
- **Después:** ~$10-15 USD/mes
- **Para más SMS:** Recargar crédito Twilio
- **Para más emails:** Migrar a AWS SES

### 🎯 **URLs importantes:**
- **API:** `http://TU-IP-PUBLICA:8000`
- **Docs:** `http://TU-IP-PUBLICA:8000/docs`
- **Mongo Express:** `http://TU-IP-PUBLICA:8081`
- **Health Check:** `http://TU-IP-PUBLICA:8000/health`

### 📞 **Soporte:**
- **AWS Free Tier:** [Documentación oficial](https://aws.amazon.com/free)
- **Gmail SMTP:** [Configuración](https://support.google.com/accounts/answer/185833)
- **Twilio Free:** [Dashboard de crédito](https://console.twilio.com/billing)

**🎊 ¡Tu plataforma BTG Pactual Funds está lista y es 100% GRATUITA!**
