from fastapi import Depends, logger
from app.core.dependencies.database import get_db
from app.core.dependencies.middleware.get_available_user import get_available_user
from app.core.dependencies.middleware.get_current_user import get_current_user
from app.core.domain.entities.user import User
from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.core.infra.repositories.user_repository import UserRepository
from app.modules.auth.domain.request.login_request import LoginRequest
from app.modules.auth.domain.response.token_response import TokenResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.domain.usecases.login_use_case import LoginUseCase
from app.modules.auth.infra.services.argon2_hasher import Argon2PasswordHasher
from app.modules.auth.infra.services.jwt_service import JWTService


class AuthController:
    def __init__(self) -> None:
        pass

    async def login(
        self,
        login_request: LoginRequest,
        user: User = Depends(get_available_user),
        db: AsyncSession = Depends(get_db),
    ) -> TokenResponse:
        user_repository = UserRepository(db)
        jwt_token_service = JWTService()
        password_service = Argon2PasswordHasher()

        if user:
            raise LibraryException(
                status_code=409,
                code=ErrorCode.DUPLICATE_ENTRY,
                msg="You are already logged in, you don't need to login again.",
            )

        try:
            login_use_case = LoginUseCase(
                user_repository=user_repository,
                token_service=jwt_token_service,
                password_service=password_service,
            )
            token = await login_use_case.execute(
                login_request.email, login_request.password
            )

            return TokenResponse(token=token)
        except ValueError as e:
            logger.logger.error(e)
            raise LibraryException(
                status_code=403,
                code=ErrorCode.INSUFFICIENT_PERMISSION,
                msg=f"Invalid Credentials",
                fields=["email", "password"],
            )

    async def google_login(
        self,
    ) -> TokenResponse:
        # TODO(aashutosh): SSO Login
        raise NotImplementedError("Google Login will be implemented soon")

    async def handle_me(self, user: User = Depends(get_current_user)) -> User:
        return user
