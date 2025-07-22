from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app.modules.auth.domain.services.password_hasher_interface import (
    PasswordHasherInterface,
)


class Argon2PasswordHasher(PasswordHasherInterface):
    def __init__(self) -> None:
        self.hasher = PasswordHasher()

    async def hash_password(self, password: str) -> str:
        return self.hasher.hash(password)

    async def compare_password(self, password: str, hash: str) -> bool:
        try:
            return self.hasher.verify(hash, password)
        except VerifyMismatchError:
            return False
