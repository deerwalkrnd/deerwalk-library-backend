"""
The system's own import template: one row per book.

    title | author | publication | isbn | category | genres | grade | cover_image_url | copies

`genres` and `copies` are comma-separated ("Fiction, Drama" / "ACC-1, ACC-2").
The JSON form older CSVs used (["Fiction"] / [{"unique_identifier": "ACC-1",
"condition": "good"}]) is still accepted.
"""

import ast
import json
import re
from typing import Any, List, Optional

from app.core.models.book import BookCategoryType
from app.modules.books.domain.requests.bulk_book_create_request import (
    BulkCreateBookCopy,
    BulkCreateBookRequest,
)
from app.modules.books.domain.responses.book_bulk_upload_skip_response import (
    BookBulkUploadSkipResponse,
)
from app.modules.books.utils.book_import.parsed_import import ParsedBookImport
from app.modules.books.utils.book_import.spreadsheet_reader import Sheet
from app.modules.books.utils.book_import.values import clean

TEMPLATE_HEADERS = [
    "title",
    "author",
    "publication",
    "isbn",
    "category",
    "genres",
    "grade",
    "cover_image_url",
    "copies",
]


class _RowError(ValueError):
    pass


def is_template_sheet(sheet: Sheet) -> bool:
    return "title" in sheet.headers and "author" in sheet.headers


def parse_template_sheets(sheets: List[Sheet]) -> ParsedBookImport:
    result = ParsedBookImport(format="template")

    for sheet in sheets:
        for row in sheet.rows:
            values = row.values
            title = clean(values.get("title"))
            if not title:
                result.skipped.append(
                    BookBulkUploadSkipResponse(
                        book_title="(no title)",
                        reason="'title' is required",
                        sheet=sheet.name,
                        row=row.number,
                    )
                )
                continue

            try:
                result.books.append(
                    BulkCreateBookRequest(
                        title=title,
                        author=clean(values.get("author")),
                        publication=clean(values.get("publication")),
                        isbn=clean(values.get("isbn")),
                        category=_parse_category(values.get("category")),
                        genres=_parse_genres(values.get("genres")),
                        grade=clean(values.get("grade")),
                        cover_image_url=clean(values.get("cover_image_url")),
                        copies=_parse_copies(values.get("copies")),
                        source_sheet=sheet.name,
                        source_row=row.number,
                    )
                )
            except _RowError as e:
                result.skipped.append(
                    BookBulkUploadSkipResponse(
                        book_title=title,
                        reason=str(e),
                        sheet=sheet.name,
                        row=row.number,
                    )
                )

    return result


def _parse_category(value: Any) -> BookCategoryType:
    text = clean(value)
    if not text:
        return BookCategoryType.NON_ACADEMIC
    normalized = re.sub(r"[\s-]+", "_", text.strip().upper())
    try:
        return BookCategoryType(normalized)
    except ValueError:
        allowed = ", ".join(c.value for c in BookCategoryType)
        raise _RowError(f"Invalid category '{text}'. Must be one of: {allowed}")


def _parse_list_cell(value: Any, field: str) -> Optional[List[Any]]:
    """A JSON / Python list literal, a comma-separated string, or None."""
    text = clean(value)
    if not text:
        return None
    if text.startswith("["):
        for loader in (json.loads, ast.literal_eval):
            try:
                parsed = loader(text)
            except (ValueError, SyntaxError):
                continue
            if isinstance(parsed, list):
                return parsed
        raise _RowError(
            f"Could not read '{field}'. Use a comma-separated list, e.g. A, B"
        )
    return [part.strip() for part in re.split(r"[,;]", text) if part.strip()]


def _parse_genres(value: Any) -> List[str]:
    items = _parse_list_cell(value, "genres") or []
    genres: List[str] = []
    for item in items:
        if not isinstance(item, str) or not item.strip():
            raise _RowError("Every genre must be a non-empty name")
        genres.append(item.strip())
    return genres


def _parse_copies(value: Any) -> List[BulkCreateBookCopy]:
    items = _parse_list_cell(value, "copies") or []
    copies: List[BulkCreateBookCopy] = []
    for item in items:
        if isinstance(item, dict):
            identifier = clean(item.get("unique_identifier"))
            condition = clean(item.get("condition"))
        else:
            identifier = clean(item)
            condition = None
        if not identifier:
            raise _RowError("Every copy needs a unique_identifier")
        copies.append(
            BulkCreateBookCopy(unique_identifier=identifier, condition=condition)
        )
    return copies
