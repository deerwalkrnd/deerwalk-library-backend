import json
from typing import Any, Dict, List

from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException


async def csv_JSON_parser(
    rows: List[Dict[str, Any]], header: List[str]
) -> List[Dict[str, Any]]:
    processed_csv: List[Dict[str, Any]] = []

    for row in rows:
        for head in header:
            if head in row and isinstance(row[head], str):
                try:
                    row[head] = json.loads(row[head])
                except json.JSONDecodeError:
                    raise LibraryException(
                        status_code=500,
                        code=ErrorCode.INVALID_FIELDS,
                        msg=f"for some reason the server was not able to JSON Decode {header} field from csv.",
                    )

        processed_csv.append(row)

    return processed_csv
