from fastapi import APIRouter

from app.modules.auth.presentation.v1.controller.auth_controller import AuthController

router = APIRouter(prefix="/auth", tags=["Auth Routes"])

auth_controller = AuthController()

router.add_api_route(
    "/login-google",
    auth_controller.google_login,
    methods=["POST"],
    response_description="Here the `token` field in the response contains the url "
    "instead of the jwt token",
)

router.add_api_route(
    "/login",
    auth_controller.login,
    methods=["POST"],
    response_description="Returns the Token of the logged in user or throws an 403 if "
    "incorrect credentials",
)
