from typing import Any

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.database import get_db
from app.core.domain.entities.user import User, UserWithPassword
from app.core.infra.repositories.user_repository import UserRepository
from app.modules.auth.infra.services.jwt_service import JWTService


async def get_available_user(
    request: Request, db: AsyncSession = Depends(get_db)
) -> User | None:
    token_header = request.headers.get("Authorization")
    if not token_header:
        return None

    splitted = token_header.split(" ")

    if len(splitted) != 2 and splitted[0] != "Bearer":
        return None

    jwt_token = splitted[1]

    token_service = JWTService()

    user_repository = UserRepository(db=db)

    data: dict[str, Any] = await token_service.decode(jwt_token)

    uuid = data.get("sub")

    if not uuid:
        return None

    user: UserWithPassword | None = await user_repository.find_one(
        obj=UserWithPassword(uuid=uuid)
    )

    if not user:
        return None

    return User.model_validate(user)
