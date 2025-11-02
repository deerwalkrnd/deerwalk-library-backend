from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, func, select
from app.core.domain.entities.user import UserWithPassword
from app.core.domain.repositories.user_repository_interface import (
    UserRepositoryInterface,
)
from app.core.infra.repositories.repository import Repository
from app.core.models.users import UserModel, UserRole


class UserRepository(Repository[UserModel, UserWithPassword], UserRepositoryInterface):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, model=UserModel, entity=UserWithPassword)

    async def get_students_count(self) -> int:
        query = select(func.count(self.model.uuid)).where(
            and_(self.model.deleted == False, self.model.role == UserRole.STUDENT)
        )
        result = await self.db.execute(query)
        students_count = result.scalar() or 0
        return students_count
