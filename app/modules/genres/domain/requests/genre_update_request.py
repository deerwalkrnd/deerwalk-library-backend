from typing import Optional

from pydantic import BaseModel


class GenreUpdateRequest(BaseModel):
    title: str
    image_url: Optional[str] = None
