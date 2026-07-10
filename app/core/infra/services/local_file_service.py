import os
from pathlib import Path

from fastapi.logger import logger

from app.core.dependencies.get_settings import get_settings
from app.core.domain.services.file_service_interface import FileServiceInterface


class LocalFileService(FileServiceInterface):
    """Stores uploaded files on local disk under ``settings.upload_dir``.

    The type-based subfolder layout produced by the controller
    (``book-cover/``, ``profile-picture/``, ``event-banners/``, ``misc/``) is
    preserved: the incoming ``file_path`` already contains the subfolder, and it
    is written verbatim under the upload root. Files are served back over HTTP by
    the ``/media`` StaticFiles mount, so ``save`` returns an absolute URL.
    """

    def __init__(self) -> None:
        self.settings = get_settings()
        self.base_dir = Path(self.settings.upload_dir).resolve()
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _resolve(self, file_path: str) -> Path:
        # Confine every path within base_dir; reject traversal / absolute escapes.
        target = (self.base_dir / file_path).resolve()
        if target != self.base_dir and self.base_dir not in target.parents:
            raise ValueError(f"Invalid file path (path traversal blocked): {file_path}")
        return target

    def _url(self, file_path: str) -> str:
        base = self.settings.media_base_url.rstrip("/")
        return f"{base}/media/{file_path.lstrip('/')}"

    async def save(self, file_path: str, body: bytes, content_type: str | None) -> str:
        try:
            target = self._resolve(file_path)
            target.parent.mkdir(parents=True, exist_ok=True)

            # Write atomically: temp file in the same dir, then os.replace.
            tmp = target.with_name(target.name + ".tmp")
            tmp.write_bytes(body)
            os.replace(tmp, target)

            logger.info(f"File saved to local disk: {target}")
            return self._url(file_path)
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error saving file {file_path}: {e}")
            raise ValueError(f"Unexpected error saving file: {str(e)}")

    async def delete(self, file_path: str) -> str:
        try:
            target = self._resolve(file_path)
            if target.is_file():
                target.unlink()
                logger.info(f"File deleted from local disk: {target}")
            else:
                logger.warning(f"File not found for deletion: {target}")
            return self._url(file_path)
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error deleting file {file_path}: {e}")
            raise ValueError(f"Unexpected error deleting file: {str(e)}")

    async def exists(self, file_path: str) -> str:
        target = self._resolve(file_path)
        if not target.is_file():
            raise ValueError(f"no such file: {file_path}")
        return self._url(file_path)

    async def get(self, file_path: str) -> str:
        target = self._resolve(file_path)
        if not target.is_file():
            raise ValueError(f"no such file: {file_path}")
        return str(target)
