from pydantic import BaseModel


class BookReviewCreateRequest(BaseModel):
    book_id: int
    user_id: str
    review_text: str
    is_spam: bool = False
