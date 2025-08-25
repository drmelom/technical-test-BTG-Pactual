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
            # In a real implementation, you would use aiosmtplib or similar
            # For now, we'll simulate the email sending
            
            print(f"📧 EMAIL SENT TO: {email}")
            print(f"📧 SUBJECT: {subject}")
            print(f"📧 MESSAGE: {message}")
            print("-" * 50)
            
            # Simulate async email sending delay
            await asyncio.sleep(0.1)
            
            return True
            
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False
    
    async def _send_sms(self, phone: Optional[str], message: str) -> bool:
        """Send SMS notification."""
        try:
            if not phone:
                return False
            
            # In a real implementation, you would use Twilio or similar
            # For now, we'll simulate the SMS sending
            
            print(f"📱 SMS SENT TO: {phone}")
            print(f"📱 MESSAGE: {message}")
            print("-" * 50)
            
            # Simulate async SMS sending delay
            await asyncio.sleep(0.1)
            
            return True
            
        except Exception as e:
            print(f"Error sending SMS: {str(e)}")
            return False


# Create service instance
notification_service = NotificationService()
