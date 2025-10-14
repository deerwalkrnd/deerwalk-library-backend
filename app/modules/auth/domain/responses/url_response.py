from pydantic import BaseModel


class URLResponse(BaseModel):
    url: str
