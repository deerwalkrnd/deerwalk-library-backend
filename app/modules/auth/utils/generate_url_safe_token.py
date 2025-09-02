import secrets


async def generate_url_safe_token(length: int = 64) -> str:
    return secrets.token_urlsafe(length)
