from pydantic import BaseModel, EmailStr


class PasswordResetTokenRequest(BaseModel):
    email: EmailStr
