from string import Template

from fastapi import Depends, UploadFile, logger

from app.core.dependencies.middleware.get_current_librarian import get_current_librarian
from app.core.domain.entities.user import User
from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.core.infra.services.s3_file_service import S3FileService
from app.modules.files.dependencies.get_s3_file_service import get_s3_file_service
from app.modules.files.domain.requests.file_type_enum import LibraryFileType
from app.modules.files.domain.responses.file_response import FileResponse

PROFILE_PATH = Template("profile-picture/$filename")
BOOK_COVER_PATH = Template("book-cover/$filename")


class FileController:
    async def upload(
        self,
        file: UploadFile,
        type: LibraryFileType,
        _: User = Depends(get_current_librarian),
        file_service: S3FileService = Depends(get_s3_file_service),
    ) -> FileResponse:
        try:
            path = ""

            if type == LibraryFileType.PROFILE_IMAGE:
                path = PROFILE_PATH.safe_substitute({"filename": file.filename})
            else:
                path = BOOK_COVER_PATH.safe_substitute({"filename": file.filename})

            url = await file_service.save(
                file_path=path,
                body=await file.read(),
                content_type=file.content_type,
            )
            return FileResponse(url=url)
        except Exception as e:
            logger.logger.error(e)
            raise LibraryException(
                status_code=500,
                code=ErrorCode.UNKOWN_ERROR,
                msg="Unable to upload files" + str(e),
            )
