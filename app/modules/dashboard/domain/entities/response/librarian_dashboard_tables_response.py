from typing import List
from pydantic import BaseModel

from app.modules.book_borrows.domain.entities.book_borrow import BookBorrow
from app.modules.books.domain.entities.book import Book
from app.modules.reserves.domain.entities.reserve import Reserve


class LibrarianDashboardTablesResponse(BaseModel):
    top_overdues: List[BookBorrow] = []
    top_books_borrowed: List[Book] = []
    top_issued_books: List[Reserve] = []
