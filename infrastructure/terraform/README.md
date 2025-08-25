# 🚀 BTG Pactual - Infraestructura AWS con Terraform

Esta carpeta contiene la configuración de Terraform para desplegar la infraestructura completa del sistema de gestión de fondos de BTG Pactual en AWS.

## 🏗️ Arquitectura de la Infraestructura

```
┌─────────────────────────────────────────────────────────────────┐
│                          Internet                                │
└─────────────────────────┬───────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────────┐
│                 Application Load Balancer                       │
│                    (Public Subnets)                            │
└─────────────────────────┬───────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────────┐
│              Auto Scaling Group (EC2)                          │
│                  FastAPI Backend                               │
│                  (Private Subnets)                             │
└─────────────────────────┬───────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────────┐
│                 DocumentDB Cluster                             │
│                 (MongoDB Compatible)                           │
│                  (Private Subnets)                             │
└─────────────────────────────────────────────────────────────────┘
```

## 📦 Componentes de la Infraestructura

### 🌐 Red (network.tf)
- **VPC**: Red privada virtual con DNS habilitado
- **Subnets**: Públicas (ALB) y privadas (EC2, DB)
- **Internet Gateway**: Acceso a internet desde subnets públicas
- **NAT Gateways**: Acceso a internet desde subnets privadas
- **Route Tables**: Enrutamiento de tráfico

### 🔒 Seguridad (security.tf)
- **ALB Security Group**: Permite HTTP/HTTPS desde internet
- **EC2 Security Group**: Permite tráfico desde ALB y SSH interno
- **DocumentDB Security Group**: Permite MongoDB desde EC2
- **VPC Endpoint Security Group**: Para servicios AWS internos

### 💻 Compute (compute.tf)
- **Launch Template**: Configuración base para EC2 instances
- **Auto Scaling Group**: Escalado automático de instancias
- **Application Load Balancer**: Distribución de carga
- **Target Group**: Grupo objetivo para health checks
- **IAM Roles**: Permisos para EC2 instances

### 🗄️ Base de Datos (database.tf)
- **DocumentDB Cluster**: MongoDB compatible, cifrado
- **DocumentDB Instances**: Instancias del cluster
- **Subnet Group**: Grupo de subnets para la DB
- **Parameter Group**: Configuración de parámetros
- **Secrets Manager**: Credenciales de la base de datos

### 📧 Mensajería (messaging.tf)
- **SES Configuration**: Servicio de email
- **SNS Topics**: Notificaciones push y alertas
- **Email Templates**: Templates HTML/texto para emails
- **Event Destinations**: Logs de eventos de email

### 📊 Monitoreo (monitoring.tf)
- **CloudWatch Dashboard**: Dashboards de métricas
- **CloudWatch Alarms**: Alertas automáticas
- **Log Groups**: Agregación de logs
- **Query Definitions**: Consultas predefinidas

## 🚀 Despliegue

### Prerrequisitos

1. **AWS CLI configurado**:
```bash
aws configure
# Introducir Access Key ID, Secret Access Key, región
```

2. **Terraform instalado** (versión >= 1.0):
```bash
# Windows (con Chocolatey)
choco install terraform

# macOS (con Homebrew)
brew install terraform

# Linux
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/
```

3. **SSH Key Pair** (para acceso EC2):
```bash
mkdir -p keys
ssh-keygen -t rsa -b 4096 -f keys/id_rsa
```

### 📋 Configuración

1. **Copiar variables de ejemplo**:
```bash
cp terraform.tfvars.example terraform.tfvars
```

2. **Editar terraform.tfvars**:
```hcl
# Configuraciones básicas
environment = "dev"
project_name = "btg-pactual-funds-dev"
aws_region = "us-east-1"

# Configuración de base de datos
docdb_master_password = "TuPasswordSeguro123!"  # Cambiar por una segura

# Email para notificaciones
notification_email = "tu-email@example.com"
```

### 🚀 Comandos de Despliegue

```bash
# 1. Inicializar Terraform
terraform init

# 2. Validar configuración
terraform validate

# 3. Ver plan de ejecución
terraform plan

# 4. Aplicar cambios (crear infraestructura)
terraform apply

# 5. Ver outputs (URLs, endpoints, etc.)
terraform output
```

### 🔄 Comandos de Mantenimiento

```bash
# Ver estado actual
terraform show

# Actualizar infraestructura
terraform plan
terraform apply

# Destruir infraestructura (¡CUIDADO!)
terraform destroy
```

## 📊 Outputs Importantes

Después del despliegue, obtendrás:

- **Load Balancer URL**: URL principal de la aplicación
- **API Base URL**: URL base de la API REST  
- **Swagger Docs URL**: Documentación interactiva de la API
- **CloudWatch Dashboard URL**: Dashboard de monitoreo
- **Database Connection String**: String de conexión a la DB

## 💰 Costos Estimados (AWS Free Tier)

### Recursos Gratuitos (12 meses):
- **EC2 t3.micro**: 750 horas/mes
- **ALB**: 750 horas/mes
- **EBS**: 30 GB/mes
- **CloudWatch**: 10 métricas personalizadas

### Recursos con Costo:
- **DocumentDB**: ~$0.277/hora (db.t3.medium)
- **NAT Gateway**: ~$0.045/hora + datos
- **SES**: $0.10 por 1,000 emails

**Costo estimado mensual**: ~$210-250 USD

### 💡 Optimización de Costos:

1. **Usar instancias Spot** para desarrollo
2. **Parar instancias** fuera de horario laboral
3. **Usar S3** en lugar de EBS para logs antiguos
4. **Configurar Auto Scaling** para escalar a 0 por las noches

## 🔧 Configuración Avanzada

### Backend Remoto (Recomendado para Producción)

1. **Crear bucket S3** para el state:
```bash
aws s3 mb s3://btg-pactual-terraform-state-tu-sufijo
```

2. **Descomentar backend en main.tf**:
```hcl
backend "s3" {
  bucket = "btg-pactual-terraform-state-tu-sufijo"
  key    = "funds-management/terraform.tfstate"
  region = "us-east-1"
}
```

3. **Migrar state**:
```bash
terraform init -migrate-state
```

### Múltiples Entornos

```bash
# Desarrollo
terraform workspace new dev
terraform workspace select dev
terraform apply -var-file="dev.tfvars"

# Producción
terraform workspace new prod
terraform workspace select prod
terraform apply -var-file="prod.tfvars"
```

## 🔍 Troubleshooting

### Problemas Comunes:

1. **Error de permisos AWS**:
```bash
aws sts get-caller-identity  # Verificar identidad
aws iam list-attached-user-policies --user-name tu-usuario
```

2. **Límites de recursos**:
   - Verificar límites de VPC, EC2, EIP en la consola AWS
   - Solicitar aumento de límites si es necesario

3. **Error de DocumentDB**:
   - DocumentDB no está disponible en todas las regiones
   - Verificar disponibilidad en la región seleccionada

4. **Timeout en health checks**:
   - Verificar security groups
   - Revisar logs de la aplicación en CloudWatch

### 📝 Logs y Debug:

```bash
# Debug de Terraform
export TF_LOG=DEBUG
terraform apply

# Logs de instancias EC2
aws logs tail /aws/ec2/btg-pactual-funds-dev --follow
```

## 📚 Documentación Adicional

- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [DocumentDB Best Practices](https://docs.aws.amazon.com/documentdb/latest/developerguide/best_practices.html)

## 🤝 Contribución

1. Crear rama de feature para cambios
2. Ejecutar `terraform plan` para verificar
3. Documentar cambios en este README
4. Crear PR con descripción detallada

---

**⚠️ Importante**: Esta infraestructura está optimizada para desarrollo/testing. Para producción, considera:
- Multi-AZ deployment
- WAF para el ALB  
- Cifrado adicional
- Backup automático más robusto
- Monitoring avanzado con X-Ray
