from typing import Dict
from fastapi import Depends, logger
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
from datetime import datetime, timedelta

from app.core.dependencies.database import get_db
from app.core.dependencies.get_settings import get_settings
from app.core.dependencies.middleware.get_available_user import get_available_user
from app.core.dependencies.middleware.get_current_user import get_current_user
from app.core.domain.entities.user import User, UserWithPassword
from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.core.infra.repositories.user_repository import UserRepository
from app.modules.auth.domain.request.login_request import LoginRequest
from app.modules.auth.domain.request.sso_url_request import SSOURLRequest
from app.modules.auth.domain.response.token_response import TokenResponse
from app.modules.auth.domain.response.url_response import URLResponse
from app.modules.auth.domain.usecases.generate_jwt_token_use_case import (
    GenerateJWTTokenUseCase,
)
from app.modules.auth.domain.usecases.get_sso_login_url_use_case import (
    GetSSOLoginURLUseCase,
)
from app.modules.auth.domain.usecases.get_user_information_from_code_use_case import (
    GetUserInformationFromCodeUseCase,
)
from app.modules.auth.domain.usecases.login_use_case import LoginUseCase
from app.modules.auth.infra.services.argon2_hasher import Argon2PasswordHasher
from app.modules.auth.infra.services.jwt_service import JWTService
from app.modules.users.domain.usecases.create_user_from_google_use_case import CreateUserFromGoogleUseCase
from app.modules.users.domain.usecases.get_user_by_email_use_case import (
    GetUserByEmailUseCase,
)
from app.modules.users.domain.usecases.update_users_by_uuid_use_case import (
    UpdateUsersByUUIDUseCase,
)


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

    async def handle_google_callback(
        self, code: str, db: AsyncSession = Depends(get_db)
    ) -> TokenResponse:
        config = get_settings()

        async with httpx.AsyncClient() as client:
            get_user_information_from_code_use_case = GetUserInformationFromCodeUseCase(
                client=client,
                client_id=config.google_client_id,
                redirect_url=config.google_redirect_url,
                client_secret=config.google_client_secret,
            )
            try:
                user_information = (
                    await get_user_information_from_code_use_case.execute(code)
                )
            except ValueError as e:
                raise LibraryException(
                    status_code=408,
                    code=ErrorCode.TOKEN_EXPIRED,
                    msg="underlying google api timed out ;" + str(e),
                )


        if user_information.email and not user_information.email.endswith(
            ".deerwalk.edu.np"
        ):
            raise LibraryException(
                status_code=403,
                code=ErrorCode.INSUFFICIENT_PERMISSION,
                msg="only deerwalk students can use this api",
            )

        user_repository = UserRepository(db=db)

        get_user_by_email_use_case = GetUserByEmailUseCase(
            user_repository=user_repository
        )

        if not user_information.email:
            raise ValueError("never reaching here")

        token_service = JWTService()
        generate_jwt_use_case = GenerateJWTTokenUseCase(token_service=token_service)

        try:
            user = await get_user_by_email_use_case.execute(user_information.email)

            update_user_by_uuid_use_case = UpdateUsersByUUIDUseCase(
                user_repository=user_repository
            )
            await update_user_by_uuid_use_case.execute(
                conditions=UserWithPassword(uuid=user.uuid),
                new=UserWithPassword.model_validate(user),
            )


            data: Dict[str, datetime | str | None] = {
                "sub": user.uuid,
                "exp": datetime.now() + timedelta(days=2),
            }

            token: str = await generate_jwt_use_case.execute(payload=data)

            return TokenResponse(token=token)

            # user exists in the db, update new data and send back token
        except ValueError as e:
            # user does not exist in the db, create new entity and create a token and send back

            create_user_use_case = CreateUserFromGoogleUseCase(user_repository=user_repository)

            created = await create_user_use_case.execute(user_information)

            data : Dict[str, datetime | str | None] = {
                "sub": created.uuid,
                "exp": datetime.now() + timedelta(days=2)
            }

            token = await generate_jwt_use_case.execute(payload=data)

            return TokenResponse(token=token)

    async def handle_me(self, user: User = Depends(get_current_user)) -> User:
        return user

    async def handle_sso_login(self, sso: SSOURLRequest = Depends()) -> URLResponse:
        try:
            sso_url_use_case = GetSSOLoginURLUseCase()
            url = await sso_url_use_case.execute(sso.provider)
            return URLResponse(url=url)
        except ValueError:
            raise LibraryException(
                status_code=404,
                code=ErrorCode.NOT_FOUND,
                msg="such sso login not found",
            )
