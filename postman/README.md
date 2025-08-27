# BTG Pactual Funds API - Postman Collection

## 📋 Descripción

Colección completa de Postman para la API de gestión de fondos de BTG Pactual. Incluye todos los endpoints necesarios para testing y desarrollo con validaciones automatizadas y manejo de errores.

## 🚀 Funcionalidades

### ✅ **Endpoints Cubiertos**
- **Autenticación:** Registro y login de usuarios
- **Gestión de usuarios:** Perfil y balance
- **Fondos:** Listado, búsqueda por ID y categoría
- **Transacciones:** Suscripción, cancelación e historial
- **Health Check:** Monitoreo del estado de la API
- **Manejo de Errores:** Casos de prueba para validar excepciones

### ✅ **Pruebas Automatizadas**
- Validación de códigos de estado HTTP
- Verificación de estructura de respuestas
- Gestión automática de tokens JWT
- Validación de datos de usuario y balance
- Testing de casos de error y edge cases

### ✅ **Variables de Entorno**
- Gestión automática de tokens de acceso
- IDs de usuario y suscripción
- URL base configurable
- Datos de prueba reutilizables

## 📁 Archivos Incluidos

```
postman/
├── BTG_Pactual_Funds_API.postman_collection.json              # Colección principal
├── BTG_Pactual_Local_Environment.postman_environment.json     # Entorno local
├── BTG_Pactual_Production_Environment.postman_environment.json # Entorno AWS producción
└── README.md                                                   # Esta documentación
```

## 🔧 Configuración

### 1. Importar Colección ⚠️ **SÚPER SIMPLE**
1. Abrir Postman
2. Click en **Import**
3. **Seleccionar:** `BTG_Pactual_Funds_API.postman_collection.json`
4. ¡**Ya está listo!** - Todo configurado automáticamente ⭐

### ✅ **URLs de Producción YA CONFIGURADAS:**
- **API Base:** `http://18.205.222.251:8000` ✅
- **Documentación Swagger:** `http://18.205.222.251:8000/docs` ✅
- **Health Check:** `http://18.205.222.251:8000/health` ✅
- **Mongo Express:** `http://18.205.222.251:8081` (admin/admin) ✅

### 🎯 **No necesitas:**
- ❌ Importar environments adicionales
- ❌ Configurar variables manualmente  
- ❌ Seleccionar environments
- ❌ Cambiar URLs

**Las demás variables** (tokens, user_id) se asignan automáticamente durante la ejecución.

---

### 📝 **Para Desarrollo Local (Opcional):**
Si quieres usar entorno local, puedes importar también:
- `BTG_Pactual_Local_Environment.postman_environment.json`
- Y seleccionar el environment "Local" en Postman

### 3. Variables de Entorno Disponibles

| Variable | Descripción | Valor Local | Valor Producción |
|----------|-------------|-------------|------------------|
| `base_url` | URL base de la API | `http://localhost:8000` | `http://18.205.222.251:8000` |
| `access_token` | Token JWT (auto-asignado) | - | - |
| `user_id` | ID del usuario logueado | - | - |
| `subscription_id` | ID de suscripción activa | - | - |
| `docs_url` | Documentación Swagger | - | `http://18.205.222.251:8000/docs` |
| `health_url` | Health Check endpoint | - | `http://18.205.222.251:8000/health` |
| `mongo_express_url` | Interface MongoDB | - | `http://18.205.222.251:8081` |

## 📊 Estructura de la Colección

### 1. **Authentication**
- `Register Admin User` - Crear usuario administrador
- `Register Client User` - Crear usuario cliente  
- `Login Client` - Autenticación de cliente
- `Login Admin` - Autenticación de administrador

### 2. **Health Check**
- `Health Check` - Verificar estado de la API

### 3. **User Profile**
- `User Profile` - Obtener perfil del usuario autenticado

### 4. **Funds Management**
- `List All Funds` - Listar todos los fondos disponibles
- `Get Fund by ID` - Obtener fondo específico por ID
- `Get Funds by Category` - Filtrar fondos por categoría

### 5. **Transactions**
- `Subscribe to Fund - FPV_BTG_PACTUAL_RECAUDADORA` - Suscribirse al fondo FPV
- `Subscribe to Fund - FDO-ACCIONES` - Suscribirse al fondo de acciones
- `Subscribe to Fund - FPV_BTG_PACTUAL_ECOPETROL` - Suscribirse al fondo Ecopetrol
- `Subscribe to Fund - DEUDA_PRIVADA` - Suscribirse al fondo de deuda privada
- `Cancel Fund Subscription` - Cancelar suscripción activa
- `Get Transaction History` - Obtener historial completo
- `Get Transaction History by Fund` - Filtrar historial por fondo

### 6. **Error Handling Tests** ⚠️
- `Login with Invalid Credentials` - Probar credenciales incorrectas
- `Access Protected Route Without Token` - Acceso sin autenticación
- `Subscribe with Insufficient Funds` - Prueba de fondos insuficientes
- `Get Non-Existent Fund` - Recurso no encontrado

## 🔍 Pruebas Automatizadas

### Validaciones Incluidas
- ✅ **Status Codes:** Verificación de códigos HTTP correctos
- ✅ **Response Structure:** Validación de esquemas de respuesta
- ✅ **Authentication:** Gestión automática de tokens
- ✅ **Business Logic:** Validación de reglas de negocio
- ✅ **Error Handling:** Testing de casos de error
- ✅ **Data Persistence:** Verificación de datos guardados

### Ejemplos de Tests

```javascript
// Validación de login exitoso
pm.test('Login successful with valid credentials', function () {
    pm.response.to.have.status(200);
    const response = pm.response.json();
    pm.expect(response).to.have.property('access_token');
    pm.expect(response).to.have.property('user');
});

// Validación de suscripción
pm.test('Subscription creates transaction', function () {
    const response = pm.response.json();
    pm.expect(response).to.have.property('subscription_id');
    pm.expect(response).to.have.property('message');
    pm.environment.set('subscription_id', response.subscription_id);
});
```

## 🎯 Casos de Uso

### Desarrollo
1. **Testing Rápido:** Ejecutar endpoints individuales
2. **Debugging:** Verificar respuestas y payloads
3. **Validación:** Confirmar funcionalidad de nuevas features

### QA/Testing
1. **Regression Testing:** Ejecutar colección completa
2. **Load Testing:** Usar Postman Runner
3. **Integration Testing:** Validar flujos end-to-end

### Demostración
1. **Cliente Demo:** Mostrar funcionalidades completas
2. **Training:** Enseñar uso de la API
3. **Documentation:** Ejemplos en vivo

## 🚦 Flujo de Ejecución Recomendado

### Secuencia Óptima:
1. **Health Check** - Verificar API activa
2. **Register Client User** - Crear usuario de prueba
3. **Login Client** - Autenticarse y obtener token
4. **List All Funds** - Ver fondos disponibles
5. **Subscribe to Fund** - Hacer suscripción
6. **Get Transaction History** - Verificar transacción
7. **Cancel Fund Subscription** - Cancelar suscripción
8. **Error Handling Tests** - Validar manejo de errores

### Ejecutar Colección Completa:

**Para entorno local:**
1. Click en la colección "BTG Pactual - Funds Management API"
2. Click en "Run collection"
3. Seleccionar entorno "BTG Pactual - Local Environment"
4. Click en "Run BTG Pactual - Funds Management API"

**Para entorno de producción (AWS):**
1. Click en la colección "BTG Pactual - Funds Management API"
2. Click en "Run collection"
3. Seleccionar entorno "BTG Pactual - Production Environment (AWS)"
4. Click en "Run BTG Pactual - Funds Management API"
5. ✅ **¡La aplicación está desplegada y funcionando en AWS EC2!**

## 📈 Métricas de Success

Al ejecutar la colección completa deberías obtener:

- ✅ **~15-20 tests passed**
- ✅ **0 tests failed**
- ✅ **Response times < 500ms**
- ✅ **All endpoints returning expected status codes**

## 🔧 Troubleshooting

### Error: "Could not get any response"
- ✓ Verificar que la API esté corriendo (`docker-compose up`)
- ✓ Confirmar URL en `base_url` variable

### Error: "401 Unauthorized"
- ✓ Ejecutar login antes de endpoints protegidos
- ✓ Verificar que `access_token` esté configurado

### Error: "Connection refused"
- ✓ Verificar puerto 8000 disponible
- ✓ Confirmar contenedores Docker activos

### Tests Falling
- ✓ Ejecutar endpoints en orden secuencial
- ✓ Verificar datos de prueba en variables

## 📞 Soporte

Para problemas o sugerencias:
- Revisar logs de la API en Docker
- Verificar variables de entorno
- Consultar documentación de la API en `/docs`

---

**Versión:** 1.2 Enhanced  
**Última actualización:** 2024  
**Autor:** BTG Pactual - Technical Test Team
