import asyncio
from typing import Optional
from decimal import Decimal

from app.models import User, Fund, NotificationPreference
from app.core.config import settings


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
                return await self._send_sms(user.phone, message)
            elif user.notification_preference == NotificationPreference.BOTH:
                email_sent = await self._send_email(user.email, message, subject)
                sms_sent = await self._send_sms(user.phone, message)
                return email_sent or sms_sent  # Success if at least one succeeds
            
            return False
        except Exception as e:
            print(f"Error sending notification: {str(e)}")
            return False
    
    async def _send_email(
        self, 
        email: str, 
        message: str, 
        subject: str
    ) -> bool:
        """Send email notification."""
        try:
            # Check if email configuration is available
            if not settings.SMTP_USERNAME or not settings.SMTP_PASSWORD:
                # Fallback to simulation for development
                print(f"📧 [SIMULATED] EMAIL TO: {email}")
                print(f"📧 [SIMULATED] SUBJECT: {subject}")
                print(f"📧 [SIMULATED] MESSAGE: {message[:100]}...")
                print("-" * 50)
                await asyncio.sleep(0.1)
                return True
            
            # Real email implementation with aiosmtplib
            import aiosmtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            msg = MIMEMultipart()
            msg['From'] = settings.EMAIL_FROM
            msg['To'] = email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))
            
            await aiosmtplib.send(
                msg,
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                start_tls=True,
                username=settings.SMTP_USERNAME,
                password=settings.SMTP_PASSWORD
            )
            
            print(f"📧 [REAL] EMAIL SENT TO: {email}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending email: {str(e)}")
            # Fallback to simulation on error
            print(f"📧 [FALLBACK] EMAIL TO: {email}")
            return False
    
    async def _send_sms(self, phone: Optional[str], message: str) -> bool:
        """Send SMS notification."""
        try:
            if not phone:
                return False
            
            # Check if Twilio configuration is available
            if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
                # Fallback to simulation for development
                print(f"📱 [SIMULATED] SMS TO: {phone}")
                print(f"📱 [SIMULATED] MESSAGE: {message[:100]}...")
                print("-" * 50)
                await asyncio.sleep(0.1)
                return True
            
            # Real SMS implementation with Twilio
            from twilio.rest import Client
            
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            
            message_obj = client.messages.create(
                body=message,
                from_=settings.TWILIO_FROM_PHONE,
                to=phone
            )
            
            print(f"📱 [REAL] SMS SENT TO: {phone}, SID: {message_obj.sid}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending SMS: {str(e)}")
            # Fallback to simulation on error
            print(f"📱 [FALLBACK] SMS TO: {phone}")
            return False


# Create service instance
notification_service = NotificationService()
