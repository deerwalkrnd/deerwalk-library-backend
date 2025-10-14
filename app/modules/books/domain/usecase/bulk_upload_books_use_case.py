import csv
from io import StringIO
from typing import List
from fastapi import UploadFile
from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.core.utils.csv_JSON_parser import csv_JSON_parser
from app.core.utils.csv_validator import validate_csv_headers
from app.modules.books.domain.repository.book_repository_interface import (
    BookRepositoryInterface,
)
from app.modules.books.domain.request.book_create_request import CreateBookRequest


class BulkUploadBooksUseCase:
    def __init__(self, book_repository: BookRepositoryInterface) -> None:
        self.book_repository = book_repository

    async def execute(self, file: UploadFile) -> List[CreateBookRequest] | None:
        contents = await file.read()
        decoded = contents.decode("utf-8")
        csv_reader = csv.DictReader(StringIO(decoded))
        valid = await validate_csv_headers(
            model=CreateBookRequest, headers=csv_reader.fieldnames
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

        books_model = [CreateBookRequest(**row) for row in processed_csv]

        return books_model
