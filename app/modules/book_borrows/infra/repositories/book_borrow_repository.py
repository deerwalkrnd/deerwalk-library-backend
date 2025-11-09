from datetime import datetime
from typing import List

from pydantic import BaseModel
from sqlalchemy import and_, desc, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.infra.repositories.repository import Repository
from app.core.models.book import BookModel
from app.core.models.book_borrow import BookBorrowModel, FineStatus
from app.core.models.book_copy import BookCopyModel
from app.core.models.users import UserModel
from app.modules.book_borrows.domain.entities.book_borrow import BookBorrow
from app.modules.book_borrows.domain.repositories.book_borrow_repository_interface import (
    BookBorrowRepositoryInterface,
)
from app.modules.book_borrows.domain.responses.book_borrow_response_dto import (
    BookBorrowResponseDTO,
)

from app.core.models.books_genre import BooksGenreModel
from app.modules.books.domain.entities.book import Book


class BookBorrowRepository(
    Repository[BookBorrowModel, BookBorrow], BookBorrowRepositoryInterface
):
    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        super().__init__(db, BookBorrowModel, BookBorrow)

    async def get_borrow_with_user_and_book(
        self,
        filter: BaseModel | None,
        limit: int,
        offset: int,
        sort_by: str,
        descending: bool,
        start_date: datetime | None,
        end_date: datetime | None,
        searchable_key: str | None,
        searchable_value: str | None,
    ) -> List[BookBorrowResponseDTO]:
        if limit <= 0 or offset < 0:
            raise ValueError("Invalid limit or offset")

        if start_date and end_date and start_date > end_date:
            raise ValueError("start_date cannot be after end_date")

        if searchable_key and not searchable_value:
            raise ValueError("searchable_value required when searchable_key provided")

        query = (
            select(BookBorrowModel)
            .options(
                selectinload(BookBorrowModel.user),
                selectinload(BookBorrowModel.book_copy).selectinload(
                    BookCopyModel.book
                ),
            )
            .where(BookBorrowModel.deleted == False)
        )

        query = (
            query.join(BookCopyModel, BookBorrowModel.book_copy_id == BookCopyModel.id)
            .join(UserModel, UserModel.uuid == BookBorrowModel.user_id)
            .join(BookModel, BookModel.id == BookCopyModel.book_id)
        )

        if filter is not None:
            conditions = filter.model_dump(exclude_unset=True)
            for key, value in conditions.items():
                if not hasattr(self.model, key):
                    raise ValueError(f"Invalid filter key: {key}")
                query = query.where(getattr(self.model, key) == value)

        date_column = getattr(self.model, "created_at", None)
        if date_column is not None:
            if start_date:
                query = query.where(date_column >= start_date)
            if end_date:
                query = query.where(date_column <= end_date)

        if searchable_key and searchable_value:
            match searchable_key:
                case "student_name":
                    query = query.where(UserModel.name.ilike(f"%{searchable_value}%"))
                case "book_title":
                    query = query.where(BookModel.title.ilike(f"%{searchable_value}%"))
                case "book_copy_id":
                    try:
                        book_copy_id = int(searchable_value)
                    except ValueError as e:
                        raise e

                    query = query.where(BookCopyModel.id == book_copy_id)
                case "unique_identifier":
                    query = query.where(
                        BookCopyModel.unique_identifier.ilike(f"%{searchable_value}%")
                    )
                case _:
                    if not hasattr(self.model, searchable_key):
                        raise ValueError(f"Invalid searchable_key: {searchable_key}")
                    query = query.where(
                        getattr(self.model, searchable_key).ilike(
                            f"%{searchable_value}%"
                        )
                    )

        if not hasattr(self.model, sort_by):
            raise ValueError(f"Invalid sort_by column: {sort_by}")

        sort_column = getattr(self.model, sort_by)
        query = query.order_by(desc(sort_column) if descending else sort_column)

        query = query.limit(limit).offset(offset)

        print(query)

        result = await self.db.execute(query)
        data = result.scalars().unique().all()

        print(data)

        return [BookBorrowResponseDTO.model_validate(obj=x) for x in data]

    async def student_dashboard(self, student_id: str) -> dict[str, int | str]:
        data: dict[str, int | str] = {}

        # total borrowed count (all time)
        query = (
            select(func.count())
            .select_from(self.model)
            .where(and_(self.model.deleted == False, self.model.user_id == student_id))
        )
        result = await self.db.execute(query)
        data["borrowed_count"] = result.scalar() or 0

        # returned books count
        query = (
            select(func.count())
            .select_from(self.model)
            .where(
                and_(
                    self.model.deleted == False,
                    self.model.returned == True,
                    self.model.user_id == student_id,
                )
            )
        )
        result = await self.db.execute(query)
        data["returned_books_count"] = result.scalar() or 0

        # overdue books count
        query = (
            select(func.count())
            .select_from(self.model)
            .where(
                and_(
                    self.model.deleted == False,
                    self.model.returned == False,
                    self.model.due_date < datetime.now(),
                    self.model.user_id == student_id,
                )
            )
        )
        result = await self.db.execute(query)
        data["overdue_books_count"] = result.scalar() or 0

        # fine accumulated
        query = (
            select(func.sum(self.model.fine_accumulated))
            .select_from(self.model)
            .where(
                and_(
                    self.model.deleted == False,
                    self.model.user_id == student_id,
                )
            )
        )
        result = await self.db.execute(query)
        data["fine_levied"] = result.scalar() or 0

        # most borrowed category
        query = (
            select(BookModel.category)
            .join(BookCopyModel, BookModel.id == BookCopyModel.book_id)
            .join(BookBorrowModel, BookBorrowModel.book_copy_id == BookCopyModel.id)
            .where(BookBorrowModel.user_id == student_id)
            .group_by(BookModel.category)
            .order_by(func.count(BookBorrowModel.id).desc())
            .limit(1)
        )

        result = await self.db.execute(query)
        most_read_category = result.scalar()
        data["most_borrowed_category"] = (
            most_read_category.value if most_read_category else "none"
        )

        return data

    async def librarian_dashboard(self) -> dict[str, int]:
        data: dict[str, int] = {}
        # overdue books
        query = select(func.count(self.model.id)).where(
            and_(
                self.model.deleted == False,
                self.model.returned == False,
                self.model.due_date < datetime.now(),
            )
        )

        result = await self.db.execute(query)
        overdue_books_count = result.scalar() or 0

        data["overdue_books_count"] = overdue_books_count

        # total returned books
        query = select(func.count(self.model.id)).where(
            and_(self.model.deleted == False, self.model.returned == True)
        )

        result = await self.db.execute(query)
        returned_books_count = result.scalar() or 0

        data["returned_books_count"] = returned_books_count

        # currently issued books
        query = select(func.count(self.model.id)).where(
            and_(self.model.deleted == False, self.model.returned == False)
        )
        result = await self.db.execute(query)
        currently_issued_books_count = result.scalar() or 0

        data["currently_issued_books_count"] = currently_issued_books_count

        # total pending fines

        query = select(func.sum(self.model.fine_accumulated)).where(
            and_(
                self.model.deleted == False, self.model.fine_status == FineStatus.UNPAID
            )
        )

        result = await self.db.execute(query)
        total_pending_fines = result.scalar() or 0

        data["total_pending_fines"] = total_pending_fines

        return data

    async def get_book_recommendations(
        self, user_id: str, limit: int = 10
    ) -> List[Book]:
        currently_borrowed_query = (
            select(BookCopyModel.book_id)
            .select_from(BookBorrowModel)
            .join(BookCopyModel, BookBorrowModel.book_copy_id == BookCopyModel.id)
            .where(
                and_(
                    BookBorrowModel.user_id == user_id,
                    BookBorrowModel.returned == False,
                    BookBorrowModel.deleted == False,
                )
            )
            .distinct()
        )

        result = await self.db.execute(currently_borrowed_query)
        currently_borrowed_book_ids = [row[0] for row in result.fetchall()]

        if not currently_borrowed_book_ids:
            return []

        genre_query = (
            select(BooksGenreModel.genre_id)
            .where(BooksGenreModel.book_id.in_(currently_borrowed_book_ids))
            .distinct()
        )
        result = await self.db.execute(genre_query)
        genre_ids = [row[0] for row in result.fetchall()]

        if not genre_ids:
            return []

        recommendations_query = (
            select(BooksGenreModel.book_id)
            .where(
                and_(
                    BooksGenreModel.genre_id.in_(genre_ids),
                    BooksGenreModel.book_id.notin_(currently_borrowed_book_ids),
                )
            )
            .distinct()
            .limit(limit)
        )

        result = await self.db.execute(recommendations_query)
        recommended_book_ids = [row[0] for row in result.fetchall()]

        print(f"recommended_book_ids: {recommended_book_ids}")

        get_books_query = (
            select(BookModel)
            .where(and_(BookModel.id.in_(recommended_book_ids)))
            .distinct()
            .limit(limit)
        )

        result = await self.db.execute(get_books_query)

        print(f"\nresult: {result}\n")
        recommendations = result.scalars().unique().all()

        recommended_books = [
            self.entity.model_validate(book) for book in recommendations
        ]

        return recommended_books

    async def get_top_overdues(self, limit: int) -> List[BookBorrow]:
        query = (
            select(self.model)
            .where(
                and_(
                    self.model.deleted == False,
                    self.model.returned == False,
                    self.model.due_date < datetime.now(),
                )
            )
            .limit(limit)
        )

        result = await self.db.execute(query)
        overdue_books = result.scalars().unique().all()
        top_overdue_books = [self.entity.model_validate(row) for row in overdue_books]
        return top_overdue_books
