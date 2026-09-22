"""
The library's accession register ("DSS DATA ENTRY LIBRARY BOOKS" workbook):
one row per physical copy, spread over several sheets.

    S.N | DATE | ACC NO | AUTHOR1 | AUTHOR2 | TITLE | TITLE1 | CATEGORY |
    PLACE AND PUBLISHER | YEAR | PAGES | PRICE | ISBN NO. | CONDTION

Header spelling and column order differ from sheet to sheet, so columns are
found by name. Rules:

* Every sheet keeps its own accession series (#10 on one sheet is a different
  book from #10 on another), so a copy's unique_identifier is the sheet name
  plus the accession number, e.g. "NEPALI-MSHS-9278". A CSV has no sheet name
  and uses the bare number.
* The same accession number with the same title on two sheets is one copy
  listed twice (some sheets are merged copies of others); it is imported once,
  under the first sheet it appears on.
* Copies are grouped into books by ISBN, or by title + author when the ISBN
  is missing. A copy with no ISBN whose title and author match a book that
  does have one joins that book.
"""

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

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
from app.modules.books.utils.book_import.values import (
    clean,
    match_key,
    normalize_isbn,
)

# Normalised header spellings seen across the register's sheets.
ACCESSION_HEADERS = [
    "accession number",
    "accession no.",
    "accession no",
    "acc no.",
    "acc no",
    "acc. no.",
    "accession",
]
TITLE_HEADERS = ["title"]
ALT_TITLE_HEADERS = ["title1"]
AUTHOR_HEADERS = ["author1", "author"]
SECOND_AUTHOR_HEADERS = ["author2"]
PUBLISHER_HEADERS = ["place and publisher", "publisher", "publication"]
ISBN_HEADERS = ["isbn no.", "isbn no", "isbn"]
CONDITION_HEADERS = ["condtion", "condition"]
CATEGORY_HEADERS = ["category"]

# CATEGORY values that mean a school subject.
ACADEMIC_SUBJECTS = {
    "accountancy",
    "biology",
    "chemistry",
    "commerce",
    "computer",
    "economics",
    "engineering",
    "english",
    "math",
    "mathematics",
    "maths",
    "nepali",
    "physics",
    "science",
    "social",
}
REFERENCE_TITLE_PATTERN = re.compile(
    r"encyclop|dictionary|thesaurus|atlas|शब्दकोश", re.IGNORECASE
)


@dataclass
class _Copy:
    sheet: Optional[str]
    row: int
    title: str
    author: Optional[str]
    publication: Optional[str]
    isbn: Optional[str]
    category: BookCategoryType
    unique_identifier: str
    condition: Optional[str]


def is_register_sheet(sheet: Sheet) -> bool:
    return "title" in sheet.headers and (
        "author1" in sheet.headers or _find_header(sheet, ACCESSION_HEADERS) is not None
    )


def sheet_prefix(sheet_name: Optional[str]) -> Optional[str]:
    """'NEPALI MSHS' -> 'NEPALI-MSHS'; ' FICTION ENG' -> 'FICTION-ENG'."""
    if not sheet_name:
        return None
    prefix = re.sub(r"[^0-9A-Zऀ-ॿ]+", "-", sheet_name.upper()).strip("-")
    return prefix or None


def parse_register_sheets(sheets: List[Sheet]) -> ParsedBookImport:
    result = ParsedBookImport(format="register")
    copies: List[_Copy] = []
    # (accession number, title key) -> copy already taken, across all sheets
    seen_accessions: Dict[Tuple[str, str], _Copy] = {}
    # unique_identifier -> copy, to catch one number reused for two books
    seen_identifiers: Dict[str, _Copy] = {}

    for sheet in sheets:
        if not is_register_sheet(sheet):
            continue

        accession_header = _find_header(sheet, ACCESSION_HEADERS) or _find_header(
            sheet, ["acc"]
        )
        prefix = sheet_prefix(sheet.name)

        for row in sheet.rows:
            values = row.values
            title = _first(values, TITLE_HEADERS) or _first(values, ALT_TITLE_HEADERS)
            accession = clean(values.get(accession_header)) if accession_header else None

            if not title:
                if accession:
                    result.skipped.append(
                        _skip("(no title)", f"Accession {accession} has no title", sheet, row.number)
                    )
                continue
            if not accession:
                result.skipped.append(
                    _skip(title, "No accession number, so the copy cannot be identified", sheet, row.number)
                )
                continue

            title_key = match_key(title)
            earlier = seen_accessions.get((accession, title_key))
            if earlier:
                result.duplicates_ignored += 1
                continue

            identifier = f"{prefix}-{accession}" if prefix else accession
            clash = seen_identifiers.get(identifier)
            if clash:
                result.skipped.append(
                    _skip(
                        title,
                        f"Accession {accession} is already used by '{clash.title}' "
                        f"(row {clash.row}) on this sheet",
                        sheet,
                        row.number,
                    )
                )
                continue

            copy = _Copy(
                sheet=sheet.name,
                row=row.number,
                title=title,
                author=_author(values),
                publication=_first(values, PUBLISHER_HEADERS),
                isbn=normalize_isbn(_first(values, ISBN_HEADERS)),
                category=_category(values, title, sheet.name),
                unique_identifier=identifier,
                condition=_condition(values),
            )
            seen_accessions[(accession, title_key)] = copy
            seen_identifiers[identifier] = copy
            copies.append(copy)

    result.books = _group_into_books(copies)
    return result


def _group_into_books(copies: List[_Copy]) -> List[BulkCreateBookRequest]:
    def title_author_key(copy: _Copy) -> Tuple[str, str, str]:
        return ("title", match_key(copy.title), match_key(copy.author))

    # A copy without an ISBN joins the ISBN'd book with the same title/author.
    isbn_by_title_author: Dict[Tuple[str, str, str], str] = {}
    for copy in copies:
        if copy.isbn:
            isbn_by_title_author.setdefault(title_author_key(copy), copy.isbn)

    books: Dict[Tuple[str, ...], BulkCreateBookRequest] = {}
    for copy in copies:
        isbn = copy.isbn or isbn_by_title_author.get(title_author_key(copy))
        key: Tuple[str, ...] = ("isbn", isbn) if isbn else title_author_key(copy)

        book = books.get(key)
        if book is None:
            book = BulkCreateBookRequest(
                title=copy.title,
                author=copy.author,
                publication=copy.publication,
                isbn=isbn,
                category=copy.category,
                source_sheet=copy.sheet,
                source_row=copy.row,
            )
            books[key] = book
        else:
            # Fill in whatever the first copy's row left blank.
            book.author = book.author or copy.author
            book.publication = book.publication or copy.publication
            if book.category == BookCategoryType.NON_ACADEMIC:
                book.category = copy.category

        book.copies.append(
            BulkCreateBookCopy(
                unique_identifier=copy.unique_identifier, condition=copy.condition
            )
        )

    return list(books.values())


def _find_header(sheet: Sheet, candidates: List[str]) -> Optional[str]:
    return next((h for h in candidates if h in sheet.headers), None)


def _first(values: Dict[str, Any], headers: List[str]) -> Optional[str]:
    for header in headers:
        text = clean(values.get(header))
        if text:
            return text
    return None


def _author(values: Dict[str, Any]) -> Optional[str]:
    first = _first(values, AUTHOR_HEADERS)
    second = _first(values, SECOND_AUTHOR_HEADERS)
    if first and second and match_key(first) != match_key(second):
        return f"{first}; {second}"
    return first or second


def _condition(values: Dict[str, Any]) -> Optional[str]:
    condition = _first(values, CONDITION_HEADERS)
    # A few rows have the ISBN typed into the condition column.
    if condition and len(re.sub(r"\D", "", condition)) >= 9:
        return None
    return condition


def _category(
    values: Dict[str, Any], title: str, sheet_name: Optional[str]
) -> BookCategoryType:
    if REFERENCE_TITLE_PATTERN.search(title):
        return BookCategoryType.REFERENCE
    if match_key(_first(values, CATEGORY_HEADERS)) in ACADEMIC_SUBJECTS:
        return BookCategoryType.ACADEMIC
    if sheet_name and "COURSE" in sheet_name.upper():
        return BookCategoryType.ACADEMIC
    return BookCategoryType.NON_ACADEMIC


def _skip(title: str, reason: str, sheet: Sheet, row: int) -> BookBulkUploadSkipResponse:
    return BookBulkUploadSkipResponse(
        book_title=title, reason=reason, sheet=sheet.name, row=row
    )
