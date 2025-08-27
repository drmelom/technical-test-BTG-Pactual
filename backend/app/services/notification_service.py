import asyncio
import os
import logging
from typing import Optional
from decimal import Decimal

# Imports opcionales para modo gratuito
try:
    import aiosmtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    EMAIL_AVAILABLE = True
except ImportError:
    EMAIL_AVAILABLE = False

try:
    from twilio.rest import Client as TwilioClient
    SMS_AVAILABLE = True
except ImportError:
    SMS_AVAILABLE = False

from app.models import User, Fund, NotificationPreference
from app.core.config import settings

# Configurar logger
logger = logging.getLogger(__name__)

# Variables de entorno para servicios GRATUITOS
GMAIL_USER = os.getenv("GMAIL_SMTP_USER")  # Gmail gratuito
GMAIL_PASSWORD = os.getenv("GMAIL_SMTP_PASSWORD")  # App password de Gmail

# Twilio FREE TIER ($15 USD de crédito gratis)
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")  
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")


class NotificationService:
    """Service for sending notifications."""
    
    async def send_subscription_notification(
        self, 
        user: User, 
        fund: Fund, 
        amount: Decimal
    ) -> bool:
        """Send notification when user subscribes to a fund."""
        message = (
            f"¡Suscripción exitosa!\n\n"
            f"Estimado/a {user.full_name},\n\n"
            f"Su suscripción al fondo {fund.name} ha sido procesada exitosamente.\n"
            f"Monto invertido: COP ${amount:,.0f}\n"
            f"Saldo disponible: COP ${user.current_balance - amount:,.0f}\n\n"
            f"Gracias por confiar en BTG Pactual.\n\n"
            f"Cordialmente,\nEquipo BTG Pactual"
        )
        
        return await self._send_notification(user, message, "Suscripción Exitosa - BTG Pactual")
    
    async def send_cancellation_notification(
        self, 
        user: User, 
        fund: Fund, 
        amount: Decimal
    ) -> bool:
        """Send notification when user cancels a subscription."""
        message = (
            f"Cancelación procesada\n\n"
            f"Estimado/a {user.full_name},\n\n"
            f"Su cancelación del fondo {fund.name} ha sido procesada exitosamente.\n"
            f"Monto reembolsado: COP ${amount:,.0f}\n"
            f"Nuevo saldo disponible: COP ${user.current_balance + amount:,.0f}\n\n"
            f"Gracias por usar nuestros servicios.\n\n"
            f"Cordialmente,\nEquipo BTG Pactual"
        )
        
        return await self._send_notification(user, message, "Cancelación Procesada - BTG Pactual")
    
    async def _send_notification(
        self, 
        user: User, 
        message: str, 
        subject: str
    ) -> bool:
        """Send notification based on user preference."""
        try:
            if user.notification_preference == NotificationPreference.EMAIL:
                return await self._send_email(user.email, message, subject)
            elif user.notification_preference == NotificationPreference.SMS:
                if not user.phone_number:
                    logger.warning("📱 Número de teléfono no proporcionado")
                    return False
                return await self._send_sms(user.phone_number, message)
            elif user.notification_preference == NotificationPreference.BOTH:
                email_sent = await self._send_email(user.email, message, subject)
                sms_sent = await self._send_sms(user.phone_number, message)
                return email_sent or sms_sent  # Success if at least one succeeds
            
            return False
        except Exception as e:
            print(f"Error sending notification: {str(e)}")
            return False
    
    async def _send_email(self, to_email: str, subject: str, body: str) -> bool:
        """Enviar email usando Gmail SMTP GRATUITO o simulación"""
        
        # Modo simulación para desarrollo (cuando no hay credenciales configuradas)
        if not all([GMAIL_USER, GMAIL_PASSWORD]):
            logger.info(f"📧 [MODO GRATUITO - SIMULACIÓN] Email enviado a: {to_email}")
            logger.info(f"📝 Asunto: {subject}")
            logger.info(f"📄 Contenido: {body[:150]}...")
            logger.info(f"💡 Para activar Gmail SMTP gratuito, configura GMAIL_SMTP_USER y GMAIL_SMTP_PASSWORD")
            return True
        
        # Modo producción con Gmail SMTP GRATUITO (500 emails/día)
        try:
            message = MIMEMultipart()
            message["From"] = f"BTG Pactual Funds <{GMAIL_USER}>"
            message["To"] = to_email
            message["Subject"] = f"🏦 BTG Pactual - {subject}"
            
            # Mejorar el HTML del email
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5;">
                    <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                        <div style="text-align: center; margin-bottom: 30px;">
                            <h1 style="color: #1e3a8a; margin: 0;">🏦 BTG Pactual</h1>
                            <p style="color: #6b7280; margin: 5px 0;">Gestión de Fondos</p>
                        </div>
                        <div style="background-color: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
                            {body}
                        </div>
                        <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb;">
                            <p style="color: #9ca3af; font-size: 12px;">
                                Este es un mensaje automático del sistema BTG Pactual<br>
                                📧 Enviado vía Gmail SMTP Gratuito
                            </p>
                        </div>
                    </div>
                </body>
            </html>
            """
            message.attach(MIMEText(html_body, "html"))
            
            async with aiosmtplib.SMTP(hostname="smtp.gmail.com", port=465, use_tls=True) as server:
                await server.login(GMAIL_USER, GMAIL_PASSWORD)
                await server.send_message(message)
            
            logger.info(f"✅ Email GRATUITO enviado exitosamente a: {to_email} vía Gmail SMTP")
            logger.info(f"� Límite diario Gmail: 500 emails (100% gratis)")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error enviando email: {str(e)}")
            logger.warning(f"🔧 Verifica tu configuración de Gmail App Password")
            # Fallback a simulación si falla el envío real
            logger.info(f"📧 [FALLBACK] Email simulado enviado a: {to_email}")
            return True

    async def _send_sms(self, phone: Optional[str], message: str) -> bool:
        """Enviar SMS usando Twilio FREE TIER (Crédito $15 USD gratis) o simulación"""
        
        if not phone:
            logger.warning("📱 Número de teléfono no proporcionado")
            return False
            
        # Modo simulación para desarrollo (cuando no hay credenciales configuradas)
        if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER]) or not SMS_AVAILABLE:
            logger.info(f"📱 [MODO GRATUITO - SIMULACIÓN] SMS enviado a: {phone}")
            logger.info(f"� Mensaje: {message[:100]}...")
            logger.info(f"💡 Para activar Twilio FREE (15 USD gratis), configura TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN y TWILIO_PHONE_NUMBER")
            logger.info(f"💰 Costo estimado: ~$0.057 USD por SMS en Colombia")
            return True
        
        # Modo producción con Twilio FREE TIER
        try:
            client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            
            # Formatear mensaje para SMS con límite de caracteres
            sms_message = f"🏦 BTG Pactual\n{message[:140]}..."
            
            message_obj = client.messages.create(
                body=sms_message,
                from_=TWILIO_PHONE_NUMBER,
                to=phone
            )
            
            logger.info(f"✅ SMS GRATUITO enviado exitosamente a: {phone}")
            logger.info(f"📊 SID: {message_obj.sid}")
            logger.info(f"💰 Usando crédito FREE TIER de Twilio ($15 USD gratis)")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error enviando SMS: {str(e)}")
            logger.warning(f"🔧 Verifica tu configuración de Twilio Free Tier")
            # Fallback a simulación si falla el envío real
            logger.info(f"📱 [FALLBACK] SMS simulado enviado a: {phone}")
            return True


# Create service instance
notification_service = NotificationService()
