from datetime import datetime, timedelta


async def generate_url_safe_token_expiry(minutes: int = 5) -> datetime:
    expires_at = datetime.now() + timedelta(minutes)
    return expires_at
