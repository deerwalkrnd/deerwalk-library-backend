from enum import Enum

from pydantic import BaseModel


class SSOProviderEnum(Enum):
    GOOGLE = "GOOGLE"


class SSOURLRequest(BaseModel):
    provider: SSOProviderEnum
