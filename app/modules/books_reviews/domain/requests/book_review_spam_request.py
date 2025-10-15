from pydantic import BaseModel


class BookReviewSpamRequest(BaseModel):
    is_spam: bool
