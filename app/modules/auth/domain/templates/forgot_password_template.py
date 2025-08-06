from email.mime.text import MIMEText
from string import Template

HTTP_TEMPLATE = Template("""
<h1> Dear User, </h1>
<p>
We received a request to reset your password. 

If you want to reset your password Click this link: $link .

If you didn't request a password reset, you can safely ignore this email—your password will remain unchanged.

This link will expire in 15 minutes for your security.  
                                               
</p>
                         
<p>
Warm Regards,
Deerwalk Library
</p>
""")


async def get_forgot_password_template(
    link: str,
) -> MIMEText:
    html_content = HTTP_TEMPLATE.safe_substitute({"link": link})
    html_mime = MIMEText(html_content, "html", "utf-8")
    return html_mime
