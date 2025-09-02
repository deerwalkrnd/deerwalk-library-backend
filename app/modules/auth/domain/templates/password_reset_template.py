from email.mime.text import MIMEText
from string import Template

HTTP_TEMPLATE = Template("""
<h1> Dear $name, </h1>
<p> We heard that you wanted to reset your password, please click the link below:
    link: $password_reset_link
 </p>
                         
<p>
Warm Regards,
Deerwalk Library
</p>
""")


async def get_password_reset_template(name: str, password_reset_link: str) -> MIMEText:
    html_content = HTTP_TEMPLATE.safe_substitute(
        {"name": name, "password_reset_link": password_reset_link}
    )
    html_mime = MIMEText(html_content, "html", "utf-8")
    return html_mime
