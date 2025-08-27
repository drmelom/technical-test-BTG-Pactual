# Despliegue completo y automatizado de BTG Pactual en EC2
# Lee automáticamente las variables del archivo .env local

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Leer archivo .env local automáticamente
locals {
  env_vars = { for tuple in regexall("(.+)=(.+)", file("${path.module}/../backend/.env")) : tuple[0] => tuple[1] }
}

provider "aws" {
  region = "us-east-1"
}

# Variables mínimas necesarias
variable "key_name" {
  description = "Nombre de la key pair de AWS (debe existir previamente)"
  type        = string
  default     = "your-key-name"  # CAMBIAR por tu key pair existente
}

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
  key_name      = var.key_name
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
  value       = "ssh -i ~/.ssh/${var.key_name}.pem ec2-user@${aws_eip.btg_ip.public_ip}"
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
