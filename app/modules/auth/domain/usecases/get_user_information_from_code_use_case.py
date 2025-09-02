from typing import Any, Dict
import httpx

from app.core.domain.entities.user import User
from app.core.models.users import UserRole


class GetUserInformationFromCodeUseCase:
    def __init__(
        self,
        client: httpx.AsyncClient,
        client_id: str,
        client_secret: str,
        redirect_url: str,
    ) -> None:
        self.client = client
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_url = redirect_url

    async def exchange_code_for_token(self, code: str) -> str:
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_url,
        }
        print("Request data:", data)

        try:
            response = await self.client.post(token_url, data=data, timeout=30)
        except httpx.TimeoutException:
            raise ValueError("timed out")

        response.raise_for_status()
        return response.json().get("access_token")

    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"

        response = await self.client.get(
            url=user_info_url,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    def get_high_quality_picture_url(self, original_url: str | None) -> str:
        if not original_url:
            return ""

        if "=" in original_url:
            base_url = original_url.split("=")[0]
            return f"{base_url}=s800"  # 400x400 pixels

        return original_url

    async def execute(self, code: str) -> User:
        access_token = await self.exchange_code_for_token(code=code)
        user_info = await self.get_user_info(access_token=access_token)
        print(user_info)
        return User(
            email=user_info.get("email"),
            name=user_info.get("name"),
            role=UserRole.STUDENT,
            roll_number=None,
            image_url=self.get_high_quality_picture_url(user_info.get("picture")),
        )
