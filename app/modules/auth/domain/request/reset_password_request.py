from pydantic import BaseModel


class ResetPasswordRequest(BaseModel):
    secret_token: str
    new_password: str
    confirm_password: str
