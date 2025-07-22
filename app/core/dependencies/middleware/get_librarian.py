from typing import Annotated

from fastapi import Depends

from app.core.dependencies.middleware.get_current_user import get_current_user
from app.core.domain.entities.user import User
from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.core.models.users import UserRole


async def get_current_librarian(user: Annotated[User, Depends(get_current_user)]):
    if user.role != UserRole.LIBRARIAN:
        raise LibraryException(
            status_code=403,
            code=ErrorCode.INSUFFICIENT_PERMISSION,
            msg="You need to be a Librarian to access this resource.",
        )
    return user
