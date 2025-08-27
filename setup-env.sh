#!/bin/bash

# Script para configurar variables de entorno en EC2
# Ejecutar DESPUÉS de clonar el repo y ANTES del deploy

APP_DIR="/home/ec2-user/btg-pactual/backend"

echo "🔐 Configurando variables de entorno..."

# Crear archivo .env con las mismas variables que funcionan en local
cat > $APP_DIR/.env << 'EOF'
# Environment Configuration
ENVIRONMENT=production
DEBUG=False
API_V1_STR="/api/v1"
PROJECT_NAME="BTG Pactual Funds Management"
VERSION="1.0.0"

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=10080
ALGORITHM=HS256

# Database
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=btg_pactual

# AWS Configuration (for deployment)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=

# Email Configuration - Gmail SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=TU_GMAIL_AQUI@gmail.com
SMTP_PASSWORD=TU_APP_PASSWORD_AQUI
EMAIL_FROM=TU_GMAIL_AQUI@gmail.com

# Gmail SMTP Configuration (Free Tier) - UNIFICADO
GMAIL_SMTP_USER=TU_GMAIL_AQUI@gmail.com
GMAIL_SMTP_PASSWORD=TU_APP_PASSWORD_AQUI

# SMS Configuration (Twilio Free Tier)
TWILIO_ACCOUNT_SID=TU_TWILIO_SID_AQUI
TWILIO_AUTH_TOKEN=TU_TWILIO_TOKEN_AQUI
TWILIO_PHONE_NUMBER=TU_NUMERO_TWILIO_AQUI

# Números de prueba
TEST_PHONE_NUMBER=+573125094344

# Client Configuration
INITIAL_CLIENT_BALANCE=500000

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# CORS - permitir acceso desde cualquier origen (ajustar en producción)
BACKEND_CORS_ORIGINS=["*"]
EOF

echo "⚠️ IMPORTANTE: Debes editar el archivo .env con tus credenciales reales:"
echo "   nano $APP_DIR/.env"
echo ""
echo "🔑 Variables que debes configurar:"
echo "   - GMAIL_SMTP_USER (tu email de Gmail)"
echo "   - GMAIL_SMTP_PASSWORD (app password de Gmail)"
echo "   - TWILIO_ACCOUNT_SID (tu SID de Twilio)"
echo "   - TWILIO_AUTH_TOKEN (tu token de Twilio)"
echo "   - TWILIO_PHONE_NUMBER (tu número de Twilio)"
echo "   - SECRET_KEY (generar una clave segura nueva)"
echo ""
echo "✅ Archivo .env creado en: $APP_DIR/.env"
