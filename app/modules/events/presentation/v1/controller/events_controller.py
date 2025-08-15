from fastapi import Depends
from fastapi.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies.database import get_db
from app.core.dependencies.middleware.get_current_librarian import get_current_librarian
from app.core.domain.entities.user import User
from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.modules.events.domain.entities.event import Event
from app.modules.events.domain.request.create_event_request import CreateEventRequest
from app.modules.events.domain.usecase.create_event_use_case import CreateEventUseCase
from app.modules.events.infra.repository.event_repository import EventRepository


class EventsController:
    def __init__(self) -> None:
        pass

    async def create_event(
        self,
        create_event_request: CreateEventRequest,
        _: User = Depends(get_current_librarian),
        db: AsyncSession = Depends(get_db),
    ) -> Event:
        event_repository = EventRepository(db=db)

        try:
            create_event_use_case = CreateEventUseCase(
                event_repository=event_repository
            )
            created = await create_event_use_case.execute(
                create_event_request.name,
                create_event_request.description,
                create_event_request.image_url,
                create_event_request.event_date,
            )

            if not created:
                raise LibraryException(
                    status_code=400,
                    code=ErrorCode.INVALID_FIELDS,
                    msg="unable to create event",
                )

            return created
        except Exception as e:
            logger.error(e)
            raise LibraryException(
                status_code=500,
                code=ErrorCode.UNKOWN_ERROR,
                msg="Unable to create error ",
            )
