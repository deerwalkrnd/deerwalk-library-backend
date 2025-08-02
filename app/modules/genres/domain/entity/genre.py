from typing import Optional
from pydantic import BaseModel, ConfigDict


class Genre(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: Optional[int] = None
    title: Optional[str] = None
    image_url: Optional[str] = None
