from typing import Optional

from pydantic import BaseModel


class QuoteUpdateRequest(BaseModel):
    author: Optional[str] = None
    quote: Optional[str] = None
