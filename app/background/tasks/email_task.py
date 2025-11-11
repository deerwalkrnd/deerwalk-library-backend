import asyncio
from typing import Any

from celery import Task
from fastapi.logger import logger
from datetime import datetime

from app.background.celery_app import celery_app
from app.background.tasks.modules.events.usecases.send_event_creation_notification import (
    SendEventCreationNotificationUseCase,
)
from app.core.dependencies.database import get_db
from app.core.dependencies.get_smtp import get_smtp
from app.core.infra.services.email_notification_service import EmailNotificationService
from app.core.utils.make_email import create_email
from app.modules.auth.domain.templates.password_reset_template import (
    get_password_reset_template,
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.auth.domain.templates.welcome_template import get_welcome_template


class EmailTask(Task):  # type: ignore
    """Base Task to deal with email things
    The implementations need both smtp object and the email_service to work.
    """

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.run(*args, **kwds)  # type:ignore

    def get_email_service(self):
        smtp = asyncio.run(get_smtp())
        return EmailNotificationService(smtp=smtp)

    def get_db(self) -> AsyncSession:
        db = asyncio.run(get_db().__anext__())
        return db


@celery_app.task(bind=True, base=EmailTask, name="send_welcome_email")
def send_welcome_email_task(self: EmailTask, email: str, name: str = "User") -> None:
    try:
        email_service: EmailNotificationService = self.get_email_service()

        html_content = asyncio.run(get_welcome_template(name=name))

        email_obj = asyncio.run(
            create_email(
                html=html_content,
                subject="Welcome to Deerwalk Library",
                _from="Deerwalk Library <library@deerwalk.edu.np>",
                to=email,
            )
        )

        asyncio.run(email_service.send_email(email_obj))

        return None
    except Exception as e:
        logger.error(e)
        self.retry(exc=e, countdown=60 * (2**self.request.retries), max_retries=3)


@celery_app.task(bind=True, base=EmailTask, name="send_reset_password_email")
def send_reset_password_email_task(
    self: EmailTask,
    to: str,
    password_reset_url: str,
    name: str,
    from_email: str = "Deerwalk Library <library@deerwalk.edu.np>",
) -> None:
    try:
        email_service = self.get_email_service()

        password_reset_template = asyncio.run(
            get_password_reset_template(
                name=name,
                password_reset_link=password_reset_url,
            )
        )

        email_object = asyncio.run(
            create_email(
                to=to,
                html=password_reset_template,
                subject="Reset Your Password",
                _from=from_email,
            )
        )

        asyncio.run(email_service.send_email(email_object))
    except Exception as e:
        print(f"Failed to send email to {to}: {str(e)}")
        self.retry(exc=e, countdown=60 * (2**self.request.retries), max_retries=3)


# TODO(aashutosh): create a bulk email sending class which sends email in bulk for upcoming book returns


@celery_app.task(bind=True, base=EmailTask, name="send_new_event_email")
def send_new_event_email_task(
    self: EmailTask,
    event_name: str,
    event_date: datetime,
    from_email: str = "Deerwalk Library <library@deerwalk.edu.np>",
):
    send_email_creation_notification_use_case = SendEventCreationNotificationUseCase()

    asyncio.run(
        send_email_creation_notification_use_case.execute(
            event_name=event_name, event_date=event_date, from_email=from_email
        )
    )
