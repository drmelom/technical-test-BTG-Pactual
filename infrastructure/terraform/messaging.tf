# SES Domain Identity
resource "aws_ses_domain_identity" "main" {
  domain = var.ses_domain
}

# SES Domain DKIM
resource "aws_ses_domain_dkim" "main" {
  domain = aws_ses_domain_identity.main.domain
}

# SES Configuration Set
resource "aws_ses_configuration_set" "main" {
  name = "${var.project_name}-ses-config-set"
}

# SES Event Destination for CloudWatch
resource "aws_ses_event_destination" "cloudwatch" {
  name                   = "cloudwatch-destination"
  configuration_set_name = aws_ses_configuration_set.main.name
  enabled                = true
  matching_types         = ["send", "reject", "bounce", "complaint", "delivery"]

  cloudwatch_destination {
    default_value  = "default"
    dimension_name = "EmailAddress"
    value_source   = "emailAddress"
  }
}

# SNS Topic for SMS notifications
resource "aws_sns_topic" "notifications" {
  name = "${var.project_name}-notifications"

  tags = {
    Name = "${var.project_name}-notifications-topic"
  }
}

# SNS Topic Policy
resource "aws_sns_topic_policy" "notifications" {
  arn = aws_sns_topic.notifications.arn

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          AWS = aws_iam_role.ec2_role.arn
        }
        Action = [
          "SNS:Publish"
        ]
        Resource = aws_sns_topic.notifications.arn
      }
    ]
  })
}

# CloudWatch Log Group for SES
resource "aws_cloudwatch_log_group" "ses_logs" {
  name              = "/aws/ses/${var.project_name}"
  retention_in_days = var.log_retention_days

  tags = {
    Name = "${var.project_name}-ses-logs"
  }
}

# CloudWatch Log Group for SNS
resource "aws_cloudwatch_log_group" "sns_logs" {
  name              = "/aws/sns/${var.project_name}"
  retention_in_days = var.log_retention_days

  tags = {
    Name = "${var.project_name}-sns-logs"
  }
}

# SES Email Template for fund subscriptions
resource "aws_ses_template" "fund_subscription" {
  name    = "${var.project_name}-fund-subscription"
  subject = "Confirmación de Suscripción a Fondo - {{fund_name}}"
  
  html = <<-EOT
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>BTG Pactual - Confirmación de Suscripción</title>
</head>
<body>
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h1 style="color: #1976d2;">BTG Pactual</h1>
        <h2>Confirmación de Suscripción a Fondo</h2>
        
        <p>Estimado/a {{user_name}},</p>
        
        <p>Su suscripción al fondo <strong>{{fund_name}}</strong> ha sido procesada exitosamente.</p>
        
        <div style="background-color: #f5f5f5; padding: 20px; margin: 20px 0;">
            <h3>Detalles de la transacción:</h3>
            <ul>
                <li><strong>Fondo:</strong> {{fund_name}}</li>
                <li><strong>Monto:</strong> $${amount} COP</li>
                <li><strong>Fecha:</strong> {{transaction_date}}</li>
                <li><strong>ID de Transacción:</strong> {{transaction_id}}</li>
            </ul>
        </div>
        
        <p>Puede consultar el estado de sus inversiones ingresando a nuestra plataforma.</p>
        
        <p>Gracias por confiar en BTG Pactual.</p>
        
        <hr>
        <p style="font-size: 12px; color: #666;">
            Este es un correo automático, por favor no responda a este mensaje.
        </p>
    </div>
</body>
</html>
EOT

  text = <<-EOT
BTG Pactual - Confirmación de Suscripción

Estimado/a {{user_name}},

Su suscripción al fondo {{fund_name}} ha sido procesada exitosamente.

Detalles de la transacción:
- Fondo: {{fund_name}}
- Monto: $${amount} COP
- Fecha: {{transaction_date}}
- ID de Transacción: {{transaction_id}}

Puede consultar el estado de sus inversiones ingresando a nuestra plataforma.

Gracias por confiar en BTG Pactual.

Este es un correo automático, por favor no responda a este mensaje.
EOT
}

# SES Email Template for fund cancellations
resource "aws_ses_template" "fund_cancellation" {
  name    = "${var.project_name}-fund-cancellation"
  subject = "Confirmación de Cancelación de Fondo - {{fund_name}}"
  
  html = <<-EOT
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>BTG Pactual - Confirmación de Cancelación</title>
</head>
<body>
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h1 style="color: #1976d2;">BTG Pactual</h1>
        <h2>Confirmación de Cancelación de Fondo</h2>
        
        <p>Estimado/a {{user_name}},</p>
        
        <p>Su cancelación del fondo <strong>{{fund_name}}</strong> ha sido procesada exitosamente.</p>
        
        <div style="background-color: #f5f5f5; padding: 20px; margin: 20px 0;">
            <h3>Detalles de la cancelación:</h3>
            <ul>
                <li><strong>Fondo:</strong> {{fund_name}}</li>
                <li><strong>Monto reembolsado:</strong> $${amount} COP</li>
                <li><strong>Fecha:</strong> {{transaction_date}}</li>
                <li><strong>ID de Transacción:</strong> {{transaction_id}}</li>
            </ul>
        </div>
        
        <p>El monto ha sido devuelto a su saldo disponible.</p>
        
        <p>Gracias por confiar en BTG Pactual.</p>
        
        <hr>
        <p style="font-size: 12px; color: #666;">
            Este es un correo automático, por favor no responda a este mensaje.
        </p>
    </div>
</body>
</html>
EOT

  text = <<-EOT
BTG Pactual - Confirmación de Cancelación

Estimado/a {{user_name}},

Su cancelación del fondo {{fund_name}} ha sido procesada exitosamente.

Detalles de la cancelación:
- Fondo: {{fund_name}}
- Monto reembolsado: $${amount} COP
- Fecha: {{transaction_date}}
- ID de Transacción: {{transaction_id}}

El monto ha sido devuelto a su saldo disponible.

Gracias por confiar en BTG Pactual.

Este es un correo automático, por favor no responda a este mensaje.
EOT
}
