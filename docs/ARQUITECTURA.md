# Arquitectura de la Solución - BTG Pactual Funds Management

## Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           FRONTEND/CLIENT                              │
│                        (Postman/Mobile/Web)                           │
└─────────────────────────┬───────────────────────────────────────────────┘
                         │ HTTPS/REST API
                         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        APPLICATION LAYER                               │
│ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────────────────┐ │
│ │   API Gateway   │ │  Load Balancer  │ │     Security Layer          │ │
│ │   (AWS ALB)     │ │   (AWS ALB)     │ │ (JWT Auth + Rate Limiting)  │ │
│ └─────────────────┘ └─────────────────┘ └─────────────────────────────┘ │
└─────────────────────────┬───────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      BACKEND SERVICES                                  │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │                    FastAPI Application                             │ │
│ │ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐ │ │
│ │ │ Auth        │ │ Funds       │ │Transaction  │ │ Notification    │ │ │
│ │ │ Controller  │ │ Controller  │ │ Controller  │ │ Service         │ │ │
│ │ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────────┘ │ │
│ │ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐ │ │
│ │ │ User        │ │ Fund        │ │ Transaction │ │ Subscription    │ │ │
│ │ │ Service     │ │ Service     │ │ Service     │ │ Service         │ │ │
│ │ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────────┘ │ │
│ │ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                   │ │
│ │ │ User        │ │ Fund        │ │ Transaction │                   │ │
│ │ │ Repository  │ │ Repository  │ │ Repository  │                   │ │
│ │ └─────────────┘ └─────────────┘ └─────────────┘                   │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────┬───────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        DATA LAYER                                      │
│ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────────────────┐ │
│ │   MongoDB       │ │   MongoDB       │ │        External APIs        │ │
│ │   Primary       │ │   Replica Set   │ │  ┌─────────┐ ┌─────────────┐│ │
│ │                 │ │                 │ │  │ Twilio  │ │   SMTP      ││ │
│ │ - Users         │ │ (Read Replicas) │ │  │  SMS    │ │   Email     ││ │
│ │ - Funds         │ │                 │ │  └─────────┘ └─────────────┘│ │
│ │ - Transactions  │ │                 │ │                             │ │
│ │ - Subscriptions │ │                 │ │                             │ │
│ └─────────────────┘ └─────────────────┘ └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                     INFRASTRUCTURE LAYER                               │
│ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────────────────┐ │
│ │      VPC        │ │   Monitoring    │ │        Security             │ │
│ │                 │ │                 │ │                             │ │
│ │ ┌─────────────┐ │ │ ┌─────────────┐ │ │ ┌─────────┐ ┌─────────────┐ │ │
│ │ │Public Subnet│ │ │ │ CloudWatch  │ │ │ │   WAF   │ │    KMS      │ │ │
│ │ │   (ALB)     │ │ │ │             │ │ │ │         │ │ Encryption  │ │ │
│ │ └─────────────┘ │ │ └─────────────┘ │ │ └─────────┘ └─────────────┘ │ │
│ │ ┌─────────────┐ │ │ ┌─────────────┐ │ │ ┌─────────┐ ┌─────────────┐ │ │
│ │ │Private Sub. │ │ │ │   X-Ray     │ │ │ │ Secrets │ │   IAM       │ │ │
│ │ │  (EC2/ECS)  │ │ │ │   Tracing   │ │ │ │ Manager │ │   Roles     │ │ │
│ │ └─────────────┘ │ │ └─────────────┘ │ │ └─────────┘ └─────────────┘ │ │
│ │ ┌─────────────┐ │ │                 │ │                             │ │
│ │ │Private Sub. │ │ │                 │ │                             │ │
│ │ │ (DocumentDB)│ │ │                 │ │                             │ │
│ │ └─────────────┘ │ │                 │ │                             │ │
│ └─────────────────┘ └─────────────────┘ └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

## Justificación de la Arquitectura

### 1. **Patrón de Arquitectura: Clean Architecture + Microservices Ready**

#### **¿Por qué Clean Architecture?**
- **Separación de responsabilidades**: Cada capa tiene una responsabilidad específica
- **Independencia de frameworks**: El core business logic no depende de FastAPI o MongoDB
- **Testabilidad**: Cada componente se puede probar de forma aislada
- **Mantenibilidad**: Facilita cambios y evolución del sistema
- **Escalabilidad**: Preparada para evolucionar a microservicios

#### **Capas implementadas:**

1. **Controllers/API Layer**: Manejo de HTTP requests, validación de entrada, serialización
2. **Service Layer**: Lógica de negocio, orquestación de operaciones
3. **Repository Layer**: Acceso a datos, abstracción de la base de datos
4. **Domain Layer**: Modelos de dominio, entidades de negocio

### 2. **Base de Datos: MongoDB (NoSQL)**

#### **¿Por qué MongoDB?**
- **Esquema flexible**: Permite evolución de los modelos sin migraciones complejas
- **Escalabilidad horizontal**: Fácil sharding para crecimiento futuro
- **Performance**: Excelente rendimiento para lecturas y escrituras
- **JSON nativo**: Se integra naturalmente con Python y FastAPI
- **Agregaciones**: Permite consultas complejas para reportes y analytics

#### **Modelo de datos optimizado:**
```javascript
// Users Collection
{
  "_id": ObjectId,
  "email": "string",
  "full_name": "string", 
  "role": "client|admin",
  "balance": NumberDecimal,
  "notification_preference": "email|sms",
  "created_at": ISODate
}

// Funds Collection  
{
  "_id": "1", // Business ID for easy reference
  "name": "string",
  "minimum_amount": NumberDecimal,
  "category": "FPV|FIC",
  "is_active": Boolean
}

// Transactions Collection
{
  "_id": ObjectId,
  "transaction_id": "UUID4", // Business ID
  "user_id": ObjectId,
  "fund_id": "string",
  "type": "subscription|cancellation",
  "amount": NumberDecimal,
  "status": "completed|failed",
  "created_at": ISODate
}

// Subscriptions Collection
{
  "_id": ObjectId,
  "subscription_id": "UUID4",
  "user_id": ObjectId,
  "fund_id": "string", 
  "amount": NumberDecimal,
  "status": "active|cancelled",
  "subscribed_at": ISODate,
  "cancelled_at": ISODate
}
```

### 3. **Tecnologías Seleccionadas**

#### **Backend: FastAPI**
- **Performance**: Uno de los frameworks más rápidos de Python
- **Async**: Soporte nativo para operaciones asíncronas
- **Documentación automática**: Swagger/OpenAPI integrado
- **Validación**: Pydantic para validación de tipos automática
- **Productividad**: Desarrollo rápido con excelente developer experience

#### **ODM: Beanie (sobre Motor/PyMongo)**
- **Async**: Compatible con FastAPI async/await
- **Type Safety**: Validación de tipos con Pydantic
- **Performance**: Motor es el driver async oficial de MongoDB
- **Simplicidad**: API similar a Django ORM pero para MongoDB

#### **Autenticación: JWT + bcrypt**
- **Stateless**: No requiere almacenamiento de sesiones
- **Escalable**: Funciona bien en arquitecturas distribuidas
- **Seguro**: bcrypt para hashing de contraseñas
- **Standard**: JWT es un estándar de la industria

### 4. **Infraestructura: AWS con Terraform**

#### **¿Por qué AWS?**
- **Madurez**: Servicios probados y estables
- **Ecosistema**: Gran variedad de servicios integrados
- **Seguridad**: Compliance y certificaciones de seguridad
- **Escalabilidad**: Auto-scaling y managed services
- **Cost optimization**: Diversos modelos de pricing

#### **¿Por qué Terraform?**
- **Infrastructure as Code**: Versionado y reproducible
- **Multi-cloud**: No está atado a un proveedor específico
- **Plan/Apply**: Preview de cambios antes de aplicar
- **State management**: Control de estado centralizado
- **Modularidad**: Reutilización de componentes

#### **Servicios AWS utilizados:**

1. **Compute**: EC2 con Auto Scaling Groups
2. **Load Balancing**: Application Load Balancer
3. **Database**: DocumentDB (MongoDB compatible)
4. **Networking**: VPC, Subnets, Security Groups
5. **Monitoring**: CloudWatch, X-Ray
6. **Security**: IAM, KMS, Secrets Manager

### 5. **Patrones de Diseño Implementados**

#### **Repository Pattern**
- Abstrae el acceso a datos
- Facilita testing con mocks
- Permite cambiar de base de datos sin afectar la lógica de negocio

#### **Service Layer Pattern**
- Encapsula la lógica de negocio
- Coordina operaciones entre múltiples repositories
- Maneja transacciones y reglas de negocio complejas

#### **Dependency Injection**
- FastAPI Depends() para inyección automática
- Facilita testing y desacoplamiento
- Mejora la mantenibilidad del código

#### **Factory Pattern**
- Para creación de objetos complejos (usuarios, transacciones)
- Centraliza la lógica de creación
- Facilita cambios en la construcción de objetos

### 6. **Seguridad Implementada**

#### **Autenticación y Autorización**
- JWT tokens con expiración configurable
- Roles-based access control (RBAC)
- Middleware de autenticación en todas las rutas protegidas

#### **Validación de Datos**
- Pydantic schemas para validación automática
- Sanitización de inputs
- Validación de tipos y rangos

#### **Seguridad de API**
- CORS configurado correctamente
- Rate limiting (preparado para implementar)
- Headers de seguridad (X-Frame-Options, etc.)

#### **Seguridad de Datos**
- Passwords hasheados con bcrypt y salt
- Variables sensibles en variables de entorno
- Conexiones seguras a la base de datos

### 7. **Observabilidad y Monitoreo**

#### **Logging Estructurado**
- JSON logger para facilitar parsing
- Correlation IDs para tracking de requests
- Diferentes niveles de log (DEBUG, INFO, WARNING, ERROR)

#### **Health Checks**
- Endpoint `/health` para verificar estado del servicio
- Checks de conectividad a base de datos
- Métricas de performance incluidas

#### **Error Handling**
- Manejo centralizado de excepciones
- Responses consistentes para errores
- Logging de errores para debugging

### 8. **Escalabilidad y Performance**

#### **Async Programming**
- FastAPI async/await para operaciones I/O
- Motor driver async para MongoDB
- Concurrent request handling

#### **Database Optimization**
- Índices apropiados en MongoDB
- Query optimization
- Connection pooling

#### **Caching Strategy** (preparado)
- Redis para caching de consultas frecuentes
- Cache invalidation strategies
- Session storage distribuido

### 9. **Testing Strategy**

#### **Niveles de Testing**
- Unit tests para servicios y repositories
- Integration tests para APIs
- E2E tests con pytest-asyncio
- Performance tests para endpoints críticos

#### **Testing Tools**
- pytest para framework de testing
- httpx para testing de APIs async
- Faker para generación de datos de prueba
- Coverage reporting

### 10. **DevOps y CI/CD**

#### **Containerización**
- Docker para empaquetado de aplicación
- Multi-stage builds para optimización
- Docker Compose para desarrollo local
- Health checks en containers

#### **Infrastructure as Code**
- Terraform para infrastructure provisioning
- Módulos reutilizables
- Environment separation (dev/staging/prod)
- State management con backend remoto

### 11. **Consideraciones Futuras**

#### **Microservices Evolution**
- Arquitectura preparada para split en microservicios
- Service boundaries bien definidos
- API contracts establecidos

#### **Event-Driven Architecture**
- Preparado para implementar event sourcing
- Message queues para comunicación asíncrona
- CQRS para separación de lecturas y escrituras

#### **Advanced Features**
- Real-time notifications con WebSockets
- Advanced analytics y reporting
- Multi-tenancy support
- API versioning strategy

## Beneficios de esta Arquitectura

1. **Mantenibilidad**: Código organizado y fácil de mantener
2. **Escalabilidad**: Preparado para crecer horizontal y verticalmente  
3. **Testabilidad**: Componentes desacoplados fáciles de testear
4. **Seguridad**: Multiple layers de seguridad implementadas
5. **Performance**: Async programming y database optimization
6. **Observabilidad**: Logging y monitoring comprehensive
7. **Flexibilidad**: Fácil adaptación a nuevos requerimientos
8. **Productividad**: Desarrollo rápido con buenas prácticas

Esta arquitectura proporciona una base sólida para el sistema de gestión de fondos de BTG Pactual, balanceando las necesidades actuales con la capacidad de evolución futura.
