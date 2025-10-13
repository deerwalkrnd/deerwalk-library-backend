from app.core.models.book import BookCategoryType
from app.modules.books.domain.entities.book import Book
from app.modules.books.domain.repository.book_repository_interface import \
    BookRepositoryInterface


class CreateBookUseCase:
    def __init__(self, book_repository: BookRepositoryInterface) -> None:
        self.book_repository = book_repository

    async def execute(
        self,
        title: str,
        author: str,
        publication: str,
        isbn: str,
        category: BookCategoryType,
        grade: str | None,
        cover_image_url: str | None = None,
    ) -> Book | None:
        book = await self.book_repository.create(
            obj=Book(
                title=title,
                author=author,
                publication=publication,
                isbn=isbn,
                category=category,
                grade=grade,
                cover_image_url=cover_image_url,
            )
        )

        return book
