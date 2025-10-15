from app.modules.book_borrows.domain.entities.book_borrow import BookBorrow


class BookBorrowResponseDTO(BookBorrow):
    class Config:
        from_attributes = True
