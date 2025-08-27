# Despliegue simple de BTG Pactual en EC2
# Solo los recursos necesarios para subir el docker-compose existente

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"  # Región free tier
}

# Security Group - abrir puertos necesarios
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

  # Puerto 8081 - Mongo Express (opcional)
  ingress {
    from_port   = 8081
    to_port     = 8081
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # SSH
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Cambiar por tu IP en producción
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

# Key Pair - necesitas crear esto en AWS Console o tener una key
resource "aws_key_pair" "btg_key" {
  key_name   = "btg-pactual-key"
  public_key = file("~/.ssh/id_rsa.pub")  # Ajusta la ruta de tu clave pública
}

# EC2 Instance - t3.micro (free tier)
resource "aws_instance" "btg_app" {
  ami                    = "ami-0c02fb55956c7d316"  # Amazon Linux 2023
  instance_type          = "t3.micro"               # Free tier eligible
  key_name              = aws_key_pair.btg_key.key_name
  vpc_security_group_ids = [aws_security_group.btg_sg.id]

  # Script de instalación
  user_data = base64encode(<<-EOF
    #!/bin/bash
    yum update -y
    yum install -y docker git
    
    # Instalar docker compose
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    
    # Iniciar docker
    systemctl start docker
    systemctl enable docker
    usermod -a -G docker ec2-user
    
    # Crear directorio para la app
    mkdir -p /home/ec2-user/btg-pactual
    chown ec2-user:ec2-user /home/ec2-user/btg-pactual
  EOF
  )

  tags = {
    Name = "BTG Pactual App"
  }

  # Storage mínimo pero suficiente
  root_block_device {
    volume_size = 20  # 20 GB
    volume_type = "gp3"
  }
}

# Elastic IP (opcional pero recomendado)
resource "aws_eip" "btg_ip" {
  instance = aws_instance.btg_app.id
  domain   = "vpc"

  tags = {
    Name = "BTG Pactual IP"
  }
}

# Outputs importantes
output "instance_ip" {
  description = "IP pública de la instancia"
  value       = aws_eip.btg_ip.public_ip
}

output "ssh_command" {
  description = "Comando para conectarse por SSH"
  value       = "ssh -i ~/.ssh/id_rsa ec2-user@${aws_eip.btg_ip.public_ip}"
}

output "api_url" {
  description = "URL de la API"
  value       = "http://${aws_eip.btg_ip.public_ip}:8000"
}

output "mongo_express_url" {
  description = "URL de Mongo Express"
  value       = "http://${aws_eip.btg_ip.public_ip}:8081"
}
