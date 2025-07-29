from email.mime.multipart import MIMEMultipart

from aiosmtplib import SMTP

from app.core.domain.services.email_service_interface import EmailServiceInterface


class EmailNotificationService(EmailServiceInterface):
    def __init__(self, smtp: SMTP) -> None:
        self.smtp = smtp

    async def send_email(self, message: MIMEMultipart) -> None:
        async with self.smtp as smtp_client:
            await smtp_client.send_message(message)
