# Configuración súper simple para despliegue BTG Pactual
# Terraform crea automáticamente el key pair y lee las credenciales del backend/.env

# Repositorio - URL actualizada
repo_url = "https://github.com/drmelom/technical-test-BTG-Pactual.git"

# Tu IP para SSH (opcional - 0.0.0.0/0 permite desde cualquier IP)
your_ip = "0.0.0.0/0"

# ✅ Terraform creará automáticamente:
#   - Key pair SSH
#   - Security groups
#   - EC2 instance
#   - Elastic IP
# ✅ Las credenciales se leen del archivo ../backend/.env
# ✅ Solo ejecuta: terraform apply
