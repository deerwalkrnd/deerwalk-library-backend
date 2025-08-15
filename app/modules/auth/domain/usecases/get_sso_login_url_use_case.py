from app.core.dependencies.get_settings import get_settings
from app.modules.auth.domain.request.sso_url_request import SSOProviderEnum


class GetSSOLoginURLUseCase:
    def __init__(self) -> None:
        pass

    async def execute(self, sso: SSOProviderEnum) -> str:
        config = get_settings()
        match sso:
            case SSOProviderEnum.GOOGLE:
                return f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={config.google_client_id}&redirect_uri={config.google_redirect_url}&scope=openid%20profile%20email&access_type=offline"
            case _:
                raise ValueError("no such SSO platform")
