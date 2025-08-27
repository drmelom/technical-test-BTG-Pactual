#!/bin/bash

# Script de instalación para EC2 Free Tier
# Instala Docker y prepara el entorno para BTG Pactual Funds

set -e

echo "🚀 Iniciando configuración de BTG Pactual Funds - Free Tier"

# Actualizar sistema
echo "📦 Actualizando paquetes del sistema..."
sudo yum update -y

# Instalar Docker
echo "🐳 Instalando Docker..."
sudo yum install -y docker git

# Iniciar Docker
echo "▶️ Iniciando servicios Docker..."
sudo systemctl start docker
sudo systemctl enable docker

# Agregar usuario ec2-user al grupo docker
echo "👤 Configurando permisos de usuario..."
sudo usermod -a -G docker ec2-user

# Instalar Docker Compose
echo "🔧 Instalando Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Crear directorio para la aplicación
echo "📁 Creando directorios de aplicación..."
sudo mkdir -p /opt/btg-pactual
sudo chown -R ec2-user:ec2-user /opt/btg-pactual

# Crear directorio para MongoDB
echo "🗄️ Preparando MongoDB..."
sudo mkdir -p /opt/mongodb/data
sudo chown -R ec2-user:ec2-user /opt/mongodb

# Configurar firewall para el puerto de la aplicación
echo "🔥 Configurando firewall..."
sudo iptables -I INPUT -p tcp --dport ${app_port} -j ACCEPT
sudo iptables -I INPUT -p tcp --dport 27017 -j ACCEPT

# Crear archivo docker-compose para la aplicación
echo "📝 Creando configuración Docker Compose..."
cat > /opt/btg-pactual/docker-compose.yml << 'EOF'
version: '3.8'

services:
  mongodb:
    image: mongo:7-jammy
    container_name: btg_mongodb
    restart: unless-stopped
    ports:
      - "27017:27017"
    volumes:
      - /opt/mongodb/data:/data/db
    environment:
      MONGO_INITDB_ROOT_USERNAME: btgadmin
      MONGO_INITDB_ROOT_PASSWORD: BtgP@ssw0rd123
      MONGO_INITDB_DATABASE: btg_funds_db
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 30s
      timeout: 10s
      retries: 5
    networks:
      - btg_network

  mongo-express:
    image: mongo-express:latest
    container_name: btg_mongo_express
    restart: unless-stopped
    ports:
      - "8081:8081"
    environment:
      ME_CONFIG_MONGODB_ADMINUSERNAME: btgadmin
      ME_CONFIG_MONGODB_ADMINPASSWORD: BtgP@ssw0rd123
      ME_CONFIG_MONGODB_URL: mongodb://btgadmin:BtgP@ssw0rd123@mongodb:27017/
      ME_CONFIG_BASICAUTH_USERNAME: admin
      ME_CONFIG_BASICAUTH_PASSWORD: btgpactual123
    depends_on:
      - mongodb
    networks:
      - btg_network

  # Placeholder para la aplicación BTG Pactual
  # La aplicación se deployará desde CI/CD o manualmente
  
networks:
  btg_network:
    driver: bridge

volumes:
  mongodb_data:
    driver: local
EOF

# Iniciar servicios base
echo "🎬 Iniciando servicios base..."
cd /opt/btg-pactual
docker-compose up -d mongodb mongo-express

# Esperar a que MongoDB esté listo
echo "⏳ Esperando a que MongoDB esté listo..."
sleep 30

# Crear usuario de aplicación en MongoDB
echo "👤 Creando usuario de aplicación..."
docker exec btg_mongodb mongosh -u btgadmin -p BtgP@ssw0rd123 --eval "
use btg_funds_db;
db.createUser({
  user: 'btguser',
  pwd: 'BtgUser123!',
  roles: [
    { role: 'readWrite', db: 'btg_funds_db' }
  ]
});
"

# Crear scripts útiles
echo "📝 Creando scripts de utilidad..."

# Script para ver logs
cat > /opt/btg-pactual/view-logs.sh << 'EOF'
#!/bin/bash
echo "📊 BTG Pactual - Logs de servicios"
echo "=================================="
docker-compose logs -f --tail=100
EOF
chmod +x /opt/btg-pactual/view-logs.sh

# Script para restart
cat > /opt/btg-pactual/restart-services.sh << 'EOF'
#!/bin/bash
echo "🔄 BTG Pactual - Reiniciando servicios"
echo "======================================"
docker-compose down
docker-compose up -d
echo "✅ Servicios reiniciados"
EOF
chmod +x /opt/btg-pactual/restart-services.sh

# Script de status
cat > /opt/btg-pactual/status.sh << 'EOF'
#!/bin/bash
echo "📈 BTG Pactual - Estado de servicios"
echo "===================================="
docker-compose ps
echo ""
echo "🗄️ Estado de MongoDB:"
docker exec btg_mongodb mongosh -u btgadmin -p BtgP@ssw0rd123 --eval "db.adminCommand('ping')" --quiet
echo ""
echo "🌐 URLs disponibles:"
echo "- Mongo Express: http://$(curl -s ifconfig.me):8081 (admin:btgpactual123)"
echo "- API (cuando esté deployada): http://$(curl -s ifconfig.me):${app_port}"
EOF
chmod +x /opt/btg-pactual/status.sh

# Información final
echo ""
echo "✅ BTG Pactual Funds - Configuración completada!"
echo "================================================"
echo ""
echo "📋 Servicios instalados:"
echo "  ✅ Docker y Docker Compose"
echo "  ✅ MongoDB (puerto 27017)"
echo "  ✅ Mongo Express (puerto 8081)"
echo ""
echo "🔗 Para acceder:"
echo "  - Mongo Express: http://$(curl -s ifconfig.me):8081"
echo "    Usuario: admin / Contraseña: btgpactual123"
echo ""
echo "📁 Directorio de trabajo: /opt/btg-pactual"
echo "🛠️ Scripts disponibles:"
echo "  - ./status.sh - Ver estado de servicios"
echo "  - ./view-logs.sh - Ver logs"
echo "  - ./restart-services.sh - Reiniciar servicios"
echo ""
echo "🔄 Para deployar la aplicación BTG Pactual:"
echo "  cd /opt/btg-pactual"
echo "  git clone <your-repo>"
echo "  docker-compose up -d"
echo ""
echo "💰 Configuración optimizada para AWS Free Tier"
echo "🎉 ¡Sistema listo para producción!"

# Ejecutar status final
/opt/btg-pactual/status.sh
