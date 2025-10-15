from pydantic import BaseModel


class CreateGenreReqeust(BaseModel):
    title: str
    image_url: str
