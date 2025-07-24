from fastapi import Depends
from app.core.dependencies.middleware.get_available_user import get_available_user
from app.core.domain.entities.user import User
from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.modules.auth.domain.request.login_request import LoginRequest
from app.modules.auth.domain.response.token_response import TokenResponse


class AuthController:
    def __init__(self) -> None:
        pass

    async def login(
        self, login_request: LoginRequest, user: User = Depends(get_available_user)
    ) -> TokenResponse:
        print(user)
        if user:
            raise LibraryException(
                status_code=409,
                code=ErrorCode.DUPLICATE_ENTRY,
                msg="You are already logged in, you don't need to login again.",
            )
        print(login_request)
        return TokenResponse(token="asd")

    async def google_login(
        self,
    ) -> TokenResponse:
        return TokenResponse(token="")
