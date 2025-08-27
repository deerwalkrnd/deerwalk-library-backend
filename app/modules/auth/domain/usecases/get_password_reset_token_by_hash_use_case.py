from app.modules.auth.domain.entity.password_reset_token import PasswordResetToken
from app.modules.auth.domain.repository.password_reset_token_repository_interface import (
    PasswordResetTokenRepositoryInterface,
)


class GetPasswordResetTokenByHashUseCase:
    def __init__(
        self, password_reset_token_repository: PasswordResetTokenRepositoryInterface
    ):
        self.password_reset_token_repository = password_reset_token_repository

    async def execute(self, token: str) -> None | PasswordResetToken:
        password_reset_token = await self.password_reset_token_repository.find_one(
            obj=PasswordResetToken(token=token)
        )

        if password_reset_token:
            return password_reset_token

        return None
