from pydantic import BaseModel


class CreateGenreReqeust(BaseModel):
    id: int
    title: str
    image_url: str
