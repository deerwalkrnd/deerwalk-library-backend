from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

from fastapi import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.books.domain.entities.book import Book
from app.modules.books.domain.entities.book_copy import BookCopy
from app.modules.books.domain.entities.books_genre import BooksGenre
from app.modules.books.domain.repositories.book_copy_repository_interface import (
    BookCopyRepositoryInterface,
)
from app.modules.books.domain.repositories.book_repository_interface import (
    BookRepositoryInterface,
)
from app.modules.books.domain.repositories.books_genre_repository_interface import (
    BooksGenreRepositoryInterface,
)
from app.modules.books.domain.requests.bulk_book_create_request import (
    BulkCreateBookCopy,
    BulkCreateBookRequest,
)
from app.modules.books.domain.responses.book_bulk_upload_skip_response import (
    BookBulkUploadSkipResponse,
)
from app.modules.books.domain.services.book_bulk_upload_service_interface import (
    BookBulkUploadResult,
    BookBulkUploadServiceInterface,
)
from app.modules.books.utils.book_import.values import match_key, normalize_isbn
from app.modules.genres.domain.entities.genre import Genre
from app.modules.genres.domain.repositories.genre_repository_interface import (
    GenreRepositoryInterface,
)

# Given to imported books that name no genre (the library register has none).
DEFAULT_GENRE = "Uncategorized"

# Books written per transaction. Large enough that a full register (~12k
# copies) imports in a handful of round trips, small enough that one bad row
# only forces a slow per-book retry of its own batch.
BATCH_SIZE = 250

TitleAuthorKey = Tuple[str, str]


@dataclass
class _NewBook:
    request: BulkCreateBookRequest
    isbn: Optional[str]
    genre_ids: List[int]
    copies: List[BulkCreateBookCopy] = field(default_factory=list)
    book_id: Optional[int] = None  # set once written


@dataclass
class _Batch:
    new_books: List[_NewBook] = field(default_factory=list)
    # Copies for books that were already in the library: (book_id, copy)
    extra_copies: List[Tuple[int, BulkCreateBookCopy]] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.new_books) + len(self.extra_copies)


class BookBulkUploadService(BookBulkUploadServiceInterface):
    """
    Writes parsed import rows to the database.

    A book already in the library (same ISBN, or same title + author when
    there is no ISBN) is not an error: its new copies are added to it, so the
    same register can be re-imported after more rows are typed in. Copies
    whose unique_identifier already exists are left alone.
    """

    def __init__(
        self,
        book_repository: BookRepositoryInterface,
        books_genre_repository: BooksGenreRepositoryInterface,
        book_copy_repository: BookCopyRepositoryInterface,
        genre_repository: GenreRepositoryInterface,
        db: AsyncSession,
    ):
        self.book_repository = book_repository
        self.books_genre_repository = books_genre_repository
        self.book_copy_repository = book_copy_repository
        self.genre_repository = genre_repository
        self.db = db

    async def bulk_upload(
        self, create_book_requests: List[BulkCreateBookRequest]
    ) -> BookBulkUploadResult:
        result = BookBulkUploadResult()
        genre_ids_by_name = await self._load_genres()
        books_by_isbn, books_by_title_author = await self._load_books()
        taken_identifiers = await self.book_copy_repository.get_all_unique_identifiers()
        # New books already queued, so later rows of the same file merge in.
        pending_by_isbn: Dict[str, _NewBook] = {}
        pending_by_title_author: Dict[TitleAuthorKey, _NewBook] = {}
        updated_book_ids: Set[int] = set()
        created_book_ids: Set[int] = set()

        batch = _Batch()
        for request in create_book_requests:
            copies: List[BulkCreateBookCopy] = []
            for copy in request.copies:
                if copy.unique_identifier in taken_identifiers:
                    result.duplicates_ignored += 1
                else:
                    taken_identifiers.add(copy.unique_identifier)
                    copies.append(copy)

            isbn = normalize_isbn(request.isbn)
            title_author = (match_key(request.title), match_key(request.author))

            existing_id = (
                books_by_isbn.get(isbn)
                if isbn
                else books_by_title_author.get(title_author)
            )
            if existing_id is not None:
                if not request.copies:
                    result.skipped.append(
                        self._skip(request, "This book is already in the library")
                    )
                for copy in copies:
                    batch.extra_copies.append((existing_id, copy))
                if copies:
                    updated_book_ids.add(existing_id)
                continue

            pending = (
                pending_by_isbn.get(isbn)
                if isbn
                else pending_by_title_author.get(title_author)
            )
            if pending is not None:
                pending.copies.extend(copies)
                continue

            genre_ids, missing = self._resolve_genres(request.genres, genre_ids_by_name)
            if missing:
                result.skipped.append(
                    self._skip(
                        request,
                        f"Genre '{missing}' does not exist. Create it first or leave genres empty.",
                    )
                )
                continue
            if not genre_ids:
                genre_ids = [await self._default_genre_id(genre_ids_by_name)]

            new_book = _NewBook(
                request=request, isbn=isbn, genre_ids=genre_ids, copies=copies
            )
            if isbn:
                pending_by_isbn[isbn] = new_book
            else:
                pending_by_title_author[title_author] = new_book
            batch.new_books.append(new_book)

            if len(batch) >= BATCH_SIZE:
                await self._write(batch, result)
                # Written books are now ordinary existing books: later rows
                # for them must become extra copies, not edits to a batch
                # that has already gone out.
                for written in batch.new_books:
                    if written.book_id is not None:
                        created_book_ids.add(written.book_id)
                        if written.isbn:
                            books_by_isbn[written.isbn] = written.book_id
                        else:
                            books_by_title_author[
                                (
                                    match_key(written.request.title),
                                    match_key(written.request.author),
                                )
                            ] = written.book_id
                pending_by_isbn.clear()
                pending_by_title_author.clear()
                batch = _Batch()

        await self._write(batch, result)
        result.books_updated = len(updated_book_ids - created_book_ids)
        return result

    async def _load_genres(self) -> Dict[str, int]:
        genres = await self.genre_repository.find_many(
            limit=10_000, offset=0, sort_by="id", descending=False
        )
        return {g.title.strip().casefold(): g.id for g in genres if g.title and g.id}

    async def _load_books(
        self,
    ) -> Tuple[Dict[str, int], Dict[TitleAuthorKey, int]]:
        by_isbn: Dict[str, int] = {}
        by_title_author: Dict[TitleAuthorKey, int] = {}
        for book in await self.book_repository.get_identity_fields_of_all_books():
            if book.id is None:
                continue
            isbn = normalize_isbn(book.isbn)
            if isbn:
                by_isbn.setdefault(isbn, book.id)
            else:
                by_title_author.setdefault(
                    (match_key(book.title), match_key(book.author)), book.id
                )
        return by_isbn, by_title_author

    @staticmethod
    def _resolve_genres(
        names: List[str], genre_ids_by_name: Dict[str, int]
    ) -> Tuple[List[int], Optional[str]]:
        ids: List[int] = []
        for name in names:
            genre_id = genre_ids_by_name.get(name.strip().casefold())
            if genre_id is None:
                return [], name
            if genre_id not in ids:
                ids.append(genre_id)
        return ids, None

    async def _default_genre_id(self, genre_ids_by_name: Dict[str, int]) -> int:
        key = DEFAULT_GENRE.casefold()
        if key not in genre_ids_by_name:
            # create() commits. That is safe here: rows are only staged in
            # the session inside _write, which always commits or rolls back.
            genre = await self.genre_repository.create(Genre(title=DEFAULT_GENRE))
            if genre is None or genre.id is None:
                raise RuntimeError(f"Could not create the '{DEFAULT_GENRE}' genre")
            genre_ids_by_name[key] = genre.id
        return genre_ids_by_name[key]

    async def _write(self, batch: _Batch, result: BookBulkUploadResult) -> None:
        if not len(batch):
            return
        try:
            await self._stage(batch)
            await self.db.commit()
            result.books_created += len(batch.new_books)
            result.copies_added += len(batch.extra_copies) + sum(
                len(b.copies) for b in batch.new_books
            )
            return
        except Exception as e:
            await self.db.rollback()
            for new_book in batch.new_books:
                new_book.book_id = None
            logger.logger.warning(f"Import batch failed ({e}); retrying book by book")

        # Find the offending rows so the rest of the batch still goes in.
        for new_book in batch.new_books:
            try:
                await self._stage(_Batch(new_books=[new_book]))
                await self.db.commit()
                result.books_created += 1
                result.copies_added += len(new_book.copies)
            except Exception as e:
                await self.db.rollback()
                new_book.book_id = None
                result.skipped.append(self._skip(new_book.request, f"Database error: {e}"))
        for book_id, copy in batch.extra_copies:
            try:
                await self._stage(_Batch(extra_copies=[(book_id, copy)]))
                await self.db.commit()
                result.copies_added += 1
            except Exception as e:
                await self.db.rollback()
                result.skipped.append(
                    BookBulkUploadSkipResponse(
                        book_title=copy.unique_identifier,
                        reason=f"Could not add copy: {e}",
                    )
                )

    async def _stage(self, batch: _Batch) -> None:
        book_ids = await self.book_repository.add_many(
            [
                Book(
                    title=b.request.title,
                    author=b.request.author,
                    publication=b.request.publication,
                    isbn=b.isbn,
                    category=b.request.category,
                    grade=b.request.grade,
                    cover_image_url=b.request.cover_image_url,
                )
                for b in batch.new_books
            ]
        )

        copies: List[BookCopy] = [
            BookCopy(
                book_id=book_id,
                unique_identifier=copy.unique_identifier,
                condition=copy.condition,
            )
            for book_id, copy in batch.extra_copies
        ]
        links: List[BooksGenre] = []
        for new_book, book_id in zip(batch.new_books, book_ids):
            new_book.book_id = book_id
            copies.extend(
                BookCopy(
                    book_id=book_id,
                    unique_identifier=copy.unique_identifier,
                    condition=copy.condition,
                )
                for copy in new_book.copies
            )
            links.extend(
                BooksGenre(book_id=book_id, genre_id=genre_id)
                for genre_id in new_book.genre_ids
            )

        if copies:
            await self.book_copy_repository.add_many(copies)
        if links:
            await self.books_genre_repository.add_many(links)

    @staticmethod
    def _skip(request: BulkCreateBookRequest, reason: str) -> BookBulkUploadSkipResponse:
        return BookBulkUploadSkipResponse(
            book_title=request.title,
            reason=reason,
            sheet=request.source_sheet,
            row=request.source_row,
        )
