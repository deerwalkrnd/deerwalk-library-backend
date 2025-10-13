from fastapi import APIRouter

from app.modules.users.presentation.v1.controller.users_controller import (
    UsersController,
)

router = APIRouter(prefix="/users", tags=["users"])
users_controller = UsersController()

# router.add_api_route(
#     path="/test",
#     endpoint=users_controller.test_email,
# )

router.add_api_route(
    path="/",
    endpoint=users_controller.list_many_users,
    methods=["GET"],
    response_description="Returns you the Users based on the many params passed",
)
router.add_api_route(
    path="/{uuid}",
    endpoint=users_controller.list_one_user,
    methods=["GET"],
    response_description="You will get user back with the passed uuid",
)
router.add_api_route(
    path="/",
    endpoint=users_controller.create_user,
    methods=["POST"],
    response_description="Creating a uaser entity",
)
router.add_api_route(
    path="/{uuid}",
    endpoint=users_controller.delete_user,
    methods=["DELETE"],
    response_description="Deletes the user and returns success status on deletion",
)
router.add_api_route(
    path="/{uuid}",
    endpoint=users_controller.update_user,
    methods=["PUT"],
    response_description="Update a user based on the incoming field,"
    " need to send a multipart/form-data",
)

router.add_api_route(
    path="/bulk-upload",
    endpoint=users_controller.bulk_upload_users,
    methods=["POST"],
    response_description="upload a csv to bulk-create users.",
)
