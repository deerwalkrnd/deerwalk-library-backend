from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.infra.repositories.repository import Repository
from app.core.models.password_reset_token import PasswordResetTokenModel
from app.modules.auth.domain.entity.password_reset_token import PasswordResetToken
from app.modules.auth.domain.repository.password_reset_token_repository_interface import (
    PasswordResetTokenRepositoryInterface,
)


class PasswordResetTokenRepository(
    Repository[PasswordResetTokenModel, PasswordResetToken],
    PasswordResetTokenRepositoryInterface,
):
    def __init__(self, db: AsyncSession):
        super().__init__(
            db=db, model=PasswordResetTokenModel, entity=PasswordResetToken
        )

    async def find_one_by_user_id(self, user_id: str) -> PasswordResetToken | None:
        now = datetime.now()
        query = (
            select(self.model)
            .where(self.model.user_id == user_id, self.model.token_expiry > now)
            .order_by(self.model.created_at.desc())
            .limit(1)
        )

        result = await self.db.execute(query)
        token_model = result.scalar_one_or_none()

        if token_model:
            return PasswordResetToken(
                id=token_model.id,
                user_id=token_model.user_id,
                token=token_model.token,
                token_expiry=token_model.token_expiry,
            )
        return None
