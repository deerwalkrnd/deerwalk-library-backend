from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template


HTTP_TEMPLATE = Template("""
<h1> Dear $name, </h1>
<p> We wanted to take the time to welcome you to the Deerwalk Library Application.
We hope that you will make the best out of this platform and learn a lot.
 </p>
""")


async def get_welcome_tempelate(
    name: str,
    to: str,
    subject: str,
    _from: str,
) -> MIMEMultipart:
    message = MIMEMultipart("alternative")

    html_content = HTTP_TEMPLATE.safe_substitute({"name": name})
    html_mime = MIMEText(html_content, "html", "utf-8")

    message["From"] = _from
    message["To"] = to
    message["Subject"] = subject

    message.attach(html_mime)

    return message
