#!/bin/bash

# Script completo para configurar BTG Pactual en EC2
# Se ejecuta automáticamente durante el boot de la instancia
# Usa directamente el contenido del archivo .env local

set -e

# Variables pasadas desde Terraform
REPO_URL="${repo_url}"
ENV_CONTENT="${env_content}"

APP_DIR="/home/ec2-user/btg-pactual"
LOG_FILE="/var/log/btg-deployment.log"

# Función para logging
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a $LOG_FILE
}

log "🚀 Iniciando despliegue automático de BTG Pactual..."

# 1. Actualizar sistema e instalar dependencias
log "📦 Actualizando sistema..."
yum update -y >> $LOG_FILE 2>&1
yum install -y docker git curl >> $LOG_FILE 2>&1

# 2. Instalar Docker Compose
log "🐳 Instalando Docker Compose..."
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# 3. Configurar Docker
log "🔧 Configurando Docker..."
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user

# 4. Crear directorios
log "📁 Creando directorios..."
mkdir -p $APP_DIR
chown ec2-user:ec2-user $APP_DIR

# 5. Clonar repositorio
log "📥 Clonando repositorio..."
cd /home/ec2-user
git clone $REPO_URL btg-pactual >> $LOG_FILE 2>&1
chown -R ec2-user:ec2-user $APP_DIR

# 6. Configurar variables de entorno directamente del .env local
log "🔐 Copiando archivo .env desde local..."
cd $APP_DIR/backend

# Escribir el contenido del .env directamente (viene desde local)
cat > .env << 'EOF'
${ENV_CONTENT}
EOF

# Solo cambiar ENVIRONMENT a production para el deploy
sed -i 's/ENVIRONMENT=development/ENVIRONMENT=production/' .env
sed -i 's/DEBUG=True/DEBUG=False/' .env

# Generar una nueva SECRET_KEY más segura para producción
NEW_SECRET_KEY=$(openssl rand -hex 32)
sed -i "s/SECRET_KEY=.*/SECRET_KEY=$NEW_SECRET_KEY/" .env

chown ec2-user:ec2-user .env

log "✅ Archivo .env configurado con variables de local"

# 7. Construir y ejecutar aplicación
log "🏗️ Construyendo y ejecutando aplicación..."

# Cambiar al usuario ec2-user para ejecutar docker
sudo -u ec2-user bash << 'EOSU'
cd /home/ec2-user/btg-pactual/backend

# Construir y ejecutar
docker-compose up -d --build

# Esperar que los servicios estén listos
sleep 60

# Verificar estado
docker-compose ps
EOSU

# 8. Crear scripts de utilidad
log "🛠️ Creando scripts de utilidad..."

# Script para ver logs
cat > $APP_DIR/view-logs.sh << 'EOF'
#!/bin/bash
echo "📊 BTG Pactual - Logs de servicios"
echo "=================================="
cd /home/ec2-user/btg-pactual/backend
docker-compose logs -f --tail=100
EOF
chmod +x $APP_DIR/view-logs.sh

# Script para reiniciar
cat > $APP_DIR/restart.sh << 'EOF'
#!/bin/bash
echo "🔄 Reiniciando BTG Pactual..."
cd /home/ec2-user/btg-pactual/backend
docker-compose restart
echo "✅ Servicios reiniciados"
EOF
chmod +x $APP_DIR/restart.sh

# Script de estado
cat > $APP_DIR/status.sh << 'EOF'
#!/bin/bash
echo "📈 BTG Pactual - Estado de servicios"
echo "===================================="
cd /home/ec2-user/btg-pactual/backend
docker-compose ps
echo ""
echo "🌐 URLs disponibles:"
echo "  API: http://$(curl -s ifconfig.me):8000"
echo "  Docs: http://$(curl -s ifconfig.me):8000/docs"
echo "  Health: http://$(curl -s ifconfig.me):8000/health"
echo "  Mongo Express: http://$(curl -s ifconfig.me):8081"
EOF
chmod +x $APP_DIR/status.sh

chown -R ec2-user:ec2-user $APP_DIR

# 9. Verificación final
log "🔍 Verificación final..."
sleep 30

# Intentar verificar que la API responde
if curl -f http://localhost:8000/health >> $LOG_FILE 2>&1; then
    log "✅ API respondiendo correctamente"
else
    log "⚠️ API aún no responde, puede necesitar más tiempo"
fi

# 10. Información final
log "✅ Despliegue completado!"
log "========================"
log "API: http://$(curl -s ifconfig.me):8000"
log "Docs: http://$(curl -s ifconfig.me):8000/docs"
log "Mongo Express: http://$(curl -s ifconfig.me):8081"
log "Directorio: $APP_DIR"

log "🎉 BTG Pactual desplegado exitosamente con variables del .env local!"
