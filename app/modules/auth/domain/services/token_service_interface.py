from abc import ABC, abstractmethod
from typing import Any


class TokenServiceInterface(ABC):
    @abstractmethod
    async def encode(self, payload: dict[str, Any]) -> str:
        raise NotImplementedError

    @abstractmethod
    async def decode(self, payload: str) -> dict[str, Any]:
        raise NotImplementedError
