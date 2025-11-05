from datetime import datetime
from email.mime.text import MIMEText
from string import Template

HTML_TEMPLATE = Template("""
<h1> Dear $name, </h1>

<p>
    The librarian has added a new event for you to checkout.
    <p> <b> $event_name </b> </p>
    <p> <b> $event_date </b> </p>

</p>

<p>
Warm Regards,
Deerwalk Library
</p>
""")


async def get_new_event_template(
    name: str, event_name: str, event_date: datetime
) -> MIMEText:
    normalized_date = event_date.strftime("%d/%m/%Y")

    event_template = HTML_TEMPLATE.safe_substitute(
        {"name": name, "event_name": event_name, "event_date": normalized_date}
    )

    return MIMEText(event_template, "html", "utf-8")
