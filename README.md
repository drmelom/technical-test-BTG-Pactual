# 🏦 BTG Pactual Funds Management API

Sistema de gestión de fondos de inversión con FastAPI, MongoDB y notificaciones por email/SMS.

## 🚀 Despliegue Rápido

### Desarrollo Local
```bash
cd backend
docker-compose up -d
```

### Producción en AWS (Free Tier)
```bash
cd deployment
cp terraform.tfvars.example terraform.tfvars
# Editar: key_name y repo_url
terraform init
terraform apply
```

## 📁 Estructura del Proyecto

```
├── backend/                 # FastAPI application
│   ├── app/                # Application code
│   ├── docker-compose.yml  # Local development
│   ├── Dockerfile          # Container definition
│   └── .env               # Environment variables
├── deployment/              # AWS deployment files
│   ├── deploy-ec2-simple.tf    # Terraform configuration
│   ├── user_data_complete.sh   # EC2 setup script
│   ├── terraform.tfvars.example # Config template
│   └── README.md               # Deployment guide
├── postman/                # API testing
└── docs/                   # Documentation
```

## � Despliegue en Producción

1. **Ir a la carpeta de deployment:**
   ```bash
   cd deployment
   ```

2. **Seguir las instrucciones** en `deployment/README.md`

## 🌐 URLs después del despliegue
- API: `http://TU-IP:8000`
- Docs: `http://TU-IP:8000/docs`
- MongoDB Express: `http://TU-IP:8000:8081`

## 💰 Costos
$0 - Todo en AWS Free Tier