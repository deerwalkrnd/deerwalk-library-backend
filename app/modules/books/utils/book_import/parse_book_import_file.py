from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.modules.books.utils.book_import.parsed_import import ParsedBookImport
from app.modules.books.utils.book_import.register_format import (
    is_register_sheet,
    parse_register_sheets,
)
from app.modules.books.utils.book_import.spreadsheet_reader import read_sheets
from app.modules.books.utils.book_import.template_format import (
    TEMPLATE_HEADERS,
    is_template_sheet,
    parse_template_sheets,
)


def parse_book_import_file(filename: str, content: bytes) -> ParsedBookImport:
    """
    Read a CSV/XLSX upload in either the system template or the library's
    accession-register layout, detected from the column headers.
    """
    sheets = read_sheets(filename=filename, content=content)

    register_sheets = [s for s in sheets if is_register_sheet(s)]
    if register_sheets:
        parsed = parse_register_sheets(register_sheets)
    else:
        template_sheets = [s for s in sheets if is_template_sheet(s)]
        if not template_sheets:
            raise LibraryException(
                status_code=400,
                code=ErrorCode.INVALID_FIELDS,
                msg=(
                    "Could not find a book list in this file. Use the import "
                    f"template (columns: {', '.join(TEMPLATE_HEADERS)}) or the "
                    "library register layout (ACC NO, AUTHOR1, TITLE, ...)."
                ),
            )
        parsed = parse_template_sheets(template_sheets)

    if not parsed.books and not parsed.skipped:
        raise LibraryException(
            status_code=400,
            code=ErrorCode.INVALID_FIELDS,
            msg="The file has headers but no book rows.",
        )

    return parsed
