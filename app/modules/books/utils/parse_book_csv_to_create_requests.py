import csv
from io import StringIO
from typing import List
from fastapi import UploadFile
from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.core.utils.csv_JSON_parser import csv_JSON_parser
from app.core.utils.csv_validator import validate_csv_headers
from app.modules.books.domain.request.book_create_request import CreateBookRequest


async def parse_book_csv_to_create_requests(
    file: UploadFile,
) -> List[CreateBookRequest]:
    contents = await file.read()
    decoded = contents.decode("utf-8")
    csv_reader = csv.DictReader(StringIO(decoded))

    valid = await validate_csv_headers(
        model=CreateBookRequest,
        headers=csv_reader.fieldnames,
    )
    if not valid:
        raise LibraryException(
            status_code=400,
            code=ErrorCode.INVALID_FIELDS,
            msg="CSV headers do not match!",
        )

    list_csv_reader = list(csv_reader)
    processed_csv = await csv_JSON_parser(
        rows=list_csv_reader, header=["copies", "genres"]
    )

    create_book_requests_model = [CreateBookRequest(**row) for row in processed_csv]
    return create_book_requests_model