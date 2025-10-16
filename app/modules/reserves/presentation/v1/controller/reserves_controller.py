from typing import Any
from app.modules.reserves.domain.requests.reserve_book_request import ReserveBookRequest


class ReservesController:
    def __init__(self) -> None:
        pass

    async def reserve_book(self, reserve_book_request: ReserveBookRequest) -> None:
        raise NotImplementedError

    async def remove_reserve(self, reserve_id: int) -> None:
        raise NotImplementedError

    async def is_book_reserved(self, book_id: int) -> Any:
        raise NotImplementedError

    async def get_borrow_requests(self, params: Any) -> Any:
        raise NotImplementedError
