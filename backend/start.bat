@echo off
echo ========================================
echo   BTG Pactual - Funds Management API
echo ========================================
echo.

REM Check if Docker is running
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Docker no está instalado o no está ejecutándose
    echo Por favor instala Docker Desktop desde: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM Check if .env exists
if not exist .env (
    echo 📄 Creando archivo .env desde .env.example...
    copy .env.example .env
    echo.
    echo ⚠️  IMPORTANTE: Edita el archivo .env con tus configuraciones antes de continuar
    echo    - Cambia SECRET_KEY por una clave segura
    echo    - Configura credenciales de email y SMS si las tienes
    echo.
    set /p answer=¿Quieres continuar con la configuración por defecto? (y/n): 
    if /i not "%answer%"=="y" (
        echo 📝 Edita el archivo .env y ejecuta este script nuevamente
        pause
        exit /b 0
    )
)

echo 🚀 Iniciando servicios de BTG Pactual...
echo.

REM Stop any existing containers
echo 🛑 Deteniendo contenedores existentes...
docker-compose down

REM Build and start services
echo 🔨 Construyendo y iniciando servicios...
docker-compose up -d --build

if %errorlevel% neq 0 (
    echo ❌ Error iniciando los servicios
    pause
    exit /b 1
)

echo.
echo ⏳ Esperando que los servicios estén listos...
timeout /t 10 /nobreak >nul

REM Check if services are healthy
echo 🔍 Verificando estado de los servicios...

REM Check Backend
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Backend no está respondiendo en el puerto 8000
) else (
    echo ✅ Backend: http://localhost:8000
)

REM Check MongoDB
docker-compose ps | find "btg_mongodb" | find "Up" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ MongoDB no está ejecutándose
) else (
    echo ✅ MongoDB: localhost:27017
)

REM Check Mongo Express
curl -s http://localhost:8081 >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Mongo Express no está respondiendo en el puerto 8081
) else (
    echo ✅ Mongo Express: http://localhost:8081
)

echo.
echo ========================================
echo 🎉 ¡BTG Pactual API está ejecutándose!
echo ========================================
echo.
echo 📚 Documentación API: http://localhost:8000/docs
echo 🔄 API ReDoc:          http://localhost:8000/redoc
echo 🏥 Health Check:       http://localhost:8000/health
echo 📊 MongoDB Admin:      http://localhost:8081 (admin/admin)
echo.
echo 👤 Usuario Admin por defecto:
echo    Email: admin@btgpactual.com
echo    Password: Admin123!
echo.
echo 💡 Comandos útiles:
echo    Ver logs:           docker-compose logs -f backend
echo    Reiniciar:          docker-compose restart backend
echo    Detener todo:       docker-compose down
echo    Reconstruir:        docker-compose up -d --build
echo.
echo 📋 Para probar la API puedes usar:
echo    - Swagger UI en http://localhost:8000/docs
echo    - Postman o cualquier cliente HTTP
echo    - curl desde la terminal
echo.

set /p answer=¿Abrir documentación en el navegador? (y/n): 
if /i "%answer%"=="y" (
    start http://localhost:8000/docs
)

echo.
echo Presiona cualquier tecla para salir...
pause >nul
