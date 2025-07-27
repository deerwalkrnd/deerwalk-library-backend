from pydantic import BaseModel, EmailStr

from app.core.models.users import UserRole


class UpdateUserRequest(BaseModel):
    name: str | None = None
    roll_number: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    graduating_year: str | None = None
    role: UserRole | None = None
    # user_metadata: dict[str, str] | None = None
