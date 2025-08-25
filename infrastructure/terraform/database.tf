# DocumentDB Subnet Group
resource "aws_docdb_subnet_group" "main" {
  name       = "${var.project_name}-docdb-subnet-group"
  subnet_ids = aws_subnet.private[*].id

  tags = {
    Name = "${var.project_name}-docdb-subnet-group"
  }
}

# DocumentDB Parameter Group
resource "aws_docdb_cluster_parameter_group" "main" {
  family = "docdb5.0"
  name   = "${var.project_name}-docdb-cluster-params"

  parameter {
    name  = "tls"
    value = "disabled"  # Disable TLS for simplicity in development
  }

  tags = {
    Name = "${var.project_name}-docdb-cluster-params"
  }
}

# DocumentDB Cluster
resource "aws_docdb_cluster" "main" {
  cluster_identifier      = "${var.project_name}-docdb-cluster"
  engine                  = "docdb"
  master_username         = var.docdb_master_username
  master_password         = var.docdb_master_password
  backup_retention_period = var.backup_retention_days
  preferred_backup_window = "07:00-09:00"
  skip_final_snapshot     = true
  
  db_subnet_group_name            = aws_docdb_subnet_group.main.name
  db_cluster_parameter_group_name = aws_docdb_cluster_parameter_group.main.name
  vpc_security_group_ids          = [aws_security_group.docdb.id]

  storage_encrypted = true
  
  # Enable logging
  enabled_cloudwatch_logs_exports = ["audit"]

  tags = {
    Name = "${var.project_name}-docdb-cluster"
  }
}

# DocumentDB Cluster Instances
resource "aws_docdb_cluster_instance" "main" {
  count              = var.docdb_cluster_size
  identifier         = "${var.project_name}-docdb-${count.index}"
  cluster_identifier = aws_docdb_cluster.main.id
  instance_class     = var.docdb_instance_class

  enable_performance_insights = var.enable_monitoring

  tags = {
    Name = "${var.project_name}-docdb-instance-${count.index}"
  }
}

# Random password for DocumentDB (if not provided)
resource "random_password" "docdb_password" {
  count   = var.docdb_master_password == "" ? 1 : 0
  length  = 16
  special = true
}

# Store DocumentDB credentials in Secrets Manager
resource "aws_secretsmanager_secret" "docdb_credentials" {
  name                    = "${var.project_name}-docdb-credentials"
  description             = "DocumentDB cluster credentials"
  recovery_window_in_days = 0  # Force delete for dev environment

  tags = {
    Name = "${var.project_name}-docdb-credentials"
  }
}

resource "aws_secretsmanager_secret_version" "docdb_credentials" {
  secret_id = aws_secretsmanager_secret.docdb_credentials.id
  secret_string = jsonencode({
    username = var.docdb_master_username
    password = var.docdb_master_password != "" ? var.docdb_master_password : random_password.docdb_password[0].result
    endpoint = aws_docdb_cluster.main.endpoint
    port     = aws_docdb_cluster.main.port
  })
}
