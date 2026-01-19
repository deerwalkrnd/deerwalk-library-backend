import csv
import json
from io import StringIO
from typing import Any, Dict, List, Optional, Set

from pydantic import ValidationError

from app.core.models.book import BookCategoryType
from app.modules.books.domain.requests.bulk_book_create_request import (
    BulkCreateBookCopy,
    BulkCreateBookRequest,
)
from app.modules.books.domain.responses.csv_validation_result import (
    CSVRowError,
    CSVValidationResult,
)


class BookCSVValidator:
    """
    Validates book CSV files and provides detailed error messages.
    """

    REQUIRED_HEADERS = {
        "title",
        "author",
        "publication",
        "isbn",
        "category",
        "genres",
        "grade",
        "cover_image_url",
        "copies",
    }

    VALID_CATEGORIES = {cat.value for cat in BookCategoryType}

    def __init__(self, available_genres: Optional[Set[str]] = None):
        """
        Initialize validator with optional list of available genre names.
        If provided, genre names will be validated against this list.
        """
        self.available_genres = available_genres

    def validate_csv_content(self, csv_content: str) -> CSVValidationResult:
        """
        Validates the entire CSV content and returns detailed validation result.
        """
        errors: List[CSVRowError] = []

        try:
            csv_reader = csv.DictReader(StringIO(csv_content))
            headers = csv_reader.fieldnames
        except Exception as e:
            return CSVValidationResult(
                is_valid=False,
                total_rows=0,
                errors=[
                    CSVRowError(
                        row_number=0,
                        field="file",
                        error=f"Failed to parse CSV file: {str(e)}",
                    )
                ],
            )

        # Validate headers
        header_errors = self._validate_headers(headers)
        if header_errors:
            return CSVValidationResult(
                is_valid=False,
                total_rows=0,
                errors=header_errors,
            )

        rows = list(csv_reader)
        total_rows = len(rows)

        if total_rows == 0:
            return CSVValidationResult(
                is_valid=False,
                total_rows=0,
                errors=[
                    CSVRowError(
                        row_number=0,
                        field="file",
                        error="CSV file is empty (no data rows found)",
                    )
                ],
            )

        # Validate each row
        for row_idx, row in enumerate(rows):
            row_number = row_idx + 2  # +2 because row 1 is header, and we're 1-indexed
            row_errors = self._validate_row(row, row_number)
            errors.extend(row_errors)

        return CSVValidationResult(
            is_valid=len(errors) == 0,
            total_rows=total_rows,
            errors=errors,
        )

    def _validate_headers(
        self, headers: Optional[List[str]]
    ) -> List[CSVRowError]:
        """Validates CSV headers against required fields."""
        errors: List[CSVRowError] = []

        if not headers:
            errors.append(
                CSVRowError(
                    row_number=1,
                    field="headers",
                    error="CSV file has no headers",
                )
            )
            return errors

        csv_headers = set(headers)
        missing_headers = self.REQUIRED_HEADERS - csv_headers
        extra_headers = csv_headers - self.REQUIRED_HEADERS

        if missing_headers:
            errors.append(
                CSVRowError(
                    row_number=1,
                    field="headers",
                    error=f"Missing required columns: {', '.join(sorted(missing_headers))}",
                )
            )

        if extra_headers:
            errors.append(
                CSVRowError(
                    row_number=1,
                    field="headers",
                    error=f"Unknown columns found: {', '.join(sorted(extra_headers))}",
                )
            )

        return errors

    def _validate_row(
        self, row: Dict[str, Any], row_number: int
    ) -> List[CSVRowError]:
        """Validates a single CSV row."""
        errors: List[CSVRowError] = []

        # Validate required string fields
        required_fields = ["title", "author", "publication", "isbn"]
        for field in required_fields:
            value = row.get(field, "").strip()
            if not value:
                errors.append(
                    CSVRowError(
                        row_number=row_number,
                        field=field,
                        value=row.get(field),
                        error=f"'{field}' is required and cannot be empty",
                    )
                )

        # Validate category
        category_value = row.get("category", "").strip()
        if not category_value:
            errors.append(
                CSVRowError(
                    row_number=row_number,
                    field="category",
                    value=category_value,
                    error="'category' is required and cannot be empty",
                )
            )
        elif category_value not in self.VALID_CATEGORIES:
            errors.append(
                CSVRowError(
                    row_number=row_number,
                    field="category",
                    value=category_value,
                    error=(
                        f"Invalid category '{category_value}'. "
                        f"Must be one of: {', '.join(sorted(self.VALID_CATEGORIES))}"
                    ),
                )
            )

        # Validate genres (JSON array of strings)
        genres_errors = self._validate_genres_field(row, row_number)
        errors.extend(genres_errors)

        # Validate copies (JSON array of objects)
        copies_errors = self._validate_copies_field(row, row_number)
        errors.extend(copies_errors)

        return errors

    def _validate_genres_field(
        self, row: Dict[str, Any], row_number: int
    ) -> List[CSVRowError]:
        """Validates the genres field."""
        errors: List[CSVRowError] = []
        genres_value = row.get("genres", "").strip()

        if not genres_value:
            errors.append(
                CSVRowError(
                    row_number=row_number,
                    field="genres",
                    value=genres_value,
                    error="'genres' is required. Provide a JSON array of genre names, e.g., [\"Fiction\", \"Drama\"]",
                )
            )
            return errors

        try:
            genres = json.loads(genres_value)
        except json.JSONDecodeError as e:
            errors.append(
                CSVRowError(
                    row_number=row_number,
                    field="genres",
                    value=genres_value,
                    error=(
                        f"Invalid JSON format for 'genres': {str(e)}. "
                        "Expected format: [\"Genre1\", \"Genre2\"]"
                    ),
                )
            )
            return errors

        if not isinstance(genres, list):
            errors.append(
                CSVRowError(
                    row_number=row_number,
                    field="genres",
                    value=genres_value,
                    error="'genres' must be a JSON array, e.g., [\"Fiction\", \"Drama\"]",
                )
            )
            return errors

        if len(genres) == 0:
            errors.append(
                CSVRowError(
                    row_number=row_number,
                    field="genres",
                    value=genres_value,
                    error="'genres' must contain at least one genre name",
                )
            )
            return errors

        for idx, genre in enumerate(genres):
            if not isinstance(genre, str):
                errors.append(
                    CSVRowError(
                        row_number=row_number,
                        field="genres",
                        value=str(genre),
                        error=f"Genre at index {idx} must be a string, got {type(genre).__name__}",
                    )
                )
            elif not genre.strip():
                errors.append(
                    CSVRowError(
                        row_number=row_number,
                        field="genres",
                        value=genre,
                        error=f"Genre at index {idx} cannot be empty",
                    )
                )
            elif self.available_genres and genre not in self.available_genres:
                errors.append(
                    CSVRowError(
                        row_number=row_number,
                        field="genres",
                        value=genre,
                        error=f"Genre '{genre}' does not exist in the database",
                    )
                )

        return errors

    def _validate_copies_field(
        self, row: Dict[str, Any], row_number: int
    ) -> List[CSVRowError]:
        """Validates the copies field."""
        errors: List[CSVRowError] = []
        copies_value = row.get("copies", "").strip()

        # Copies is optional, empty is valid
        if not copies_value or copies_value == "[]":
            return errors

        try:
            copies = json.loads(copies_value)
        except json.JSONDecodeError as e:
            errors.append(
                CSVRowError(
                    row_number=row_number,
                    field="copies",
                    value=copies_value,
                    error=(
                        f"Invalid JSON format for 'copies': {str(e)}. "
                        "Expected format: [{\"unique_identifier\": \"COPY001\", \"condition\": \"good\"}]"
                    ),
                )
            )
            return errors

        if not isinstance(copies, list):
            errors.append(
                CSVRowError(
                    row_number=row_number,
                    field="copies",
                    value=copies_value,
                    error="'copies' must be a JSON array",
                )
            )
            return errors

        for idx, copy in enumerate(copies):
            if not isinstance(copy, dict):
                errors.append(
                    CSVRowError(
                        row_number=row_number,
                        field="copies",
                        value=str(copy),
                        error=f"Copy at index {idx} must be an object with 'unique_identifier'",
                    )
                )
                continue

            if "unique_identifier" not in copy:
                errors.append(
                    CSVRowError(
                        row_number=row_number,
                        field="copies",
                        value=str(copy),
                        error=f"Copy at index {idx} is missing required field 'unique_identifier'",
                    )
                )
            elif not copy["unique_identifier"]:
                errors.append(
                    CSVRowError(
                        row_number=row_number,
                        field="copies",
                        value=str(copy),
                        error=f"Copy at index {idx} has empty 'unique_identifier'",
                    )
                )

        return errors
