from datetime import datetime

from app.modules.auth.domain.entity.password_reset_token import PasswordResetToken
from app.modules.auth.domain.repository.password_reset_token_repository_interface import (
    PasswordResetTokenRepositoryInterface,
)


class CreatePasswordResetTokenUseCase:
    def __init__(
        self, password_reset_token_repository: PasswordResetTokenRepositoryInterface
    ) -> None:
        self.password_reset_token_repository = password_reset_token_repository

    async def execute(
        self, user_id: str, token: str, token_expiry: datetime
    ) -> PasswordResetToken | None:
        password_reset_token = await self.password_reset_token_repository.create(
            obj=PasswordResetToken(
                user_id=user_id, token=token, expires_at=token_expiry
            )
        )
        return password_reset_token
