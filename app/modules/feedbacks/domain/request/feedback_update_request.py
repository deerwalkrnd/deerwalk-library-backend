from typing import Optional
from pydantic import BaseModel


class FeedbackUpdateRequest(BaseModel):
    subject: Optional[str] = None
    feedback: Optional[str] = None
    is_acknowledged: Optional[bool] = None
