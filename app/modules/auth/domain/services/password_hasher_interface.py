from abc import ABC, abstractmethod


class PasswordHasherInterface(ABC):
    @abstractmethod
    async def hash_password(self, password: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def compare_password(self, password: str, hash: str) -> bool:
        raise NotImplementedError
