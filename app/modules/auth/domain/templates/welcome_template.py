from email.mime.text import MIMEText
from string import Template


HTTP_TEMPLATE = Template("""
<h1> Dear $name, </h1>
<p> We wanted to take the time to welcome you to the Deerwalk Library Application.
We hope that you will make the best out of this platform and learn a lot.
 </p>
                         
<p>
Warm Regards,
Deerwalk Library
</p>
""")


async def get_welcome_tempelate(
    name: str,
) -> MIMEText:
    html_content = HTTP_TEMPLATE.safe_substitute({"name": name})
    html_mime = MIMEText(html_content, "html", "utf-8")
    return html_mime
