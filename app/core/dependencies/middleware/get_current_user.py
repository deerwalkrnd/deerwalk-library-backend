from typing import Any

from fastapi import Depends, Request, logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.database import get_db
from app.core.domain.entities.user import User, UserWithPassword
from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.core.infra.repositories.user_repository import UserRepository
from app.modules.auth.infra.services.jwt_service import JWTService


async def get_current_user(
    request: Request, db: AsyncSession = Depends(get_db)
) -> User:
    token_header = request.headers.get("Authorization")
    if not token_header:
        raise LibraryException(
            code=ErrorCode.INVALID_FIELDS,
            fields=["Authorization Header"],
            msg="Missing Authorization Headers",
            status_code=401,
        )

    splitted = token_header.split(" ")

    if len(splitted) != 2 and splitted[0] != "Bearer":
        raise LibraryException(
            code=ErrorCode.INVALID_FIELDS,
            fields=["Authorization Header"],
            msg="Missing Authorization Headers",
            status_code=401,
        )

    jwt_token = splitted[1]

    token_service = JWTService()

    user_repository = UserRepository(db=db)
    data: dict[str, Any] = {}

    try:
        data = await token_service.decode(jwt_token)
    except Exception as e:
        logger.logger.error(e)
        raise LibraryException(
            code=ErrorCode.INVALID_FIELDS,
            fields=["Authorization Header"],
            msg="Invalid JWT Data",
            status_code=401,
        )

    uuid = data.get("sub")

    if not uuid:
        raise LibraryException(
            code=ErrorCode.INVALID_FIELDS,
            fields=["Authorization Header"],
            msg="Missing Authorization Headers",
            status_code=401,
        )

    user: UserWithPassword | None = await user_repository.find_one(
        obj=UserWithPassword(uuid=uuid)
    )

    if not user:
        raise LibraryException(
            code=ErrorCode.INVALID_FIELDS,
            fields=["Authorization Header"],
            msg="Missing Authorization Headers",
            status_code=401,
        )

    return User.model_validate(user)
