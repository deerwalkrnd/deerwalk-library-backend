from typing import Any, Dict, List, Optional

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
        detail: Optional[Dict[str, Any]] = None,
    ) -> None:
        error_detail: Dict[str, Any] = {
            "code": code,
            "msg": msg,
            "fields": fields,
        }
        if detail:
            error_detail["detail"] = detail
        super().__init__(status_code, error_detail, headers)
