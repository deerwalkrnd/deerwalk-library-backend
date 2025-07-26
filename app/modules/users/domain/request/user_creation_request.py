from pydantic import BaseModel, EmailStr

from app.core.models.users import UserRole


class UserCreationRequest(BaseModel):
    name: str
    roll_number: str
    email: EmailStr
    password: str
    graduating_year: str
    role: UserRole = UserRole.STUDENT
    user_metadata: dict[str, str]
