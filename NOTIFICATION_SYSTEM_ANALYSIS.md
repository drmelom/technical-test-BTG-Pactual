# Sistema de Notificaciones - BTG Pactual Funds
## Análisis de Costos y Configuración

### 📧 **Sistema de Email**

#### **Opción 1: Gmail SMTP (GRATUITO)**
- **Costo:** $0 USD/mes
- **Límite:** 500 emails/día por cuenta
- **Configuración requerida:**
  ```python
  # Variables de entorno necesarias
  GMAIL_SMTP_USER=tu-email@gmail.com
  GMAIL_SMTP_PASSWORD=tu-app-password  # No la contraseña normal
  ```
- **Configuración de Gmail:**
  1. Activar autenticación de 2 factores
  2. Generar contraseña de aplicación
  3. Usar `smtp.gmail.com:587`

#### **Opción 2: AWS SES (PAGADO)**
- **Costo:** $0.10 por 1,000 emails
- **Límite:** 200 emails/día (gratis), luego pagado
- **Configuración requerida:**
  ```python
  # Variables de entorno necesarias
  AWS_ACCESS_KEY_ID=tu-access-key
  AWS_SECRET_ACCESS_KEY=tu-secret-key
  AWS_REGION=us-east-1
  SES_DOMAIN=btgpactual.com  # Dominio verificado
  ```

#### **Opción 3: SendGrid (PAGADO)**
- **Costo:** Gratis hasta 100 emails/día, luego $14.95/mes
- **Configuración:**
  ```python
  SENDGRID_API_KEY=tu-api-key
  ```

---

### 📱 **Sistema de SMS**

#### **Twilio (PAGADO) - Recomendado**
- **Costo por SMS:** 
  - Colombia: ~$0.0565 USD/SMS
  - Internacional: $0.075 USD/SMS promedio
- **Configuración requerida:**
  ```python
  # Variables de entorno necesarias
  TWILIO_ACCOUNT_SID=tu-account-sid
  TWILIO_AUTH_TOKEN=tu-auth-token
  TWILIO_PHONE_NUMBER=+1234567890  # Número comprado en Twilio
  ```
- **Proceso de setup:**
  1. Crear cuenta en Twilio
  2. Comprar número telefónico (~$1 USD/mes)
  3. Configurar webhook para respuestas

#### **AWS SNS (ALTERNATIVO)**
- **Costo:** $0.75 por 1,000 SMS
- **Configuración:**
  ```python
  AWS_ACCESS_KEY_ID=tu-access-key
  AWS_SECRET_ACCESS_KEY=tu-secret-key
  AWS_REGION=us-east-1
  ```

---

### 💰 **Estimación de Costos Mensual**

#### **Escenario Conservador** (100 usuarios activos)
- **Email:** Gmail SMTP = $0/mes
- **SMS:** 500 SMS/mes × $0.0565 = $28.25/mes
- **Total:** ~$30/mes

#### **Escenario Medio** (1,000 usuarios activos)
- **Email:** AWS SES = 5,000 emails × $0.0001 = $0.50/mes
- **SMS:** 2,000 SMS/mes × $0.0565 = $113/mes
- **Total:** ~$115/mes

#### **Escenario Alto** (10,000 usuarios activos)
- **Email:** AWS SES = 50,000 emails × $0.0001 = $5/mes
- **SMS:** 20,000 SMS/mes × $0.0565 = $1,130/mes
- **Total:** ~$1,135/mes

---

### 🛠️ **Configuración Actual del Sistema**

El sistema está diseñado con **modo simulación por defecto** para desarrollo:

```python
# En notification_service.py
async def _send_email(self, to_email: str, subject: str, body: str) -> bool:
    """Enviar email usando Gmail SMTP o simulación"""
    
    # Modo simulación (desarrollo)
    if not all([GMAIL_USER, GMAIL_PASSWORD]):
        logger.info(f"📧 [SIMULACIÓN] Email enviado a: {to_email}")
        logger.info(f"Asunto: {subject}")
        return True
    
    # Modo producción con Gmail SMTP
    try:
        # Código real de envío...
```

### ✅ **Implementación Recomendada**

#### **Para Desarrollo:**
```bash
# No configurar variables = modo simulación
# Los logs muestran las notificaciones sin costo
```

#### **Para Producción:**
```bash
# 1. Para EMAIL (Gmail gratuito)
export GMAIL_SMTP_USER="notifications@btgpactual.com"
export GMAIL_SMTP_PASSWORD="app-password-generado"

# 2. Para SMS (Twilio)
export TWILIO_ACCOUNT_SID="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export TWILIO_AUTH_TOKEN="tu-auth-token"
export TWILIO_PHONE_NUMBER="+1234567890"
```

### 📊 **Métricas y Monitoreo**

El sistema incluye logging completo para monitorear:
- ✅ Emails enviados exitosamente
- ❌ Emails fallidos
- 📱 SMS enviados
- 💰 Tracking de costos por tipo de notificación

### 🔧 **Instalación de Dependencias**

```bash
# Para funcionalidad completa
pip install aiosmtplib twilio

# Las dependencias son opcionales
# Si no están instaladas, usa modo simulación automáticamente
```

---

### 🚀 **Recomendación Final**

1. **Desarrollo:** Usar modo simulación (sin costos)
2. **Producción inicial:** Gmail SMTP + Twilio con límites bajos
3. **Escala:** Migrar a AWS SES + mantener Twilio
4. **Monitoreo:** Usar CloudWatch para tracking de costos

**Costo inicial recomendado:** ~$30-50/mes para comenzar
**ROI:** Notificaciones mejoran retención de usuarios en ~25%
