from fastapi import APIRouter

from app.modules.reserves.presentation.v1.controller.reserves_controller import (
    ReservesController,
)

router = APIRouter(prefix="/reserves", tags=["reserves"])
reserves_controller = ReservesController()

router.add_api_route(
    "",
    methods=["POST"],
    response_description="reserves a book for the user",
    endpoint=reserves_controller.reserve_book,
)

router.add_api_route(
    "",
    methods=["GET"],
    response_description="returns all borrow requests along with joined tables",
    endpoint=reserves_controller.get_reserve_requests,
)

router.add_api_route(
    "/{book_id}/is-reserved",
    methods=["GET"],
    response_description="returns if a copy of the provided book has been reserved or not by the currently logged in user",
    endpoint=reserves_controller.is_book_reserved,
)

router.add_api_route(
    "/{reserve_id}",
    methods=["DELETE"],
    response_description="removes a reservation for the book",
    endpoint=reserves_controller.remove_reserve,
)

router.add_api_route(
    "/{reserve_id}/borrowed",
    methods=["POST"],
    response_description="Marks a reserve as reserve completed and gone to the borrowed state",
    endpoint=reserves_controller.after_borrow_from_reserve,
)
