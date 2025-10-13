from datetime import datetime

from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.modules.auth.domain.entity.password_reset_token import PasswordResetToken


async def validate_password_reset_token(
    token: str,
    token_entity: PasswordResetToken,
) -> bool:
    if not token_entity.token:
        raise LibraryException(
            status_code=404,
            code=ErrorCode.NOT_FOUND,
            msg="password reset token not found.",
        )

    if token_entity.token != token:
        raise LibraryException(
            status_code=401,
            code=ErrorCode.INSUFFICIENT_PERMISSION,
            msg="Invalid password reset token.",
        )

    if token_entity.expires_at and token_entity.expires_at < datetime.now():
        raise LibraryException(
            status_code=401,
            code=ErrorCode.TOKEN_EXPIRED,
            msg="password reset token has expired.",
        )

    return True
