from aiosmtplib import SMTP

from app.core.dependencies.get_settings import get_settings


async def get_smtp() -> SMTP:
    settings = get_settings()
    return SMTP(
        hostname=settings.smtp_host,
        port=settings.smtp_port,
        # use_tls=settings.smtp_use_tls,
        start_tls=settings.smtp_use_tls,
        username=settings.smtp_username,
        password=settings.smtp_password,
    )
