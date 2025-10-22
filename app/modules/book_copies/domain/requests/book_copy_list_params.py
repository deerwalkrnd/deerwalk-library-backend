from app.core.domain.entities.request.query.filter_request import FilterParams
from app.core.domain.entities.request.query.pagination_request import PaginationParams


class BookCopyListParams(PaginationParams, FilterParams):
    book_id: int
