from enum import Enum


class ErrorCode(str, Enum):
    TOKEN_EXPIRED = "token_expired"
    INVALID_TOKEN = "invalid_token"
    INSUFFICIENT_PERMISSION = "insufficient_permission"
    INVALID_FIELDS = "invalid_fields"
    UNKOWN_ERROR = "unknown_error"
    DUPLICATE_ENTRY = "duplicate_entry"
    NOT_FOUND = "not_found"
    INCOMPLETE_PROFILE = "incomplete_profile"
