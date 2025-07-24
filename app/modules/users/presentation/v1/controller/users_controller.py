from typing import List
from fastapi import Depends
from app.core.domain.entities.user import User
from app.modules.users.domain.request.user_list_request import UserSearchRequest


class UsersController:
    async def get_all_with_search_pagination_and_filter(
        self, params: UserSearchRequest = Depends()
    ) -> List[User]:

        return []
