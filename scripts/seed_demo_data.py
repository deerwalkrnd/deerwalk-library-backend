"""Seed a realistic demo dataset for the Deerwalk Library system.

Wipes the domain tables (but keeps the seeded librarian account) and re-seeds,
so it is safe to re-run before a demo.

Run from the backend root:
    .venv/Scripts/python.exe -m scripts.seed_demo_data
"""

import asyncio
import random
import struct
import zlib
from datetime import datetime, timedelta
from pathlib import Path

from sqlalchemy import delete, select

from app.core.dependencies.database import SessionLocal
from app.core.dependencies.get_settings import get_settings
from app.core.models.book import BookCategoryType, BookModel
from app.core.models.book_borrow import BookBorrowModel, FineStatus
from app.core.models.book_copy import BookCopyModel
from app.core.models.book_review import BookReviewModel
from app.core.models.bookmark import BookmarkModel
from app.core.models.books_genre import BooksGenreModel
from app.core.models.event import EventModel
from app.core.models.feedback import FeedbackModel
from app.core.models.genre import GenreModel
from app.core.models.quote import QuoteModel
from app.core.models.recommendation import RecommendationModel
from app.core.models.reserve import BookReserveEnum, ReserveModel
from app.core.models.users import UserModel, UserRole
from app.modules.auth.infra.services.argon2_hasher import Argon2PasswordHasher

random.seed(20260920)
NOW = datetime.now()
SETTINGS = get_settings()
FINE_RATE = SETTINGS.default_fine_amount
MEDIA_ROOT = Path(SETTINGS.upload_dir)
MEDIA_BASE = SETTINGS.media_base_url.rstrip("/")


# --------------------------------------------------------------------------
# Local cover generation (pure-python PNG, so the demo needs no internet and
# exercises the new local-disk storage path instead of S3).
# --------------------------------------------------------------------------
def _png(path: Path, width: int, height: int, top: tuple, bottom: tuple) -> None:
    raw = bytearray()
    for y in range(height):
        t = y / max(height - 1, 1)
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        raw.append(0)  # filter type: none
        for x in range(width):
            # subtle diagonal sheen so covers don't read as flat blocks
            s = 18 if (x + y * 2) % 140 < 8 else 0
            raw += bytes((min(r + s, 255), min(g + s, 255), min(b + s, 255)))

    def chunk(tag: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(bytes(raw), 6))
        + chunk(b"IEND", b"")
    )


PALETTE = [
    ((38, 70, 121), (17, 32, 58)),
    ((123, 46, 62), (58, 20, 29)),
    ((28, 94, 86), (12, 44, 40)),
    ((104, 71, 26), (52, 34, 10)),
    ((72, 48, 110), (33, 22, 52)),
    ((26, 82, 118), (11, 38, 56)),
    ((110, 58, 40), (52, 26, 17)),
    ((44, 88, 48), (20, 42, 22)),
]


def make_cover(slug: str, idx: int, w: int = 300, h: int = 420) -> str:
    rel = f"book-cover/{slug}.png"
    _png(MEDIA_ROOT / rel, w, h, *PALETTE[idx % len(PALETTE)])
    return f"{MEDIA_BASE}/media/{rel}"


# --------------------------------------------------------------------------
# Source data
# --------------------------------------------------------------------------
GENRES = [
    "Fiction",
    "Non-Fiction",
    "Science",
    "History",
    "Biography",
    "Mystery",
    "Fantasy",
    "Poetry",
]

A = BookCategoryType.ACADEMIC
N = BookCategoryType.NON_ACADEMIC
R = BookCategoryType.REFERENCE

# title, author, publication, category, grade, [genres]
BOOKS = [
    ("Things Fall Apart", "Chinua Achebe", "Heinemann", N, "9", ["Fiction"]),
    ("To Kill a Mockingbird", "Harper Lee", "J. B. Lippincott", N, "9", ["Fiction"]),
    ("Palpasa Cafe", "Narayan Wagle", "Nepa~laya", N, "10", ["Fiction"]),
    ("Seto Dharti", "Amar Neupane", "FinePrint", N, "10", ["Fiction"]),
    ("1984", "George Orwell", "Secker & Warburg", N, "11", ["Fiction", "Mystery"]),
    ("Animal Farm", "George Orwell", "Secker & Warburg", N, "8", ["Fiction"]),
    ("The Hobbit", "J. R. R. Tolkien", "Allen & Unwin", N, "7", ["Fantasy"]),
    (
        "Harry Potter and the Philosopher's Stone",
        "J. K. Rowling",
        "Bloomsbury",
        N,
        "6",
        ["Fantasy"],
    ),
    ("The Alchemist", "Paulo Coelho", "HarperTorch", N, "9", ["Fiction"]),
    (
        "A Brief History of Time",
        "Stephen Hawking",
        "Bantam Books",
        N,
        "11",
        ["Science", "Non-Fiction"],
    ),
    ("Cosmos", "Carl Sagan", "Random House", N, "11", ["Science", "Non-Fiction"]),
    (
        "Sapiens: A Brief History of Humankind",
        "Yuval Noah Harari",
        "Harper",
        N,
        "12",
        ["History", "Non-Fiction"],
    ),
    (
        "The Diary of a Young Girl",
        "Anne Frank",
        "Contact Publishing",
        N,
        "8",
        ["Biography", "History"],
    ),
    ("Wings of Fire", "A. P. J. Abdul Kalam", "Universities Press", N, "9", ["Biography"]),
    (
        "The Story of My Experiments with Truth",
        "M. K. Gandhi",
        "Navajivan",
        N,
        "11",
        ["Biography"],
    ),
    ("Gitanjali", "Rabindranath Tagore", "Macmillan", N, "10", ["Poetry"]),
    ("Muna Madan", "Laxmi Prasad Devkota", "Sajha Prakashan", N, "8", ["Poetry"]),
    (
        "The Adventures of Sherlock Holmes",
        "Arthur Conan Doyle",
        "George Newnes",
        N,
        "8",
        ["Mystery"],
    ),
    (
        "Murder on the Orient Express",
        "Agatha Christie",
        "Collins Crime Club",
        N,
        "10",
        ["Mystery"],
    ),
    ("Concepts of Physics, Volume 1", "H. C. Verma", "Bharati Bhawan", A, "11", ["Science"]),
    ("Fundamentals of Physics", "Halliday & Resnick", "Wiley", A, "12", ["Science"]),
    ("Organic Chemistry", "Morrison & Boyd", "Pearson", A, "12", ["Science"]),
    (
        "Higher Engineering Mathematics",
        "B. S. Grewal",
        "Khanna Publishers",
        A,
        "12",
        ["Science"],
    ),
    (
        "Introduction to Algorithms",
        "Cormen, Leiserson, Rivest & Stein",
        "MIT Press",
        A,
        "12",
        ["Science", "Non-Fiction"],
    ),
    ("Campbell Biology", "Urry, Cain & Wasserman", "Pearson", A, "12", ["Science"]),
    (
        "A History of Nepal",
        "John Whelpton",
        "Cambridge University Press",
        A,
        "11",
        ["History"],
    ),
    (
        "Oxford Advanced Learner's Dictionary",
        "A. S. Hornby",
        "Oxford University Press",
        R,
        "-",
        ["Non-Fiction"],
    ),
    (
        "Encyclopaedia Britannica, Volume 4",
        "Britannica Editors",
        "Encyclopaedia Britannica",
        R,
        "-",
        ["Non-Fiction"],
    ),
    (
        "Oxford Atlas of the World",
        "Oxford Cartographers",
        "Oxford University Press",
        R,
        "-",
        ["Non-Fiction", "History"],
    ),
    ("Roget's Thesaurus", "Peter Mark Roget", "Penguin", R, "-", ["Non-Fiction"]),
]

STUDENTS = [
    ("Aarav Shrestha", "DSS-2024-001", "aarav.shrestha", "2027", "Grade 10"),
    ("Priya Koirala", "DSS-2024-002", "priya.koirala", "2027", "Grade 10"),
    ("Bibek Khadka", "DSS-2024-003", "bibek.khadka", "2026", "Grade 11"),
    ("Anisha Gurung", "DSS-2024-004", "anisha.gurung", "2026", "Grade 11"),
    ("Nirajan Thapa", "DSS-2024-005", "nirajan.thapa", "2025", "Grade 12"),
    ("Ritika Adhikari", "DSS-2024-006", "ritika.adhikari", "2025", "Grade 12"),
    ("Roshan Bista", "DSS-2024-007", "roshan.bista", "2028", "Grade 9"),
    ("Smriti Sharma", "DSS-2024-008", "smriti.sharma", "2028", "Grade 9"),
    ("Krishna Maharjan", "DSS-2024-009", "krishna.maharjan", "2027", "Grade 10"),
    ("Sujata Rai", "DSS-2024-010", "sujata.rai", "2026", "Grade 11"),
    ("Prabin Lamichhane", "DSS-2024-011", "prabin.lamichhane", "2025", "Grade 12"),
    ("Manisha Tamang", "DSS-2024-012", "manisha.tamang", "2028", "Grade 9"),
]

REVIEW_TEXTS = [
    "Genuinely hard to put down once the second half picks up.",
    "Clear explanations and the diagrams actually help. Recommended before exams.",
    "A bit dense in the middle chapters, but worth finishing.",
    "My favourite read this term. The ending surprised me.",
    "Good reference, though some chapters assume a lot of background.",
    "Beautifully written. I reread the last chapter twice.",
    "Helpful for the practical work, less so for the theory.",
    "The historical context sections were the most interesting part.",
    "Solid introduction, though some examples feel dated now.",
    "Loved the characters. Borrowed the sequel straight after.",
]

QUOTES = [
    ("A room without books is like a body without a soul.", "Marcus Tullius Cicero"),
    ("The more that you read, the more things you will know.", "Dr. Seuss"),
    ("Books are a uniquely portable magic.", "Stephen King"),
    ("There is no friend as loyal as a book.", "Ernest Hemingway"),
    ("Reading is to the mind what exercise is to the body.", "Joseph Addison"),
    ("A reader lives a thousand lives before he dies.", "George R. R. Martin"),
]

# name, description, days from today, venue
EVENTS = [
    (
        "Book Week 2026",
        "A week of author talks, reading circles and an inter-house quiz.",
        6,
        "Library Hall",
    ),
    (
        "Poetry Recital Evening",
        "Students perform Nepali and English poetry from the collection.",
        13,
        "Auditorium",
    ),
    (
        "Reading Marathon",
        "Sustained silent reading challenge across grades 6 to 12.",
        27,
        "Library, Floor 2",
    ),
    (
        "Library Orientation for Grade 6",
        "Introduction to the catalogue, borrowing rules and the new portal.",
        -24,
        "Library Hall",
    ),
]

# recommender, designation, book title, note
RECOMMENDATIONS = [
    (
        "Deerwalk Library",
        "Head Librarian",
        "Sapiens: A Brief History of Humankind",
        "Librarian's pick for Grade 12 this month.",
    ),
    (
        "Sabina Pradhan",
        "English Faculty",
        "The Hobbit",
        "A perfect starting point for the Fantasy shelf.",
    ),
    (
        "Deerwalk Library",
        "Head Librarian",
        "Wings of Fire",
        "Requested repeatedly by Grade 9 - now stocked with extra copies.",
    ),
    (
        "Rajesh Karki",
        "Physics Faculty",
        "Cosmos",
        "Pairs well with the Grade 11 physics syllabus.",
    ),
    (
        "Deerwalk Library",
        "Head Librarian",
        "Muna Madan",
        "A short Nepali classic every student should read once.",
    ),
]

# subject, body
FEEDBACKS = [
    ("Borrowing period", "Could we extend the borrowing period during exam months?"),
    ("New portal", "The new portal is much easier than the register book. Thank you."),
    ("More copies", "Please add more copies of Concepts of Physics - always issued out."),
    ("Study space", "Would love a quiet study corner near the reference section."),
]


async def main() -> None:
    db = SessionLocal()
    hasher = Argon2PasswordHasher()

    try:
        # ---- wipe domain tables, keep the seeded librarian ----------------
        for model in (
            BookReviewModel,
            BookmarkModel,
            BookBorrowModel,
            ReserveModel,
            BooksGenreModel,
            BookCopyModel,
            BookModel,
            GenreModel,
            EventModel,
            QuoteModel,
            RecommendationModel,
            FeedbackModel,
        ):
            await db.execute(delete(model))
        await db.execute(delete(UserModel).where(UserModel.role == UserRole.STUDENT))
        await db.commit()

        # ---- genres -------------------------------------------------------
        genres = {}
        for i, title in enumerate(GENRES):
            g = GenreModel(
                title=title,
                image_url=make_cover(f"genre-{title.lower()}", i, 400, 260),
            )
            db.add(g)
            genres[title] = g
        await db.flush()

        # ---- books + copies ----------------------------------------------
        books = []
        copies = []
        for i, (title, author, pub, cat, grade, gnames) in enumerate(BOOKS):
            slug = "".join(c if c.isalnum() else "-" for c in title.lower())
            slug = slug[:40].strip("-")
            book = BookModel(
                title=title,
                author=author,
                publication=pub,
                category=cat,
                grade=grade,
                isbn=(
                    f"978-{random.randint(0, 9)}-{random.randint(100, 999)}"
                    f"-{random.randint(10000, 99999)}-{random.randint(0, 9)}"
                ),
                cover_image_url=make_cover(slug, i),
            )
            db.add(book)
            await db.flush()
            books.append(book)

            for gname in gnames:
                db.add(BooksGenreModel(book_id=book.id, genre_id=genres[gname].id))

            prefix = "".join(w[0] for w in title.split()[:3] if w[0].isalpha()).upper()
            prefix = prefix or "BK"
            for c in range(random.randint(2, 4)):
                copy = BookCopyModel(
                    book_id=book.id,
                    unique_identifier=f"{prefix}-{1000 + i * 10 + c}",
                    is_available=True,
                    condition=random.choice(["New", "Good", "Good", "Fair", "Poor"]),
                )
                db.add(copy)
                copies.append(copy)
        await db.flush()

        # ---- students -----------------------------------------------------
        pw = await hasher.hash_password("Student123!")
        students = []
        for name, roll, handle, gy, section in STUDENTS:
            s = UserModel(
                name=name,
                roll_number=roll,
                email=f"{handle}@sifal.deerwalk.edu.np",
                password=pw,
                role=UserRole.STUDENT,
                graduating_year=gy,
                user_metadata={"section": section},
            )
            db.add(s)
            students.append(s)
        await db.flush()

        librarian = (
            (
                await db.execute(
                    select(UserModel).where(UserModel.role == UserRole.LIBRARIAN)
                )
            )
            .scalars()
            .first()
        )
        # Read now: attributes expire after commit and would trigger lazy IO.
        librarian_email = librarian.email if librarian else "MISSING"

        # ---- borrow history (returned) ------------------------------------
        pool = copies[:]
        random.shuffle(pool)
        cursor = 0

        for _ in range(46):
            copy = pool[cursor % len(pool)]
            cursor += 1
            student = random.choice(students)
            issued = NOW - timedelta(days=random.randint(35, 240))
            due = issued + timedelta(days=14)
            late = random.random() < 0.28
            if late:
                returned_on = due + timedelta(days=random.randint(1, 9))
            else:
                returned_on = due - timedelta(days=random.randint(0, 10))
            overdue_days = max((returned_on - due).days, 0)
            fine = FINE_RATE * overdue_days
            db.add(
                BookBorrowModel(
                    book_copy_id=copy.id,
                    user_id=student.uuid,
                    fine_accumulated=fine,
                    fine_status=FineStatus.PAID if fine else FineStatus.DISABLED,
                    times_renewable=3,
                    times_renewed=random.choice([0, 0, 1]),
                    due_date=due,
                    returned=True,
                    returned_date=returned_on,
                    fine_rate=FINE_RATE,
                    remark=(
                        "Returned late; fine settled."
                        if late
                        else "Returned in good condition."
                    ),
                )
            )

        # ---- currently issued (including overdue) -------------------------
        cursor = cursor % len(pool)
        active = pool[cursor : cursor + 19]
        overdue_set = {id(c) for c in active[:6]}

        for copy in active:
            student = random.choice(students)
            if id(copy) in overdue_set:
                days_over = random.randint(2, 21)
                due = NOW - timedelta(days=days_over)
                fine = FINE_RATE * days_over
                status = FineStatus.UNPAID
            else:
                due = NOW + timedelta(days=random.randint(1, 13))
                fine = 0
                status = FineStatus.DISABLED

            copy.is_available = False
            db.add(
                BookBorrowModel(
                    book_copy_id=copy.id,
                    user_id=student.uuid,
                    fine_accumulated=fine,
                    fine_status=status,
                    times_renewable=3,
                    times_renewed=random.choice([0, 0, 1, 2]),
                    due_date=due,
                    returned=False,
                    fine_rate=FINE_RATE,
                )
            )

        # ---- reserves ------------------------------------------------------
        for copy in pool[cursor + 19 : cursor + 26]:
            db.add(
                ReserveModel(
                    book_copy_id=copy.id,
                    user_id=random.choice(students).uuid,
                    state=BookReserveEnum.RESERVED,
                    due=NOW + timedelta(days=random.randint(1, 3)),
                    remarks="Collect from the issue desk within 3 days.",
                )
            )

        # ---- reviews / bookmarks -------------------------------------------
        seen = set()
        for _ in range(30):
            book = random.choice(books)
            student = random.choice(students)
            if (book.id, student.uuid) in seen:
                continue
            seen.add((book.id, student.uuid))
            db.add(
                BookReviewModel(
                    book_id=book.id,
                    user_id=student.uuid,
                    review_text=random.choice(REVIEW_TEXTS),
                    is_spam=False,
                )
            )

        marked = set()
        for _ in range(34):
            book = random.choice(books)
            student = random.choice(students)
            if (book.id, student.uuid) in marked:
                continue
            marked.add((book.id, student.uuid))
            db.add(BookmarkModel(book_id=book.id, user_id=student.uuid))

        # ---- events / quotes / recommendations / feedback -------------------
        for i, (name, desc, offset, venue) in enumerate(EVENTS):
            db.add(
                EventModel(
                    name=name,
                    description=desc,
                    event_date=NOW + timedelta(days=offset),
                    venue=venue,
                    image_url=make_cover(f"event-{i}", i + 3, 640, 320),
                )
            )

        for text, author in QUOTES:
            db.add(QuoteModel(quote=text, author=author))

        for i, (name, designation, book_title, note) in enumerate(RECOMMENDATIONS):
            db.add(
                RecommendationModel(
                    name=name,
                    designation=designation,
                    book_title=book_title,
                    note=note,
                    cover_image_url=make_cover(f"rec-{i}", i + 1),
                )
            )

        for i, (subject, text) in enumerate(FEEDBACKS):
            db.add(
                FeedbackModel(
                    user_id=students[i].uuid,
                    subject=subject,
                    feedback=text,
                    is_acknowledged=(i == 1),
                )
            )

        await db.commit()

        print("Demo data seeded.")
        print(f"  librarian : {librarian_email}")
        print(f"  students  : {len(students)}  (password: Student123!)")
        print(f"  books     : {len(books)}   copies: {len(copies)}")
        print(f"  issued    : {len(active)}  (6 overdue)  history: 46 returned")

    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(main())
