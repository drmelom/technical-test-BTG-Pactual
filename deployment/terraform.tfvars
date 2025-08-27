# Configuración mínima para despliegue BTG Pactual
# Terraform lee automáticamente las credenciales del archivo backend/.env

# AWS Configuration
key_name = "your-key-name"  # Nombre de tu key pair existente en AWS
your_ip  = "0.0.0.0/0"      # Tu IP para SSH (opcional)

# Repositorio
repo_url = "https://github.com/drmelom/technical-test-BTG-Pactual.git"

# ✅ Las credenciales de Gmail y Twilio se leen automáticamente del archivo backend/.env
# ✅ No necesitas configurar nada más
# ✅ Solo ejecuta: terraform apply
