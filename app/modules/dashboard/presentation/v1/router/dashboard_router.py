from fastapi import APIRouter

from app.modules.dashboard.presentation.v1.controller.dashboard_controller import (
    DashboardController,
)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])
dashboard_controller = DashboardController()


router.add_api_route(
    "/librarian",
    endpoint=dashboard_controller.librarian_dashboard,
    methods=["GET"],
    response_description="returns the library dashboard response",
)

router.add_api_route(
    "/student",
    endpoint=dashboard_controller.student_dashboard,
    methods=["GET"],
    response_description="returns the student dashboard",
)
