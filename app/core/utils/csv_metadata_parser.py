import json
from typing import Any, Dict, List

from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException


async def csv_metadata_parser(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    processed_csv: List[Dict[str, Any]] = []

    for row in rows:
        if "user_metadata" in row and isinstance(row["user_metadata"], str):
            try:
                row["user_metadata"] = json.loads(row["user_metadata"])
            except json.JSONDecodeError:
                raise LibraryException(
                    status_code=500,
                    code=ErrorCode.INVALID_FIELDS,
                    msg="for some reason the server was not able to JSON Decode metadata field from csv.",
                )

        processed_csv.append(row)

    return processed_csv
