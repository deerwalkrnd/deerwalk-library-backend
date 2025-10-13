from fastapi import APIRouter

from app.modules.auth.presentation.v1.controller.auth_controller import \
    AuthController
from app.modules.auth.presentation.v1.controller.password_reset_token_controller import \
    PasswordResetController

router = APIRouter(prefix="/auth", tags=["auth"])

auth_controller = AuthController()
password_reset_controller = PasswordResetController()

router.add_api_route(
    "/google-callback",
    auth_controller.handle_google_callback,
    methods=["GET"],
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
    "/sso",
    auth_controller.handle_sso_login,
    methods=["GET"],
    response_description="Returns the URL to redirect the user to after generating with google sso",
)

router.add_api_route(
    "/forgot-password",
    password_reset_controller.forgot_password,
    methods=["POST"],
    response_description="Returns the token in email that can be used to reset password",
)

router.add_api_route(
    "/reset-password",
    password_reset_controller.reset_password,
    methods=["POST"],
    response_description="Updates the password if token is valid",
)
