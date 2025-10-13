from typing import Any, Dict

from app.modules.auth.domain.services.token_service_interface import \
    TokenServiceInterface


class GenerateJWTTokenUseCase:
    def __init__(self, token_service: TokenServiceInterface) -> None:
        self.token_service = token_service

    async def execute(self, payload: Dict[Any, Any]) -> str:
        return await self.token_service.encode(payload=payload)
