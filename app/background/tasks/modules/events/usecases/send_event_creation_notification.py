import asyncio
from datetime import datetime
from typing import Any, Coroutine, List
from app.core.dependencies.database import get_db
from app.core.dependencies.get_smtp import get_smtp
from app.core.domain.repositories.user_repository_interface import (
    UserRepositoryInterface,
)
from app.core.infra.repositories.user_repository import UserRepository
from app.core.infra.services.email_notification_service import EmailNotificationService
from app.core.utils.make_email import create_email
from app.modules.events.domain.templates.new_event_template import (
    get_new_event_template,
)
from app.modules.users.domain.usecases.get_all_students_use_case import (
    GetAllStudentsUseCase,
)


class SendEventCreationNotificationUseCase:
    def __init__(
        self,
    ) -> None:
        pass

    async def execute(self, event_name: str, event_date: datetime, from_email: str):

        self.db = await get_db().__anext__()
        self.user_repository: UserRepositoryInterface = UserRepository(db=self.db)
        self.email_service = EmailNotificationService(await get_smtp())

        get_all_students_use_case = GetAllStudentsUseCase(
            user_repository=self.user_repository
        )

        all_students = await get_all_students_use_case.execute()

        email_promises: List[Coroutine[Any, Any, None]] = []

        for student in all_students:
            if not student.name:
                student.name = "Student"

            if not student.email:
                continue

            new_event_tempelate = await get_new_event_template(
                event_name=event_name, event_date=event_date, name=student.name
            )

            subject = f"New Event Added | {event_name}"

            email_object = await create_email(
                to=student.email,
                subject=subject,
                html=new_event_tempelate,
                _from=from_email,
            )

            print("sending email to: ", email_object)

            t = self.email_service.send_email(message=email_object)
            email_promises.append(t)

        await asyncio.gather(*email_promises)
