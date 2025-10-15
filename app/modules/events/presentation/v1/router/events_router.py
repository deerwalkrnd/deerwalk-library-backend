from fastapi import APIRouter

from app.modules.events.presentation.v1.controller.events_controller import (
    EventsController,
)

router = APIRouter(prefix="/events", tags=["events"])
events_controller = EventsController()

router.add_api_route(
    path="/",
    methods=["POST"],
    endpoint=events_controller.create_event,
    response_description="201 if event created else error",
)

router.add_api_route(
    path="/latest",
    methods=["GET"],
    endpoint=events_controller.get_latest_event,
    response_description="get latest event or not found error",
)

router.add_api_route(
    path="/{id}",
    methods=["GET"],
    endpoint=events_controller.get_one_event,
    response_description="gets one events, specified by the id",
)


router.add_api_route(
    path="/{id}",
    methods=["DELETE"],
    endpoint=events_controller.delete_event,
    response_description="returns 200 when deleted, otherwise error",
)

router.add_api_route(
    path="/",
    methods=["GET"],
    endpoint=events_controller.get_many_events,
    response_description="returns paginated response of all available events",
)

router.add_api_route(
    path="/{id}",
    methods=["PUT"],
    endpoint=events_controller.update_event,
    response_description="updates event by id."
)
