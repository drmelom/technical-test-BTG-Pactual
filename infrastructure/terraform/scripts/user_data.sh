#!/bin/bash
# User data script for EC2 instances
# This script will be executed when instances are launched

set -e

# Variables passed from Terraform
PROJECT_NAME="${PROJECT_NAME}"
SECRET_ARN="${SECRET_ARN}"
APP_PORT="${APP_PORT}"

# Update system
yum update -y

# Install required packages
yum install -y docker git htop curl wget unzip jq

# Install AWS CLI v2
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
./aws/install

# Start and enable Docker
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Create application directory
mkdir -p /opt/btg-pactual
cd /opt/btg-pactual

# Clone application repository (replace with your repo)
# git clone https://github.com/drmelom/technical-test-BTG-Pactual.git .
# For now, we'll create the necessary files

# Create docker-compose.yml for production
cat > docker-compose.prod.yml << 'EOF'
version: '3.8'

services:
  backend:
    build: ./backend
    container_name: btg_backend_prod
    restart: unless-stopped
    ports:
      - "${APP_PORT:-8000}:8000"
    environment:
      # These will be populated from AWS Secrets Manager
      MONGODB_URL: ${MONGODB_URL}
      SECRET_KEY: ${SECRET_KEY}
      ENVIRONMENT: production
      PROJECT_NAME: BTG Pactual Funds Management
      
      # AWS Services
      AWS_REGION: ${AWS_DEFAULT_REGION}
      
      # Disable docs in production
      DOCS_URL: 
      REDOC_URL: 
      OPENAPI_URL: 
      
    logging:
      driver: awslogs
      options:
        awslogs-group: "/aws/ec2/${PROJECT_NAME}"
        awslogs-region: "${AWS_DEFAULT_REGION}"
        awslogs-stream-prefix: "backend"
    
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

networks:
  default:
    name: btg_network
EOF

# Create environment file from AWS Secrets Manager
get_secret_value() {
    aws secretsmanager get-secret-value --secret-id "$SECRET_ARN" --query SecretString --output text --region $(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone | sed 's/.$//')
}

# Function to extract value from JSON
extract_json_value() {
    echo "$1" | jq -r ".$2"
}

# Get database credentials from Secrets Manager
echo "Retrieving database credentials from Secrets Manager..."
SECRET_JSON=$(get_secret_value)

if [ $? -eq 0 ]; then
    DB_USERNAME=$(extract_json_value "$SECRET_JSON" "username")
    DB_PASSWORD=$(extract_json_value "$SECRET_JSON" "password")
    DB_ENDPOINT=$(extract_json_value "$SECRET_JSON" "endpoint")
    DB_PORT=$(extract_json_value "$SECRET_JSON" "port")
    
    # Create .env file
    cat > .env << EOF
# Database Configuration
MONGODB_URL=mongodb://${DB_USERNAME}:${DB_PASSWORD}@${DB_ENDPOINT}:${DB_PORT}/btg_pactual?ssl=false&retryWrites=false
DATABASE_NAME=btg_pactual

# Security
SECRET_KEY=$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
ENVIRONMENT=production
PROJECT_NAME=BTG Pactual Funds Management
VERSION=1.0.0
API_V1_STR=/api/v1

# AWS Configuration
AWS_REGION=$(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone | sed 's/.$//')

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Disable docs in production
DOCS_URL=
REDOC_URL=
OPENAPI_URL=
EOF

    echo "Environment configuration created successfully."
else
    echo "Failed to retrieve database credentials from Secrets Manager."
    exit 1
fi

# Install CloudWatch Agent
wget https://s3.amazonaws.com/amazoncloudwatch-agent/amazon_linux/amd64/latest/amazon-cloudwatch-agent.rpm
rpm -U ./amazon-cloudwatch-agent.rpm

# Configure CloudWatch Agent
cat > /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json << EOF
{
    "logs": {
        "logs_collected": {
            "files": {
                "collect_list": [
                    {
                        "file_path": "/opt/btg-pactual/logs/app.log",
                        "log_group_name": "/aws/ec2/${PROJECT_NAME}",
                        "log_stream_name": "{instance_id}/app",
                        "timezone": "UTC",
                        "timestamp_format": "%Y-%m-%d %H:%M:%S"
                    },
                    {
                        "file_path": "/var/log/docker",
                        "log_group_name": "/aws/ec2/${PROJECT_NAME}",
                        "log_stream_name": "{instance_id}/docker",
                        "timezone": "UTC"
                    }
                ]
            }
        }
    },
    "metrics": {
        "namespace": "BTG-Pactual/Application",
        "metrics_collected": {
            "cpu": {
                "measurement": ["cpu_usage_idle", "cpu_usage_iowait", "cpu_usage_user", "cpu_usage_system"],
                "metrics_collection_interval": 60,
                "resources": ["*"],
                "totalcpu": false
            },
            "disk": {
                "measurement": ["used_percent"],
                "metrics_collection_interval": 60,
                "resources": ["*"]
            },
            "diskio": {
                "measurement": ["io_time", "read_bytes", "write_bytes", "reads", "writes"],
                "metrics_collection_interval": 60,
                "resources": ["*"]
            },
            "mem": {
                "measurement": ["mem_used_percent"],
                "metrics_collection_interval": 60
            },
            "netstat": {
                "measurement": ["tcp_established", "tcp_time_wait"],
                "metrics_collection_interval": 60
            },
            "swap": {
                "measurement": ["swap_used_percent"],
                "metrics_collection_interval": 60
            }
        }
    }
}
EOF

# Start CloudWatch Agent
/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -s -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json

# Create systemd service for the application
cat > /etc/systemd/system/btg-pactual.service << 'EOF'
[Unit]
Description=BTG Pactual Funds Management API
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/btg-pactual
ExecStart=/usr/local/bin/docker-compose -f docker-compose.prod.yml up -d
ExecStop=/usr/local/bin/docker-compose -f docker-compose.prod.yml down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
systemctl daemon-reload
systemctl enable btg-pactual.service

# Create log directory
mkdir -p /opt/btg-pactual/logs

# Create health check script
cat > /opt/btg-pactual/health-check.sh << 'EOF'
#!/bin/bash
# Health check script for the application

HEALTH_URL="http://localhost:${APP_PORT:-8000}/health"
MAX_RETRIES=3
RETRY_DELAY=5

for i in $(seq 1 $MAX_RETRIES); do
    if curl -f -s "$HEALTH_URL" > /dev/null; then
        echo "$(date): Health check passed"
        exit 0
    else
        echo "$(date): Health check failed (attempt $i/$MAX_RETRIES)"
        if [ $i -lt $MAX_RETRIES ]; then
            sleep $RETRY_DELAY
        fi
    fi
done

echo "$(date): Health check failed after $MAX_RETRIES attempts"
exit 1
EOF

chmod +x /opt/btg-pactual/health-check.sh

# Set up log rotation
cat > /etc/logrotate.d/btg-pactual << 'EOF'
/opt/btg-pactual/logs/*.log {
    daily
    missingok
    rotate 7
    compress
    notifempty
    create 0644 root root
    postrotate
        systemctl reload btg-pactual.service > /dev/null 2>&1 || true
    endscript
}
EOF

# Start the application service
echo "Starting BTG Pactual application..."
systemctl start btg-pactual.service

# Wait for the application to be ready
sleep 30

# Run health check
/opt/btg-pactual/health-check.sh

if [ $? -eq 0 ]; then
    echo "BTG Pactual application is running successfully!"
    
    # Log instance information
    cat > /opt/btg-pactual/logs/deployment.log << EOF
Deployment completed successfully at $(date)
Instance ID: $(curl -s http://169.254.169.254/latest/meta-data/instance-id)
Instance Type: $(curl -s http://169.254.169.254/latest/meta-data/instance-type)
Availability Zone: $(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone)
Private IP: $(curl -s http://169.254.169.254/latest/meta-data/local-ipv4)
Public IP: $(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
Project: ${PROJECT_NAME}
Application Port: ${APP_PORT}
EOF

else
    echo "Failed to start BTG Pactual application!"
    exit 1
fi

echo "EC2 instance setup completed successfully!"
