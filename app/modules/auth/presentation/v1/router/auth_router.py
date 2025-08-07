from fastapi import APIRouter

from app.modules.auth.presentation.v1.controller.auth_controller import AuthController
from app.modules.auth.presentation.v1.controller.forgot_password_controller import (
    ForgotPasswordController,
)

router = APIRouter(prefix="/auth", tags=["Auth Routes"])

auth_controller = AuthController()
forgot_password_controller = ForgotPasswordController()

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

router.add_api_route(
    "/me",
    auth_controller.handle_me,
    methods=["GET"],
    response_description="Returns the User Data if logged in else, 403",
)

router.add_api_route(
    "/forgot-password",
    forgot_password_controller.forgot_password,
    methods=["POST"],
    response_description="Returns a token to be used in url.",
)

router.add_api_route(
    "/reset-password",
    forgot_password_controller.reset_password,
    methods=["POST"],
    response_description="Resets the password to new password.",
)

# TODO(forgot password)
# We will do the forgot password feature after we've done the email service with celery
