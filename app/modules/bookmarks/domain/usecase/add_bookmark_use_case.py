from app.modules.bookmarks.domain.entities.bookmark import Bookmark
from app.modules.bookmarks.domain.repository.bookmark_repository_interface import \
    BookmarkRepositoryInterface


class AddBookmarkUseCase:
    def __init__(self, bookmark_repository: BookmarkRepositoryInterface):
        self.bookmark_repository = bookmark_repository

    async def execute(self, user_id: str, book_id: int) -> Bookmark | None:
        return await self.bookmark_repository.create(
            obj=Bookmark(user_id=user_id, book_id=book_id)
        )
