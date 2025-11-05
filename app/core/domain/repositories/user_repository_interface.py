from abc import abstractmethod
from typing import List
from app.core.domain.entities.user import User, UserWithPassword
from app.core.domain.repositories.repository_interface import RepositoryInterface


class UserRepositoryInterface(RepositoryInterface[UserWithPassword]):
    @abstractmethod
    async def get_students_count(
        self,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_all_students(self) -> List[User]:
        raise NotImplementedError
