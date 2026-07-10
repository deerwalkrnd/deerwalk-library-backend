from app.core.domain.services.file_service_interface import FileServiceInterface
from app.core.infra.services.local_file_service import LocalFileService


async def get_file_service() -> FileServiceInterface:
    return LocalFileService()
