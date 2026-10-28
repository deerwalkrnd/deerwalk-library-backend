-- =============================================================================
-- wipe-books.sql  —  DESTRUCTIVE: remove every book so the catalogue can be
--                    re-imported from the library register.
-- =============================================================================
--
-- REMOVES
--   books, book_copies, books_genre (genre links), bookmarks, book_reviews,
--   book_borrows (ALL loan history, including books currently checked out),
--   book_reserves.
--
-- KEEPS
--   users, genres, events, quotes, recommendations, feedbacks.
--
-- Covers already uploaded stay on disk under media/book-cover/; delete that
-- folder separately if you want it empty too.
--
-- RUN
--   1. Back up first:
--        pg_dump -h localhost -p 5435 -U dev-user -Fc dev_db > before-wipe.dump
--      (restore with: pg_restore -h localhost -p 5435 -U dev-user -d dev_db --clean before-wipe.dump)
--   2. psql -h localhost -p 5435 -U dev-user -d dev_db -f scripts/wipe-books.sql
--
-- The counts are printed before the wipe. Everything runs in one transaction,
-- and TRUNCATE without CASCADE fails (wiping nothing) if some other table we
-- did not list still points at these ones.
-- =============================================================================

\set ON_ERROR_STOP on

BEGIN;

SELECT 'books' AS table_name, count(*) FROM books
UNION ALL SELECT 'book_copies', count(*) FROM book_copies
UNION ALL SELECT 'book_borrows', count(*) FROM book_borrows
UNION ALL SELECT 'book_borrows (not returned)', count(*) FROM book_borrows WHERE returned IS NOT TRUE
UNION ALL SELECT 'book_reserves', count(*) FROM book_reserves
UNION ALL SELECT 'bookmarks', count(*) FROM bookmarks
UNION ALL SELECT 'book_reviews', count(*) FROM book_reviews;

TRUNCATE TABLE
    book_reserves,
    book_borrows,
    bookmarks,
    book_reviews,
    books_genre,
    book_copies,
    books
RESTART IDENTITY;

COMMIT;

SELECT 'books left' AS check, count(*) FROM books;
