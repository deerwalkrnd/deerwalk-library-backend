from app.modules.bookmarks.domain.entities.bookmark import Bookmark
from app.modules.bookmarks.domain.repositories.bookmark_repository_interface import (
    BookmarkRepositoryInterface,
)


class CheckBookmarkByBookIdUseCase:
    def __init__(self, bookmark_repository: BookmarkRepositoryInterface):
        self.bookmark_repository = bookmark_repository

    async def execute(self, book_id: int, user_id: str) -> bool:
        bookmark = await self.bookmark_repository.find_one(
            obj=Bookmark(user_id=user_id, book_id=book_id)
        )
        if bookmark:
            return True
        else:
            return False
