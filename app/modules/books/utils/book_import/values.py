import re
import unicodedata
from typing import Any, Optional

from app.modules.books.utils.book_import.spreadsheet_reader import cell_to_text

# What people type into a register cell to mean "nothing recorded".
PLACEHOLDERS = {"n/a", "na", "none", "null", "nil", "not available", "."}


def clean(value: Any) -> Optional[str]:
    """Cell text, or None for blanks and placeholders like '-', '----', 'N/A'."""
    text = cell_to_text(value)
    if text is None:
        return None
    if re.fullmatch(r"[-–—_\s]+", text) or text.lower() in PLACEHOLDERS:
        return None
    return text


def normalize_isbn(value: Any) -> Optional[str]:
    """
    '978-0-544-85992-0', '978 0 544 85992 0' and 9780544859920.0 all become
    '9780544859920'. Anything with too few digits to be an ISBN is None.
    """
    text = clean(value)
    if text is None:
        return None
    isbn = re.sub(r"[^0-9X]", "", text.upper())
    if len(isbn.replace("X", "")) < 9:
        return None
    return isbn


def match_key(value: Optional[str]) -> str:
    """
    Loose comparison key for titles and authors: case, spacing and punctuation
    are ignored. Built by dropping characters rather than a \\w regex so that
    Devanagari vowel signs (Unicode marks, not "word" characters) are kept.
    """
    if not value:
        return ""
    return "".join(
        ch
        for ch in unicodedata.normalize("NFC", value).casefold()
        if not unicodedata.category(ch)[0] in ("P", "Z", "C", "S")
    )
