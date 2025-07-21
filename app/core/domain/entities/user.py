from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict

from app.core.models.users import UserRole


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: Optional[str] = None
    name: Optional[str] = None
    roll_number: Optional[str] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None
    graduating_year: Optional[str] = None
    image_url: Optional[str] = None
    user_metadata: Optional[Dict[str, Any]] = None


class UserWithPassword(User):
    password: Optional[str] = None
