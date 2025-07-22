import asyncio
from typing import Any, AsyncGenerator
from app.core.dependencies.database import get_db
from app.core.dependencies.get_settings import get_settings
from app.core.domain.entities.user import UserWithPassword
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.infra.repositories.user_repository import UserRepository
from app.core.models.users import UserRole
from app.modules.auth.infra.services.argon2_hasher import Argon2PasswordHasher


async def seed_admin(user: UserWithPassword) -> UserWithPassword:
    database: AsyncGenerator[AsyncSession, Any] = get_db()
    db: AsyncSession = await database.__anext__()

    password_hasher = Argon2PasswordHasher()
    user_repository = UserRepository(db=db)

    if not user.password:
        raise ValueError("password is required for this user type to be added")

    user.password = await password_hasher.hash_password(user.password)
    created = await user_repository.create(user)

    print(f"Admin Created with data {created=}")

    return user


if __name__ == "__main__":

    settings = get_settings()

    admin = UserWithPassword(
        name="Deerwalk Library",
        email=settings.admin_email,
        password=settings.admin_password,
        role=UserRole.LIBRARIAN,
    )
    asyncio.run(seed_admin(admin))
