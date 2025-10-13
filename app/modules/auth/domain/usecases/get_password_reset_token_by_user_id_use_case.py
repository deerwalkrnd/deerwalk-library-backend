from app.modules.auth.domain.entity.password_reset_token import \
    PasswordResetToken
from app.modules.auth.domain.repository.password_reset_token_repository_interface import \
    PasswordResetTokenRepositoryInterface


class GetPasswordResetTokenByUserIdUseCase:
    def __init__(
        self, password_reset_token_repository: PasswordResetTokenRepositoryInterface
    ):
        self.password_reset_token_repository = password_reset_token_repository

    async def execute(self, user_id: str) -> PasswordResetToken | None:
        return await self.password_reset_token_repository.find_one_by_user_id(
            user_id=user_id
        )
