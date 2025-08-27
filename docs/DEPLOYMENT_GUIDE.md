# 🚀 Despliegue Súper Simplificado - BTG Pactual

## ✅ Prerrequisitos

1. **Terraform instalado** en tu máquina
2. **AWS CLI configurado** con tus credenciales
3. **Key Pair** creada en AWS Console (EC2 > Key Pairs)
4. **Tu archivo `.env` en `backend/.env`** con las credenciales que ya funcionan en local

## 🏗️ Despliegue en 2 pasos

### 1. Configuración mínima (30 segundos)
```bash
# Copiar y ajustar solo 2 variables
cp terraform.tfvars.example terraform.tfvars
nano terraform.tfvars

# Solo cambiar:
# key_name = "tu-key-pair-name"
# repo_url = "https://github.com/tu-usuario/tu-repo.git"
```

### 2. ¡Deploy automático! (1 comando)
```bash
terraform init
terraform apply
```

## 🎯 ¡ESO ES TODO!

- ✅ **Lee automáticamente** tu archivo `backend/.env`
- ✅ **Usa las mismas credenciales** que tienes en local
- ✅ **No duplicas configuración**
- ✅ **Todo en un comando**

## ⏱️ Tiempos
- **terraform apply**: ~2 minutos
- **Despliegue completo**: ~8 minutos
- **Total**: Una taza de café ☕

## 🔍 Verificar
```bash
# Terraform te dará las URLs al final:
# API: http://TU-IP:8000/docs
curl http://TU-IP:8000/health
```

## 🛠️ ¿Algo salió mal?
```bash
# Ver logs del despliegue
ssh -i ~/.ssh/tu-key.pem ec2-user@TU-IP
sudo tail -f /var/log/btg-deployment.log

# Reiniciar servicios
cd /home/ec2-user/btg-pactual && ./restart.sh
```

## 💡 Ventajas de este enfoque
- ✅ **DRY**: No repites configuración
- ✅ **Seguro**: Credenciales solo en un lugar
- ✅ **Simple**: Solo 2 variables en terraform.tfvars
- ✅ **Automático**: Lee tu .env existente
- ✅ **Consistente**: Misma config local y producción

## 🧹 Limpiar
```bash
terraform destroy
```

## 💰 Costos
**$0** - Todo en Free Tier
