from fastapi import APIRouter

from app.modules.feedbacks.presentation.v1.controller.feedback_controller import (
    FeedbackController,
)

router = APIRouter(prefix="/feedbacks", tags=["feedbacks"])

feedback_controller = FeedbackController()

router.add_api_route(
    path="",
    endpoint=feedback_controller.list_feedbacks,
    methods=["GET"],
    description="get a list of all feedbacks.",
)

router.add_api_route(
    path="",
    endpoint=feedback_controller.create_feedback,
    methods=["POST"],
    description="create a feedback.",
)

router.add_api_route(
    path="/{id}",
    endpoint=feedback_controller.update_feedbacks,
    methods=["PUT"],
    description="update a feedback.",
)
