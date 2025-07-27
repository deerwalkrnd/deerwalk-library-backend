from aiobotocore.session import AioSession
from app.core.infra.services.s3_file_service import S3FileService


async def get_s3_file_service() -> S3FileService:
    session = AioSession()
    file_service = S3FileService(session=session)
    return file_service
