from fastapi import APIRouter

from app.modules.bookmarks.presentation.v1.controller.bookmark_controller import (
    BookmarkController,
)

router = APIRouter(prefix="/bookmarks", tags=["bookmarks"])

bookmark_controller = BookmarkController()

router.add_api_route(
    path="",
    methods=["GET"],
    endpoint=bookmark_controller.get_bookmark,
    description="get a list of bookmarks for current user.",
)

router.add_api_route(
    path="",
    methods=["POST"],
    endpoint=bookmark_controller.add_bookmark,
    description="create/add bookmark for a user.",
)

router.add_api_route(
    path="/{id}",
    endpoint=bookmark_controller.remove_bookmark,
    methods=["DELETE"],
    description="delete/remove bookmark of a user.",
)

router.add_api_route(
    path="/{book_id}",
    endpoint=bookmark_controller.check_bookmark,
    methods=["GET"],
    description="check if a book is bookmarked or not",
    status_code=200,
)
