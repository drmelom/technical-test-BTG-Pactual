# Infraestructura AWS Free Tier - BTG Pactual
## Configuración usando solo servicios GRATUITOS

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Provider AWS configurado para Free Tier
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      Owner       = var.owner
      ManagedBy   = "Terraform"
      FreeTier    = "true"
    }
  }
}

# VPC gratuita (incluida en Free Tier)
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.project_name}-${var.environment}-vpc"
  }
}

# Internet Gateway (gratuito)
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project_name}-${var.environment}-igw"
  }
}

# Subnets públicas (gratuitas)
resource "aws_subnet" "public" {
  count             = min(length(var.public_subnet_cidrs), 2)  # Solo 2 para Free Tier
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.public_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]
  
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project_name}-${var.environment}-public-subnet-${count.index + 1}"
    Type = "Public"
  }
}

# Route Table para subnets públicas
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-public-rt"
  }
}

# Asociar route table con subnets públicas
resource "aws_route_table_association" "public" {
  count          = length(aws_subnet.public)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# Security Group para la aplicación (gratuito)
resource "aws_security_group" "app" {
  name        = "${var.project_name}-${var.environment}-app"
  description = "Security group for BTG Pactual app - Free Tier"
  vpc_id      = aws_vpc.main.id

  # HTTP access
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTPS access  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Application port
  ingress {
    from_port   = var.app_port
    to_port     = var.app_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # SSH access
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Restringir en producción
  }

  # All outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-app-sg"
  }
}

# EC2 Instance para aplicación (FREE TIER ELIGIBLE - t2.micro)
resource "aws_instance" "app" {
  ami                    = "ami-0c02fb55956c7d316"  # Amazon Linux 2023 Free Tier
  instance_type          = "t2.micro"                # FREE TIER - 750 horas/mes gratis
  subnet_id             = aws_subnet.public[0].id
  vpc_security_group_ids = [aws_security_group.app.id]
  
  # User data para instalación automática
  user_data = base64encode(templatefile("${path.module}/scripts/install_docker.sh", {
    app_port = var.app_port
  }))

  # Storage (8 GB incluidos en Free Tier)
  root_block_device {
    volume_size = 8  # Máximo gratis en Free Tier
    volume_type = "gp2"
    encrypted   = false  # Encriptación no disponible en Free Tier
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-app"
    FreeTier = "t2.micro-eligible"
  }
}

# MongoDB usando contenedor Docker (GRATIS)
# En lugar de DocumentDB que es pagado, usaremos MongoDB containerizado
resource "null_resource" "deploy_mongodb" {
  depends_on = [aws_instance.app]

  provisioner "remote-exec" {
    inline = [
      "sudo yum update -y",
      "sudo yum install -y docker git",
      "sudo systemctl start docker",
      "sudo systemctl enable docker",
      "sudo usermod -a -G docker ec2-user",
      
      # Crear volumen para persistencia de MongoDB
      "sudo mkdir -p /opt/mongodb/data",
      "sudo chown -R ec2-user:ec2-user /opt/mongodb",
      
      # Ejecutar MongoDB en contenedor con persistencia
      "docker run -d --name mongodb --restart always -p 27017:27017 -v /opt/mongodb/data:/data/db -e MONGO_INITDB_ROOT_USERNAME=btgadmin -e MONGO_INITDB_ROOT_PASSWORD=BtgP@ssw0rd123 mongo:7-jammy",
      
      # Esperar que MongoDB inicie
      "sleep 30",
      
      # Crear base de datos y usuario
      "docker exec mongodb mongosh --eval 'use btg_funds_db; db.createUser({user: \"btguser\", pwd: \"BtgUser123!\", roles: [\"readWrite\"]})'"
    ]

    connection {
      type = "ssh"
      host = aws_instance.app.public_ip
      user = "ec2-user"
      # Para conexión SSH, necesitarás configurar tu key pair
      # private_key = file("path/to/your/private/key.pem")
    }
  }
}

# Elastic IP (1 gratis en Free Tier)
resource "aws_eip" "app" {
  instance = aws_instance.app.id
  domain   = "vpc"

  tags = {
    Name = "${var.project_name}-${var.environment}-eip"
  }

  depends_on = [aws_internet_gateway.main]
}
