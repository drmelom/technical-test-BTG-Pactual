# Network Outputs
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "vpc_cidr_block" {
  description = "CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}

output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "IDs of the private subnets"
  value       = aws_subnet.private[*].id
}

# Load Balancer Outputs
output "load_balancer_url" {
  description = "URL of the Application Load Balancer"
  value       = "http://${aws_lb.main.dns_name}"
}

output "load_balancer_zone_id" {
  description = "Canonical hosted zone ID of the load balancer"
  value       = aws_lb.main.zone_id
}

output "load_balancer_dns_name" {
  description = "DNS name of the load balancer"
  value       = aws_lb.main.dns_name
}

# Database Outputs
output "docdb_cluster_endpoint" {
  description = "DocumentDB cluster endpoint"
  value       = aws_docdb_cluster.main.endpoint
  sensitive   = true
}

output "docdb_cluster_reader_endpoint" {
  description = "DocumentDB cluster reader endpoint"
  value       = aws_docdb_cluster.main.reader_endpoint
  sensitive   = true
}

output "docdb_cluster_port" {
  description = "DocumentDB cluster port"
  value       = aws_docdb_cluster.main.port
}

output "docdb_cluster_identifier" {
  description = "DocumentDB cluster identifier"
  value       = aws_docdb_cluster.main.cluster_identifier
}

# Security Group Outputs
output "alb_security_group_id" {
  description = "ID of the ALB security group"
  value       = aws_security_group.alb.id
}

output "ec2_security_group_id" {
  description = "ID of the EC2 security group"
  value       = aws_security_group.ec2.id
}

output "docdb_security_group_id" {
  description = "ID of the DocumentDB security group"
  value       = aws_security_group.docdb.id
}

# Auto Scaling Outputs
output "autoscaling_group_name" {
  description = "Name of the Auto Scaling Group"
  value       = aws_autoscaling_group.main.name
}

output "autoscaling_group_arn" {
  description = "ARN of the Auto Scaling Group"
  value       = aws_autoscaling_group.main.arn
}

# IAM Outputs
output "ec2_instance_profile_name" {
  description = "Name of the EC2 instance profile"
  value       = aws_iam_instance_profile.ec2_profile.name
}

output "ec2_role_arn" {
  description = "ARN of the EC2 IAM role"
  value       = aws_iam_role.ec2_role.arn
}

# Messaging Outputs
output "sns_topic_notifications_arn" {
  description = "ARN of the notifications SNS topic"
  value       = aws_sns_topic.notifications.arn
}

output "sns_topic_alerts_arn" {
  description = "ARN of the alerts SNS topic"
  value       = aws_sns_topic.alerts.arn
}

output "ses_domain_identity" {
  description = "SES domain identity"
  value       = aws_ses_domain_identity.main.domain
}

# Secrets Manager Outputs
output "docdb_credentials_secret_arn" {
  description = "ARN of the DocumentDB credentials secret"
  value       = aws_secretsmanager_secret.docdb_credentials.arn
  sensitive   = true
}

# Monitoring Outputs
output "cloudwatch_dashboard_url" {
  description = "URL to the CloudWatch dashboard"
  value       = "https://${var.aws_region}.console.aws.amazon.com/cloudwatch/home?region=${var.aws_region}#dashboards:name=${aws_cloudwatch_dashboard.main.dashboard_name}"
}

output "cloudwatch_log_group_app" {
  description = "Name of the application CloudWatch log group"
  value       = aws_cloudwatch_log_group.app_logs.name
}

# Application URLs and Endpoints
output "api_base_url" {
  description = "Base URL for the API"
  value       = "http://${aws_lb.main.dns_name}/api/v1"
}

output "health_check_url" {
  description = "Health check URL"
  value       = "http://${aws_lb.main.dns_name}${var.health_check_path}"
}

output "swagger_docs_url" {
  description = "Swagger documentation URL"
  value       = "http://${aws_lb.main.dns_name}/docs"
}

# Environment Information
output "environment_summary" {
  description = "Summary of the deployed environment"
  value = {
    project_name    = var.project_name
    environment     = var.environment
    aws_region      = var.aws_region
    vpc_id          = aws_vpc.main.id
    load_balancer   = aws_lb.main.dns_name
    database        = aws_docdb_cluster.main.cluster_identifier
    instance_count  = var.desired_capacity
  }
}

# Database Connection String (for application configuration)
output "database_connection_string" {
  description = "Database connection string for the application"
  value       = "mongodb://${var.docdb_master_username}:${var.docdb_master_password}@${aws_docdb_cluster.main.endpoint}:${aws_docdb_cluster.main.port}/btg_pactual?ssl=false&retryWrites=false"
  sensitive   = true
}
