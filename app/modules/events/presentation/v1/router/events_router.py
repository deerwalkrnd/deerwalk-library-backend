from fastapi import APIRouter

from app.modules.events.presentation.v1.controller.events_controller import (
    EventsController,
)

router = APIRouter(prefix="/events")
events_controller = EventsController()

router.add_api_route(
    path="/",
    methods=["POST"],
    endpoint=events_controller.create_event,
    response_description="201 if event created else error",
)
