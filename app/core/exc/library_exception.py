from typing import Any, Dict, List

from fastapi import HTTPException

from app.core.exc.error_code import ErrorCode


class LibraryException(HTTPException):
    def __init__(
        self,
        status_code: int,
        code: ErrorCode,
        msg: str,
        fields: List[Any] = [],
        headers: Dict[str, str] | None = None,
    ) -> None:
        detail = {"code": code, "msg": msg, "fields": fields}  # type:ignore
        super().__init__(status_code, detail, headers)
