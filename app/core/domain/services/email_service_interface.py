from abc import ABC, abstractmethod
from email.mime.multipart import MIMEMultipart


class EmailServiceInterface(ABC):
    @abstractmethod
    async def send_email(self, message: MIMEMultipart) -> None:
        raise NotImplementedError
