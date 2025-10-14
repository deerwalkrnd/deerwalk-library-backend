from pydantic import BaseModel


class QuoteCreateRequest(BaseModel):
    author: str
    quote: str
