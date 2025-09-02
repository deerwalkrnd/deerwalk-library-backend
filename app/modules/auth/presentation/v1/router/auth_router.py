from fastapi import APIRouter

from app.modules.auth.presentation.v1.controller.auth_controller import AuthController

router = APIRouter(prefix="/auth", tags=["Auth Routes"])

auth_controller = AuthController()

router.add_api_route(
    "/login-google",
    auth_controller.handle_google_callback,
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
    "/sso",
    auth_controller.handle_sso_login,
    methods=["GET"],
    response_description="Returns the URL to redirect the user to after generating with google sso",
)

# TODO(forgot password)
# We will do the forgot password feature after we've done the email service with celery
