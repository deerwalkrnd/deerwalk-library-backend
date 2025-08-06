from aiosmtplib import SMTP
from fastapi import BackgroundTasks, Depends, logger
from app.core.dependencies.database import get_db
from app.core.dependencies.get_settings import get_settings
from app.core.dependencies.get_smtp import get_smtp
from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.core.infra.repositories.user_repository import UserRepository
from app.core.infra.services.email_notification_service import EmailNotificationService
from app.core.utils.make_email import create_email
from app.modules.auth.domain.request.forgot_passoword_request import (
    ForgotPasswordRequest,
)
from app.modules.auth.domain.templates.forgot_password_template import (
    get_forgot_password_template,
)
from app.modules.auth.infra.services.jwt_service import JWTService
from app.modules.users.domain.usecases.get_user_by_email_use_case import (
    GetUserByEmailUseCase,
)
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta


class ForgotPasswordController:
    def __init__(self):
        pass

    async def forgot_password(
        self,
        forgot_password_request: ForgotPasswordRequest,
        background_tasks: BackgroundTasks,
        smtp: SMTP = Depends(get_smtp),
        db: AsyncSession = Depends(get_db),
    ):
        try:
            user_repository = UserRepository(db=db)
            get_user_by_email_use_case = GetUserByEmailUseCase(
                user_repository=user_repository
            )

            user = await get_user_by_email_use_case.execute(
                email=forgot_password_request.email
            )

            if not user:
                raise LibraryException(
                    status_code=404,
                    code=ErrorCode.NOT_FOUND,
                    msg="User with that email does not exists",
                )

            token_service = JWTService()

            settings = get_settings()
            secret_token = await token_service.encode(
                payload={
                    "sub": user.email,
                    "exp": datetime.now() + timedelta(minutes=15),
                }
            )
            forgot_url_link = f"{settings.frontend_url}/{secret_token}"

            email_notification_service = EmailNotificationService(smtp=smtp)

            html_content = await get_forgot_password_template(link=forgot_url_link)

            email = await create_email(
                to=f"{user.email}",
                subject="Password Reset Request",
                _from="Deerwalk Library <nepalidude3@gmail.com>",
                html=html_content,
            )

            background_tasks.add_task(email_notification_service.send_email, email)
            return None

        except Exception as e:
            logger.logger.error(e)
            raise LibraryException(
                status_code=500,
                code=ErrorCode.UNKOWN_ERROR,
                msg="could not reset password.",
            )
