import csv
from io import BytesIO, StringIO
from typing import Iterable, List

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

from app.core.models.book import BookCategoryType
from app.modules.books.utils.book_import.template_format import TEMPLATE_HEADERS

# (column, required, what to enter, example)
COLUMN_GUIDE = [
    ("title", "Yes", "Book title.", "The Famous Five"),
    ("author", "No", "Author name(s).", "Enid Blyton"),
    ("publication", "No", "Publisher.", "Hodder Children's Books"),
    (
        "isbn",
        "No",
        "ISBN-10 or ISBN-13; dashes and spaces are fine. Rows with the same ISBN "
        "are treated as the same book.",
        "978-0-340-93158-7",
    ),
    (
        "category",
        "No",
        "One of " + ", ".join(c.value for c in BookCategoryType) + ". Defaults to NON_ACADEMIC.",
        "NON_ACADEMIC",
    ),
    (
        "genres",
        "No",
        "Comma-separated genre names that already exist (see the Genres sheet). "
        "Leave empty to file the book under 'Uncategorized'.",
        "Fiction, Adventure",
    ),
    ("grade", "No", "Grade the book is meant for.", "5"),
    ("cover_image_url", "No", "Link to a cover image.", ""),
    (
        "copies",
        "No",
        "Comma-separated accession numbers, one per physical copy. Copies that are "
        "already in the library are skipped.",
        "ACC-101, ACC-102",
    ),
]

HEADER_FONT = Font(bold=True, color="FFFFFF")
HEADER_FILL = PatternFill("solid", fgColor="1E78B9")


def build_xlsx_template(genre_names: Iterable[str]) -> bytes:
    workbook = Workbook()

    books = workbook.active
    books.title = "Books"
    books.append(TEMPLATE_HEADERS)
    _style_header(books, widths=[36, 24, 26, 20, 16, 26, 8, 30, 26])
    books.freeze_panes = "A2"
    category_column = chr(ord("A") + TEMPLATE_HEADERS.index("category"))
    category_choices = DataValidation(
        type="list",
        formula1='"' + ",".join(c.value for c in BookCategoryType) + '"',
        allow_blank=True,
    )
    books.add_data_validation(category_choices)
    category_choices.add(f"{category_column}2:{category_column}5000")

    # One column name per row, so the importer never mistakes this sheet
    # (whose rows contain "title" but never alongside "author") for data.
    guide = workbook.create_sheet("Instructions")
    guide.append(["Column", "Required", "What to enter", "Example"])
    for row in COLUMN_GUIDE:
        guide.append(list(row))
    guide.append([])
    guide.append(
        [
            "Note",
            "",
            "Fill in the Books sheet, one row per book. The library's accession "
            "register (ACC NO, AUTHOR1, TITLE, ...) can also be uploaded as-is.",
        ]
    )
    _style_header(guide, widths=[18, 10, 80, 26])
    for row in guide.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")

    genres = workbook.create_sheet("Genres")
    genres.append(["Available genres"])
    for name in sorted(genre_names, key=str.casefold):
        genres.append([name])
    _style_header(genres, widths=[32])

    buffer = BytesIO()
    workbook.save(buffer)
    return buffer.getvalue()


def build_csv_template() -> bytes:
    buffer = StringIO()
    csv.writer(buffer).writerow(TEMPLATE_HEADERS)
    # BOM so Excel opens the file as UTF-8 (Nepali titles).
    return buffer.getvalue().encode("utf-8-sig")


def _style_header(sheet, widths: List[int]) -> None:
    for cell in sheet[1]:
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
    for index, width in enumerate(widths):
        sheet.column_dimensions[chr(ord("A") + index)].width = width
