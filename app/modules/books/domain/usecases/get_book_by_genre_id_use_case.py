from app.modules.books.domain.entities.books_genre import BooksGenre
from app.modules.books.domain.repositories.books_genre_repository_interface import BooksGenreRepositoryInterface


class GetBookByGenreIdUseCase():
    def __init__(self, book_genre_repository: BooksGenreRepositoryInterface):
        self.book_genre_repository = book_genre_repository
    
    async def execute(self, genre_id: int):
        books = await self.book_genre_repository.find_many(limit = 50, offset=0, sort_by="created_at", descending=True,filter=BooksGenre(genre_id=genre_id))
        return books