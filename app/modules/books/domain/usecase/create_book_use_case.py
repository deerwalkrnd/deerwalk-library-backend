from app.modules.books.domain.entities.book import Book
from app.modules.books.domain.repository.book_repository_interface import (
    BookRepositoryInterface,
)


class CreateBookUseCase:
    def __init__(self, book_repository: BookRepositoryInterface) -> None:
        self.book_repository = book_repository

    async def execute(
        self,
        title: str,
        author: str,
        publisher: str,
        isbn: str,
        category: str,
        genre: str,
        grade: str,
        cover_image_url: str | None = None,
    ) -> Book | None:
        book = await self.book_repository.create(
            obj=Book(
                title=title,
                author=author,
                publication=publisher,
                isbn=isbn,
                category=category,
                grade=grade,
                cover_image_url=cover_image_url,
            )
        )

        return book
