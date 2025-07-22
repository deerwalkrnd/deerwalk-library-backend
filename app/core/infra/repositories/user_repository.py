from sqlalchemy.ext.asyncio import AsyncSession

from app.core.domain.entities.user import UserWithPassword
from app.core.domain.repositories.user_repository_interface import \
    UserRepositoryInterface
from app.core.infra.repositories.repository import Repository
from app.core.models.users import UserModel


class UserRepository(Repository[UserModel, UserWithPassword], UserRepositoryInterface):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, model=UserModel, entity=UserWithPassword)
