from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies.database import get_db
from app.core.domain.entities.response.paginated_response import PaginatedResponseMany
from app.core.domain.entities.user import User
from app.core.infra.repositories.user_repository import UserRepository
from app.modules.users.domain.request.user_list_request import UserSearchRequest
from app.modules.users.domain.usecases.get_many_users_use_case import (
    GetManyUsersUseCase,
)


class UsersController:
    async def list_many_users(
        self, db: AsyncSession = Depends(get_db), params: UserSearchRequest = Depends()
    ) -> PaginatedResponseMany[User]:
        # TODO(aashutosh) make this response PaginationResponse(page, items, total and next)
        user_repository = UserRepository(db=db)

        get_many_users_use_case = GetManyUsersUseCase(user_repository=user_repository)

        users = await get_many_users_use_case.execute(
            page=params.page,
            limit=params.limit,
            searchable_field="name",
            searchable_value=params.searchable,
            starts=params.starts,
            ends=params.ends,
        )

        return PaginatedResponseMany(
            page=params.page, total=len(users), next=params.page + 1, items=users
        )
