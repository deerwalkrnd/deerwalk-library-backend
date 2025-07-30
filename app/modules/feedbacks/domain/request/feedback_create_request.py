from pydantic import BaseModel


class FeedbackCreateRequest(BaseModel):
    subject: str
    feedback: str
