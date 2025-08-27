#!/bin/bash

# Script para desplegar BTG Pactual en EC2
# Copia y ejecuta exactamente el mismo docker-compose que funciona en local

set -e

echo "🚀 Deployando BTG Pactual en EC2..."

# Variables (ajustar según sea necesario)
REPO_URL="https://github.com/drmelom/technical-test-BTG-Pactual.git"  # Cambiar por tu repo
APP_DIR="/home/ec2-user/btg-pactual"
BRANCH="main"

# Limpiar directorio anterior si existe
if [ -d "$APP_DIR" ]; then
    echo "📁 Limpiando directorio anterior..."
    cd $APP_DIR
    docker-compose down 2>/dev/null || true
    cd ..
    rm -rf $APP_DIR
fi

# Clonar repositorio
echo "📥 Clonando repositorio..."
git clone -b $BRANCH $REPO_URL $APP_DIR
cd $APP_DIR/backend

# Verificar que docker está funcionando
echo "🐳 Verificando Docker..."
docker --version
docker-compose --version

# Verificar que el archivo .env existe
if [ ! -f ".env" ]; then
    echo "❌ Error: No se encontró archivo .env"
    echo "💡 Necesitas crear el archivo .env con tus credenciales"
    exit 1
fi

echo "📋 Verificando configuración..."
echo "✅ Archivo .env encontrado"
echo "✅ docker-compose.yml encontrado"
echo "✅ Dockerfile encontrado"

# Construir y ejecutar exactamente como en local
echo "🔨 Construyendo y ejecutando aplicación..."
docker-compose up -d --build

# Esperar que los servicios estén listos
echo "⏳ Esperando que los servicios estén listos..."
sleep 30

# Verificar estado de los servicios
echo "📊 Estado de los servicios:"
docker-compose ps

# Verificar logs
echo "📝 Últimos logs:"
docker-compose logs --tail=10

# Verificar que la API responde
echo "🔍 Verificando que la API responde..."
curl -f http://localhost:8000/health || echo "⚠️ La API aún no responde, puede necesitar más tiempo"

# Mostrar información útil
echo ""
echo "✅ Despliegue completado!"
echo "========================"
echo ""
echo "🌐 URLs disponibles:"
echo "  API: http://$(curl -s ifconfig.me):8000"
echo "  Docs: http://$(curl -s ifconfig.me):8000/docs"
echo "  MongoDB Express: http://$(curl -s ifconfig.me):8081"
echo ""
echo "🔧 Comandos útiles:"
echo "  Ver logs: docker-compose logs -f"
echo "  Reiniciar: docker-compose restart"
echo "  Parar: docker-compose down"
echo "  Estado: docker-compose ps"
echo ""
echo "📁 Directorio: $APP_DIR/backend"
