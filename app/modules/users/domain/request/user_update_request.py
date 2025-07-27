from pydantic import BaseModel, EmailStr


class UpdateUserRequest(BaseModel):
    name: str | None = None
    roll_number: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    graduating_year: str | None = None
    user_metadata: dict[str, str] | None = None
    image_url: str | None = None
