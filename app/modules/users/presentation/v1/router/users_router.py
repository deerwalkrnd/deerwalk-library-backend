from fastapi import APIRouter

from app.modules.users.presentation.v1.controller.users_controller import (
    UsersController,
)

router = APIRouter(prefix="/users", tags=["Users API"])
users_controller = UsersController()

router.add_api_route(
    path="/",
    endpoint=users_controller.list_many_users,
    methods=["GET"],
    response_description="Returns you the Users based on the many params passed",
)
