from typing import Sequence, Type

from pydantic import BaseModel


async def validate_csv_headers(
    model: Type[BaseModel], headers: Sequence[str] | None
) -> bool:
    if not headers:
        return False
    model_fields = set(model.model_fields.keys())
    csv_fields = set(headers)

    return csv_fields == model_fields