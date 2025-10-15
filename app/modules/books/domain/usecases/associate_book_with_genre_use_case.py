from app.modules.books.domain.entities.books_genre import BooksGenre
from app.modules.books.domain.repositories.books_genre_repository_interface import (
    BooksGenreRepositoryInterface,
)


class AssociateBookWithGenreUseCase:
    def __init__(self, books_genre_repository: BooksGenreRepositoryInterface) -> None:
        self.books_genre_repository = books_genre_repository

    async def execute(self, book_id: int, genre_id: int) -> BooksGenre:
        already = await self.books_genre_repository.find_one(
            obj=BooksGenre(book_id=book_id, genre_id=genre_id)
        )
        if already:
            return already

        created = await self.books_genre_repository.create(
            obj=BooksGenre(book_id=book_id, genre_id=genre_id)
        )
        return created if created else BooksGenre()
