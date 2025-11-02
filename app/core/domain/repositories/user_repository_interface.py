from abc import abstractmethod
from app.core.domain.entities.user import UserWithPassword
from app.core.domain.repositories.repository_interface import RepositoryInterface


class UserRepositoryInterface(RepositoryInterface[UserWithPassword]):
    @abstractmethod
    async def get_students_count(
        self,
    ) -> int:
        raise NotImplementedError
