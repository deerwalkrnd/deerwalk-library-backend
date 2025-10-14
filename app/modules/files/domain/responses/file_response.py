from pydantic import BaseModel


class FileResponse(BaseModel):
    url: str
