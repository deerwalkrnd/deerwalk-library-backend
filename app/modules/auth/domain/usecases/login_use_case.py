from datetime import datetime, timedelta

from app.core.domain.entities.user import User
from app.core.infra.repositories.user_repository import UserRepository
from app.modules.auth.domain.services.password_hasher_interface import (
    PasswordHasherInterface,
)
from app.modules.auth.domain.services.token_service_interface import (
    TokenServiceInterface,
)


class LoginUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        token_service: TokenServiceInterface,
        password_service: PasswordHasherInterface,
    ) -> None:
        self.user_repository = user_repository
        self.token_service = token_service
        self.password_service = password_service

    async def execute(self, email: str, password: str) -> str:
        user = await self.user_repository.find_one(obj=User(email=email))
        if not user or not user.password:
            raise ValueError("user does not exist")
        is_correct = await self.password_service.compare_password(
            password=password, hash=user.password
        )

        if not is_correct:
            raise ValueError("credentials are invalid")

        token = await self.token_service.encode(
            {"sub": user.uuid, "exp": datetime.now() + timedelta(days=2)}
        )

        return token
