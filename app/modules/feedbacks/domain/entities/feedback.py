from typing import Optional
from pydantic import BaseModel, ConfigDict


class Feedback(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: Optional[int] = None
    subject: Optional[str] = None
    feedback: Optional[str] = None
    user_id: Optional[str] = None
    is_acknowledged: Optional[bool] = None
