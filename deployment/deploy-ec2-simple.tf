# Despliegue completo y automatizado de BTG Pactual en EC2
# Lee automáticamente las variables del archivo .env local

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.1"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.1"
    }
  }
}

# Leer archivo .env local automáticamente
locals {
  env_vars = { for tuple in regexall("(.+)=(.+)", file("${path.module}/../backend/.env")) : tuple[0] => tuple[1] }
}

provider "aws" {
  region  = "us-east-1"
  profile = "personal"  # Usar perfil personal separado de la empresa
}

# Variables mínimas necesarias
variable "your_ip" {
  description = "Tu IP pública para SSH (opcional, por defecto permite todas)"
  type        = string
  default     = "0.0.0.0/0"
}

variable "repo_url" {
  description = "URL del repositorio GitHub"
  type        = string
  default     = "https://github.com/drmelom/technical-test-BTG-Pactual.git"  # CAMBIAR
}

# Generar key pair automáticamente
resource "tls_private_key" "btg_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

# Crear key pair en AWS usando la key generada
resource "aws_key_pair" "btg_key" {
  key_name   = "btg-pactual-${random_string.suffix.result}"
  public_key = tls_private_key.btg_key.public_key_openssh

  tags = {
    Name = "BTG Pactual Key"
  }
}

# String random para hacer único el nombre del key
resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
}

# Guardar la private key localmente
resource "local_file" "private_key" {
  content         = tls_private_key.btg_key.private_key_pem
  filename        = "${path.module}/btg-pactual-key.pem"
  file_permission = "0600"
}

# Security Group
resource "aws_security_group" "btg_sg" {
  name        = "btg-pactual-sg"
  description = "Security group for BTG Pactual app"

  # Puerto 8000 - FastAPI
  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Puerto 8081 - Mongo Express
  ingress {
    from_port   = 8081
    to_port     = 8081
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Puerto 80 - HTTP
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # SSH
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.your_ip]
  }

  # Salida libre
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "BTG Pactual SG"
  }
}

# EC2 Instance con variables del .env local
resource "aws_instance" "btg_app" {
  ami           = "ami-0c02fb55956c7d316"  # Amazon Linux 2023
  instance_type = "t3.micro"               # Free tier eligible
  key_name      = aws_key_pair.btg_key.key_name
  vpc_security_group_ids = [aws_security_group.btg_sg.id]

  # Script que copia el .env completo
  user_data = base64encode(templatefile("${path.module}/user_data_complete.sh", {
    repo_url    = var.repo_url
    env_content = file("${path.module}/../backend/.env")
  }))

  tags = {
    Name = "BTG Pactual App"
  }

  root_block_device {
    volume_size = 20
    volume_type = "gp3"
  }
}

# Elastic IP
resource "aws_eip" "btg_ip" {
  instance = aws_instance.btg_app.id
  domain   = "vpc"

  tags = {
    Name = "BTG Pactual IP"
  }
}

# Outputs
output "instance_ip" {
  description = "IP pública de la instancia"
  value       = aws_eip.btg_ip.public_ip
}

output "ssh_command" {
  description = "Comando para conectarse por SSH"
  value       = "ssh -i ${path.module}/btg-pactual-key.pem ec2-user@${aws_eip.btg_ip.public_ip}"
}

output "private_key_location" {
  description = "Ubicación de la clave privada"
  value       = "${path.module}/btg-pactual-key.pem"
}

output "key_pair_name" {
  description = "Nombre del key pair creado en AWS"
  value       = aws_key_pair.btg_key.key_name
}

output "api_url" {
  description = "URL de la API"
  value       = "http://${aws_eip.btg_ip.public_ip}:8000"
}

output "docs_url" {
  description = "URL de la documentación"
  value       = "http://${aws_eip.btg_ip.public_ip}:8000/docs"
}

output "mongo_express_url" {
  description = "URL de Mongo Express"
  value       = "http://${aws_eip.btg_ip.public_ip}:8081"
}

output "env_vars_loaded" {
  description = "Variables de entorno cargadas desde .env"
  value       = "Gmail: ${try(local.env_vars.GMAIL_SMTP_USER, "no configurado")}, Twilio: ${try(local.env_vars.TWILIO_ACCOUNT_SID != "" ? "configurado" : "no configurado", "no configurado")}"
  sensitive   = false
}
