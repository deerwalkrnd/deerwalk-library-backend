import csv
from io import StringIO
from typing import List, Optional, Set, Tuple

from fastapi import UploadFile

from app.core.exc.error_code import ErrorCode
from app.core.exc.library_exception import LibraryException
from app.core.utils.csv_JSON_parser import csv_JSON_parser
from app.core.utils.csv_validator import validate_csv_headers
from app.modules.books.domain.requests.bulk_book_create_request import (
    BulkCreateBookRequest,
)
from app.modules.books.domain.responses.csv_validation_result import (
    CSVValidationResult,
)
from app.modules.books.utils.book_csv_validator import BookCSVValidator


async def validate_book_csv(
    file: UploadFile,
    available_genres: Optional[Set[str]] = None,
) -> Tuple[CSVValidationResult, str]:
    """
    Validates a book CSV file and returns validation result with the content.
    
    Args:
        file: The uploaded CSV file
        available_genres: Optional set of valid genre names for validation
        
    Returns:
        Tuple of (CSVValidationResult, csv_content_string)
    """
    contents = await file.read()
    
    try:
        decoded = contents.decode("utf-8")
    except UnicodeDecodeError:
        try:
            decoded = contents.decode("utf-8-sig")  # Handle BOM
        except UnicodeDecodeError:
            decoded = contents.decode("latin-1")
    
    validator = BookCSVValidator(available_genres=available_genres)
    result = validator.validate_csv_content(decoded)
    
    # Reset file position for potential re-read
    await file.seek(0)
    
    return result, decoded


async def parse_book_csv_to_create_requests(
    file: UploadFile,
    available_genres: Optional[Set[str]] = None,
) -> List[BulkCreateBookRequest]:
    """
    Parses a book CSV file into a list of BulkCreateBookRequest objects.
    
    Args:
        file: The uploaded CSV file
        available_genres: Optional set of valid genre names for validation
        
    Returns:
        List of BulkCreateBookRequest objects
        
    Raises:
        LibraryException: If the CSV is invalid with detailed error message
    """
    # First validate the CSV
    validation_result, decoded = await validate_book_csv(
        file=file,
        available_genres=available_genres,
    )
    
    if not validation_result.is_valid:
        raise LibraryException(
            status_code=400,
            code=ErrorCode.INVALID_FIELDS,
            msg=validation_result.get_error_summary(),
            detail={
                "total_rows": validation_result.total_rows,
                "error_count": len(validation_result.errors),
                "errors": [
                    {
                        "row": err.row_number,
                        "field": err.field,
                        "value": err.value,
                        "message": err.error,
                    }
                    for err in validation_result.errors
                ],
            },
        )
    
    # Parse the validated CSV
    csv_reader = csv.DictReader(StringIO(decoded))
    list_csv_reader = list(csv_reader)
    
    processed_csv = await csv_JSON_parser(
        rows=list_csv_reader, header=["copies", "genres"]
    )

    create_book_requests_model = [
        BulkCreateBookRequest(**row) for row in processed_csv
    ]
    return create_book_requests_model
