from app.core.domain.entities.request.query.filter_request import FilterParams
from app.core.domain.entities.request.query.pagination_request import PaginationParams
from app.core.domain.entities.request.query.sortby_request import SortByRequest


class GetManyBookBorrowRequest(PaginationParams, FilterParams, SortByRequest):
    pass
