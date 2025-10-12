import csv
from io import StringIO
from fastapi import UploadFile
from app.core.domain.repositories.user_repository_interface import (
    UserRepositoryInterface,
)
from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.core.utils.csv_metadata_parser import csv_metadata_parser
from app.core.utils.csv_password_hasher import csv_password_hasher
from app.core.utils.csv_validator import validate_csv_headers
from app.modules.users.domain.request.user_creation_request import UserCreationRequest


class BulkUploadUsersUseCase:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    async def execute(self, file: UploadFile):
        contents = await file.read()
        decoded = contents.decode("utf-8")
        csv_reader = csv.DictReader(StringIO(decoded))

        valid = await validate_csv_headers(
            model=UserCreationRequest, headers=csv_reader.fieldnames
        )

        if not valid:
            raise LibraryException(
                status_code=400,
                code=ErrorCode.INVALID_FIELDS,
                msg="CSV headers do not match!",
            )
        
        password_hased_csv = await csv_password_hasher(rows=csv_reader)
        processed_csv = await csv_metadata_parser(rows=password_hased_csv)

        inserted_count, skipped_count = await self.user_repository.insert_many(
            rows=processed_csv
        )
        return {"inserted": inserted_count, "skipped": skipped_count}
