from pydantic import BaseModel
from typing import Optional


class BookRecommendationParams(BaseModel):
    limit: Optional[int] = None
