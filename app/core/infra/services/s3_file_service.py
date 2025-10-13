from datetime import datetime
from typing import Any, Dict

from aiobotocore.session import AioSession
from aiohttp import ClientError
from fastapi.logger import logger

from app.core.dependencies.get_settings import get_settings
from app.core.domain.services.s3_file_service_interface import \
    S3FileServiceInterface


class S3FileService(S3FileServiceInterface):
    def __init__(self, session: AioSession) -> None:
        self.session = session
        self.settings = get_settings()

    async def save(self, file_path: str, body: bytes, content_type: str | None) -> str:
        try:
            async with self.session.create_client(
                "s3",
                region_name=self.settings.s3_region_name,
                aws_access_key_id=self.settings.s3_access_key_id,
                aws_secret_access_key=self.settings.s3_secret_access_key,
            ) as client:
                put_object_kwargs: Dict[str, Any] = {
                    "Bucket": self.settings.s3_bucket_name,
                    "Key": file_path,
                    "Body": body,
                }

                if content_type:
                    put_object_kwargs["ContentType"] = content_type

                put_object_kwargs["Metadata"] = {
                    "uploaded_at": datetime.utcnow().isoformat(),
                    "service": "s3_file_service",
                }

                await client.put_object(**put_object_kwargs)

                logger.info(f"File uploaded successfully to S3: {file_path}")
                return await self.get_base_path() + file_path

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            logger.error(f"AWS S3 error uploading file {file_path}: {error_code} - {e}")
            raise ValueError(f"Failed to upload file to S3: {error_code}")
        except Exception as e:
            logger.error(f"Unexpected error uploading file {file_path}: {e}")
            raise ValueError(f"Unexpected error uploading file: {str(e)}")

    async def delete(self, file_path: str) -> str:
        try:
            async with self.session.create_client(
                "s3",
                region_name=self.settings.s3_region_name,
                aws_access_key_id=self.settings.s3_access_key_id,
                aws_secret_access_key=self.settings.s3_secret_access_key,
            ) as client:
                await client.delete_object(
                    Bucket=self.settings.s3_bucket_name, Key=file_path
                )

                logger.info(f"File deleted successfully from S3: {file_path}")

                return await self.get_base_path() + file_path

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "NoSuchKey":
                logger.warning(f"File not found for deletion in S3: {file_path}")
                raise ValueError(f"File not found for deletion in S3: {file_path}")
            else:
                logger.error(
                    f"AWS S3 error deleting file {file_path}: {error_code} - {e}"
                )
                raise ValueError(f"Failed to delete file from S3: {error_code}")
        except Exception as e:
            logger.error(f"Unexpected error deleting file {file_path}: {e}")
            raise ValueError(f"Unexpected error deleting file: {str(e)}")

    async def exists(self, file_path: str) -> str:
        try:
            async with self.session.create_client(
                "s3",
                region_name=self.settings.s3_region_name,
                aws_access_key_id=self.settings.s3_access_key_id,
                aws_secret_access_key=self.settings.s3_secret_access_key,
            ) as client:
                await client.head_object(
                    Bucket=self.settings.s3_bucket_name, Key=file_path
                )

                return await self.get_base_path() + file_path

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code in ["NoSuchKey", "404"]:
                raise ValueError("no such file in s3")
            else:
                logger.error(
                    f"AWS S3 error checking file existence {file_path}: {error_code} - {e}"
                )
                raise ValueError(f"Failed to check file existence: {error_code}")
        except Exception as e:
            logger.error(f"Unexpected error checking file existence {file_path}: {e}")
            raise ValueError(f"Unexpected error checking file existence: {str(e)}")

    async def get(self, file_path: str) -> str:
        raise NotImplementedError

    async def get_base_path(self) -> str:
        return f"https://{self.settings.s3_bucket_name}.s3.{self.settings.s3_region_name}.amazonaws.com/"
