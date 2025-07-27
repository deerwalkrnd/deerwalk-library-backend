from abc import ABC, abstractmethod
from typing import Optional


class FileServiceInterface(ABC):
    @abstractmethod
    async def save(
        self, file_path: str, body: bytes, content_type: Optional[str]
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, file_path: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def get(self, file_path: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def exists(self, file_path: str) -> str:
        raise NotImplementedError
