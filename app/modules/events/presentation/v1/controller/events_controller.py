from datetime import timedelta, datetime
from fastapi import Depends
from fastapi.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies.database import get_db
from app.core.domain.entities.response.paginated_response import PaginatedResponseMany
from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.modules.events.domain.entities.event import Event
from app.modules.events.domain.request.create_event_request import CreateEventRequest
from app.modules.events.domain.request.get_many_event_params_request import (
    GetManyEventParams,
)
from app.modules.events.domain.request.update_event_request import UpdateEventRequest
from app.modules.events.domain.usecase.create_event_use_case import CreateEventUseCase
from app.modules.events.domain.usecase.delete_event_by_id_use_case import (
    DeleteEventByIdUseCase,
)
from app.modules.events.domain.usecase.get_event_by_id_use_case import (
    GetEventByIdUseCase,
)
from app.modules.events.domain.usecase.get_many_events_use_case import (
    GetManyEventsUseCase,
)
from app.modules.events.domain.usecase.update_event_by_id_use_case import (
    UpdateEventByIdUseCase,
)
from app.modules.events.infra.repository.event_repository import EventRepository


class EventsController:
    def __init__(self) -> None:
        pass

    async def create_event(
        self,
        create_event_request: CreateEventRequest,
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
                create_event_request.event_date.replace(tzinfo=None),
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

    async def get_one_event(self, id: int, db: AsyncSession = Depends(get_db)) -> Event:
        event_repository = EventRepository(db=db)
        get_event_by_id_use_case = GetEventByIdUseCase(
            event_repository=event_repository
        )

        try:
            e = await get_event_by_id_use_case.execute(id=id)
            return e
        except ValueError as e:
            raise LibraryException(
                status_code=404, code=ErrorCode.NOT_FOUND, msg=str(e)
            )

    async def delete_event(self, id: int, db: AsyncSession = Depends(get_db)) -> None:
        event_repository = EventRepository(db)

        get_event_by_id_use_case = GetEventByIdUseCase(
            event_repository=event_repository
        )

        try:
            e = await get_event_by_id_use_case.execute(id)

            delete_event_by_id_use_case = DeleteEventByIdUseCase(
                event_repository=event_repository
            )

            await delete_event_by_id_use_case.execute(id)

        except ValueError as e:
            raise LibraryException(
                status_code=404, code=ErrorCode.NOT_FOUND, msg=str(e)
            )

    async def get_many_events(
        self, params: GetManyEventParams = Depends(), db: AsyncSession = Depends(get_db)
    ) -> PaginatedResponseMany[Event]:
        event_repository = EventRepository(db=db)

        get_many_events_use_case = GetManyEventsUseCase(
            event_repository=event_repository
        )

        if not params.starts or not params.ends:
            params.starts = datetime.now() - timedelta(days=30)
            params.ends = datetime.now() + timedelta(days=5)


        events = await get_many_events_use_case.execute(
            params.page,
            params.limit,
            params.starts,
            params.ends,
        )

        return PaginatedResponseMany(
            page=params.page, next=params.page + 1, items=events, total=len(events)
        )

    async def update_event(
        self,
        id: int,
        update_event_request: UpdateEventRequest,
        db: AsyncSession = Depends(get_db),
    ) -> None:
        event_repository = EventRepository(db=db)

        get_event_by_id_use_case = GetEventByIdUseCase(
            event_repository=event_repository
        )

        try:
            await get_event_by_id_use_case.execute(id)

            update_event_by_id_use_case = UpdateEventByIdUseCase(
                event_repository=event_repository
            )
            to_update = Event(**update_event_request.model_dump(exclude_unset=True))

            await update_event_by_id_use_case.execute(id, to_update)

        except ValueError as e:
            raise LibraryException(
                status_code=404,
                code=ErrorCode.NOT_FOUND,
                msg="event not found " + str(e),
            )

        pass
