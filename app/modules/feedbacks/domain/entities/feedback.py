from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.core.domain.entities.user import User


class Feedback(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: Optional[int] = None
    subject: Optional[str] = None
    feedback: Optional[str] = None
    user_id: Optional[str] = None
    is_acknowledged: Optional[bool] = None
    user: Optional[User] = None
    created_at: Optional[datetime] = None
