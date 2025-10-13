from app.modules.bookmarks.domain.entities.bookmark import Bookmark
from app.modules.bookmarks.domain.repository.bookmark_repository_interface import \
    BookmarkRepositoryInterface


class RemoveBookmarkByIdUseCase:
    def __init__(self, bookmark_repository: BookmarkRepositoryInterface):
        self.bookmark_repository = bookmark_repository

    async def execute(self, id: int):
        await self.bookmark_repository.hard_delete(conditions=Bookmark(id=id))
