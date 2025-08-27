from datetime import datetime, timedelta
import secrets


async def generate_password_reset_token() -> tuple[str, datetime]:
    raw_token = secrets.token_urlsafe(64)

    expires_at = datetime.now() + timedelta(minutes=5)

    return raw_token, expires_at
