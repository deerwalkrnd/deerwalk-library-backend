from abc import abstractmethod

from app.core.domain.repositories.repository_interface import RepositoryInterface
from app.modules.auth.domain.entities.password_reset_token import PasswordResetToken


class PasswordResetTokenRepositoryInterface(RepositoryInterface[PasswordResetToken]):
    @abstractmethod
    async def find_one_by_user_id(self, user_id: str) -> PasswordResetToken | None:
        raise NotImplementedError
