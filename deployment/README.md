# 🚀 Despliegue en AWS - BTG Pactual

Despliegue automatizado de la API BTG Pactual en una instancia EC2 usando Terraform.

## 📋 Prerrequisitos

1. **Terraform instalado**
2. **AWS CLI configurado** con tus credenciales
3. **Key Pair creada** en AWS Console (EC2 > Key Pairs)
4. **Tu repositorio en GitHub** (público o con acceso)

## 🚀 Despliegue

### 1. Configuración
```bash
cd deployment
cp terraform.tfvars.example terraform.tfvars
```

Edita `terraform.tfvars` con:
- `key_name`: Nombre de tu key pair en AWS
- `repo_url`: URL de tu repositorio

### 2. Deploy automático
```bash
terraform init
terraform apply
```

## 📁 Archivos en esta carpeta

- `deploy-ec2-simple.tf` - Configuración principal de Terraform
- `user_data_complete.sh` - Script de setup automático en EC2
- `terraform.tfvars.example` - Plantilla de configuración
- `README.md` - Esta documentación

## ✅ Qué hace automáticamente

1. Crea instancia EC2 (t3.micro free tier)
2. Instala Docker y Docker Compose
3. Clona tu repositorio
4. Copia variables de entorno desde `../backend/.env`
5. Ejecuta `docker-compose up -d --build`
6. Configura scripts de utilidad

## 🌐 URLs después del despliegue

Terraform mostrará al final:
- API: `http://IP:8000`
- Docs: `http://IP:8000/docs`
- MongoDB Express: `http://IP:8000:8081`

## ⏱️ Tiempo estimado
- Terraform: ~2 min
- Setup automático: ~8 min
- **Total: ~10 min**

## 🧹 Limpiar recursos
```bash
terraform destroy
```

## 💰 Costos
**$0** - Todo en Free Tier de AWS
