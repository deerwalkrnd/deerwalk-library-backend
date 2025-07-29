from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


async def create_email(
    to: str, subject: str, _from: str, html: MIMEText
) -> MIMEMultipart:
    message = MIMEMultipart("alternative")

    message["From"] = _from
    message["To"] = to
    message["Subject"] = subject
    message.attach(html)

    return message
