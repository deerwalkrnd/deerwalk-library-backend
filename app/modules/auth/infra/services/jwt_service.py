from typing import Any

import jwt

from app.core.config import Settings
from app.core.dependencies.get_settings import get_settings
from app.modules.auth.domain.services.token_service_interface import \
    TokenServiceInterface


class JWTService(TokenServiceInterface):
    def __init__(self) -> None:
        settings: Settings = get_settings()
        self.key = settings.jtw_key

    async def encode(self, payload: dict[str, Any]) -> str:
        return jwt.encode(payload=payload, key=self.key, algorithm="HS256")  # type:ignore

    async def decode(self, payload: str) -> dict[str, Any]:
        return jwt.decode(payload, key=self.key, algorithms="HS256")  # type: ignore
