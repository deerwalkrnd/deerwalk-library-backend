from abc import abstractmethod

from app.core.domain.services.file_service_interface import \
    FileServiceInterface


class S3FileServiceInterface(FileServiceInterface):
    @abstractmethod
    async def get_base_path(self) -> str:
        raise NotImplementedError
