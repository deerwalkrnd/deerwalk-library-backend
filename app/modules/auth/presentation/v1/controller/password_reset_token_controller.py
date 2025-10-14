from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.background.tasks.email_task import send_reset_password_email_task
from app.core.dependencies.database import get_db
from app.core.dependencies.get_settings import get_settings
from app.core.domain.entities.user import UserWithPassword
from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.core.infra.repositories.user_repository import UserRepository
from app.modules.auth.domain.request.password_reset_token_request import (
    PasswordResetTokenRequest,
)
from app.modules.auth.domain.request.reset_password_request import ResetPasswordRequest
from app.modules.auth.domain.response.forgot_password_response import (
    ForgotPasswordResponse,
)
from app.modules.auth.domain.response.reset_password_response import (
    ResetPasswordResponse,
)
from app.modules.auth.domain.usecases.create_password_reset_token_use_case import (
    CreatePasswordResetTokenUseCase,
)
from app.modules.auth.domain.usecases.get_password_reset_token_by_hash_use_case import (
    GetPasswordResetTokenByHashUseCase,
)
from app.modules.auth.infra.password_reset_token_repository import (
    PasswordResetTokenRepository,
)
from app.modules.auth.infra.services.argon2_hasher import Argon2PasswordHasher
from app.modules.auth.utils.generate_url_safe_token import generate_url_safe_token
from app.modules.auth.utils.generate_url_safe_token_expiry import (
    generate_url_safe_token_expiry,
)
from app.modules.auth.utils.validate_password_reset_token import (
    validate_password_reset_token,
)
from app.modules.users.domain.usecases.get_user_by_email_use_case import (
    GetUserByEmailUseCase,
)
from app.modules.users.domain.usecases.get_user_by_uuid_use_case import (
    GetUserByUUIDUseCase,
)
from app.modules.users.domain.usecases.update_users_by_uuid_use_case import (
    UpdateUsersByUUIDUseCase,
)


class PasswordResetController:
    def __init__(self) -> None:
        pass

    async def forgot_password(
        self,
        password_reset_token_request: PasswordResetTokenRequest,
        db: AsyncSession = Depends(get_db),
    ) -> ForgotPasswordResponse:
        settings = get_settings()
        password_reset_token_repository = PasswordResetTokenRepository(db=db)
        user_repository = UserRepository(db=db)

        get_user_by_email_use_case = GetUserByEmailUseCase(
            user_repository=user_repository
        )
        create_password_reset_token_use_case = CreatePasswordResetTokenUseCase(
            password_reset_token_repository=password_reset_token_repository
        )

        user = await get_user_by_email_use_case.execute(
            email=password_reset_token_request.email
        )

        if user and user.uuid and user.name:
            token = await generate_url_safe_token()
            expires_at = await generate_url_safe_token_expiry()

            _ = await create_password_reset_token_use_case.execute(
                user_id=user.uuid, token=token, token_expiry=expires_at
            )

            password_reset_link = (
                f"{settings.frontend_url}/auth/reset-password?token={token}"
            )

            send_reset_password_email_task.delay(
                to=user.email, password_reset_url=password_reset_link, name=user.name
            )

        return ForgotPasswordResponse(
            message="a password reset email is sent if the email is registered!"
        )

    async def reset_password(
        self,
        token: str,
        reset_password_request: ResetPasswordRequest,
        db: AsyncSession = Depends(get_db),
    ) -> ResetPasswordResponse | None:
        password_reset_token_repository = PasswordResetTokenRepository(db=db)
        user_repository = UserRepository(db=db)
        get_password_reset_token_by_hash_use_case = GetPasswordResetTokenByHashUseCase(
            password_reset_token_repository=password_reset_token_repository
        )
        update_user_by_uuid_use_case = UpdateUsersByUUIDUseCase(
            user_repository=user_repository
        )
        get_user_by_uuid_use_case = GetUserByUUIDUseCase(
            user_repository=user_repository
        )

        password_reset_token = await get_password_reset_token_by_hash_use_case.execute(
            token=token
        )

        if not password_reset_token:
            raise LibraryException(
                status_code=404, code=ErrorCode.NOT_FOUND, msg="Token does not exist"
            )

        validated = await validate_password_reset_token(
            token=token, token_entity=password_reset_token
        )

        if validated and password_reset_token.user_id:
            user = await get_user_by_uuid_use_case.execute(
                uuid=password_reset_token.user_id
            )

            pwd_service = Argon2PasswordHasher()
            reset_password_request.new_password = await pwd_service.hash_password(
                reset_password_request.new_password
            )

            new_data = UserWithPassword(password=reset_password_request.new_password)

            await update_user_by_uuid_use_case.execute(
                conditions=UserWithPassword(uuid=user.uuid), new=new_data
            )

            return ResetPasswordResponse(message="password reset successfully!")
