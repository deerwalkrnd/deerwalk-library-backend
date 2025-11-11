from datetime import datetime
from email.mime.text import MIMEText
from string import Template

HTML_TEMPLATE = Template("""
<h1> Dear $name, </h1>

<table>
    <tr>
        <th>Issue ID</th>
        <th>Book Number</th>
        <th>Book Title</th>
        <th>Retrun Date</th>
    </tr>
    <tr>
        <td>$borrow_id</td>
        <td>$isbn</td>
        <td>$book_title</td>
        <td>$due_date</td>
    </tr>
</table>
    
    <b>Note</b>: please return the book by the given return date, otherwise a fine of <b>Rs $fine</b> will be charged per day.  

<p>
Warm Regards,
Deerwalk Library
</p>
""")


async def get_new_borrow_template(
    name: str, borrow_id: int, isbn: str, book_title: str, due_date: datetime
) -> MIMEText:
    normalized_date = due_date.strftime("%d/%m/%Y")

    event_template = HTML_TEMPLATE.safe_substitute(
        {
            "name": name,
            "borrow_id": borrow_id,
            "due_date": normalized_date,
            "isbn": isbn,
            "book_title": book_title,
        }
    )

    return MIMEText(event_template, "html", "utf-8")
