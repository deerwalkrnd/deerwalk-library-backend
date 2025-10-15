from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PasswordResetToken(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int | None = None
    user_id: str | None = None
    token: str | None = None
    expires_at: datetime | None = None
