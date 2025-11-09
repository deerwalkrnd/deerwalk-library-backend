from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.modules.book_borrows.domain.requests.get_many_book_borrow_request import (
    GetManyBookBorrowRequest,
)


def validate_get_borrows_request(request: GetManyBookBorrowRequest) -> None:
    if not request.searchable_field:
        return

    allowed_searchable_fields = [
        "student_name",
        "book_title",
        "book_copy_id",
        "unique_identifier",
    ]

    if request.searchable_field not in allowed_searchable_fields:
        raise LibraryException(
            status_code=400,
            code=ErrorCode.INVALID_FIELDS,
            msg="cannot search with that searchable field, values are allowed to be "
            + str(allowed_searchable_fields),
        )
