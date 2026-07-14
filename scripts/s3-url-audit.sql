-- =============================================================================
-- s3-url-audit.sql  —  READ-ONLY audit of leftover AWS S3 URLs in the database
-- =============================================================================
--
-- PURPOSE
--   We are removing AWS S3 from the Deerwalk Library backend. Uploaded file
--   URLs (book covers, profile images, event banners) were historically stored
--   in the database as ABSOLUTE S3 URLs, e.g.:
--       https://<bucket>.s3.<region>.amazonaws.com/book-cover/<file>
--   This script counts how many rows still hold such URLs so we can decide
--   Phase B of the migration:
--       - many real rows  -> re-host the files and rewrite the URLs
--       - few/none        -> reset to placeholders
--
-- WHAT IT CHECKS
--   1. The three known columns:
--        books.cover_image_url, users.image_url, events.image_url
--      For each: total row count, count matching '%amazonaws.com%', 5 samples.
--   2. A schema-wide safety net: EVERY text / varchar / char column in every
--      non-system schema is scanned for 'amazonaws.com', so nothing is missed
--      if the earlier audit overlooked a table/column.
--
-- SAFETY
--   * SELECT-only. No INSERT / UPDATE / DELETE / DDL.
--   * The whole script runs inside a READ ONLY transaction that is ROLLBACK'd,
--     so the server will reject any accidental write.
--
-- HOW TO RUN (devops, against PRODUCTION, ideally with a read-only role)
--   psql "postgresql://<user>:<pass>@<host>:<port>/<dbname>" -f scripts/s3-url-audit.sql
--   or:
--   psql -h <host> -U <user> -d <dbname> -f scripts/s3-url-audit.sql
--
--   Tip: capture the output ->  ... -f scripts/s3-url-audit.sql > s3-audit-output.txt
--   Please send the full output back so we can finalize Phase B.
--
-- NOTES
--   * Uses psql's \gexec meta-command, so it MUST be run with the psql client
--     (not a generic SQL runner / GUI that ignores backslash commands).
--   * ON_ERROR_STOP is OFF so a missing table (unlikely in prod) won't abort
--     the rest of the report.
-- =============================================================================

\set ON_ERROR_STOP off
\pset pager off
\timing off

BEGIN TRANSACTION READ ONLY;

\echo '======================================================================'
\echo 'STEP 0: environment'
\echo '======================================================================'
SELECT current_database() AS database,
       current_user       AS connected_as,
       now()              AS run_at;

\echo ''
\echo '======================================================================'
\echo 'STEP 1: known columns — totals and amazonaws.com counts'
\echo '======================================================================'

SELECT 'books.cover_image_url' AS location,
       count(*)                                                   AS total_rows,
       count(*) FILTER (WHERE cover_image_url LIKE '%amazonaws.com%') AS s3_rows,
       count(*) FILTER (WHERE cover_image_url IS NOT NULL AND cover_image_url <> '') AS non_empty_rows
FROM books
UNION ALL
SELECT 'users.image_url',
       count(*),
       count(*) FILTER (WHERE image_url LIKE '%amazonaws.com%'),
       count(*) FILTER (WHERE image_url IS NOT NULL AND image_url <> '')
FROM users
UNION ALL
SELECT 'events.image_url',
       count(*),
       count(*) FILTER (WHERE image_url LIKE '%amazonaws.com%'),
       count(*) FILTER (WHERE image_url IS NOT NULL AND image_url <> '')
FROM events;

\echo ''
\echo '--- sample S3 URLs (up to 5 each) to reveal bucket / region / path pattern ---'
SELECT 'books.cover_image_url' AS location, cover_image_url AS url
FROM books WHERE cover_image_url LIKE '%amazonaws.com%' LIMIT 5;

SELECT 'users.image_url' AS location, image_url AS url
FROM users WHERE image_url LIKE '%amazonaws.com%' LIMIT 5;

SELECT 'events.image_url' AS location, image_url AS url
FROM events WHERE image_url LIKE '%amazonaws.com%' LIMIT 5;

\echo ''
\echo '======================================================================'
\echo 'STEP 2: schema-wide scan — ANY text/varchar/char column containing'
\echo '        amazonaws.com (only columns WITH matches are printed)'
\echo '======================================================================'
\echo '(list of candidate text columns being scanned:)'

SELECT table_schema, table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
  AND data_type IN ('character varying', 'text', 'character')
ORDER BY table_schema, table_name, column_name;

\echo ''
\echo '(per-column match counts — rows appear only where s3_rows > 0:)'

-- Generate one aggregate query per candidate column and execute it with \gexec.
-- Each generated query returns a single row ONLY when that column has at least
-- one 'amazonaws.com' match (HAVING count(*) > 0), so clean columns stay silent.
SELECT format(
         'SELECT %L AS table_ref, %L AS column_name, count(*) AS s3_rows '
         'FROM %I.%I WHERE %I::text LIKE ''%%amazonaws.com%%'' HAVING count(*) > 0',
         table_schema || '.' || table_name,
         column_name,
         table_schema, table_name, column_name
       )
FROM information_schema.columns
WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
  AND data_type IN ('character varying', 'text', 'character')
ORDER BY table_schema, table_name, column_name
\gexec

\echo ''
\echo '======================================================================'
\echo 'Audit complete. Transaction will be rolled back (no changes made).'
\echo '======================================================================'

ROLLBACK;
