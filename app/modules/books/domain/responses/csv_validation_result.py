from typing import List, Optional

from pydantic import BaseModel


class CSVRowError(BaseModel):
    """Represents an error found in a specific CSV row."""

    row_number: int
    field: str
    value: Optional[str] = None
    error: str


class CSVValidationResult(BaseModel):
    """Result of CSV validation containing all errors found."""

    is_valid: bool
    total_rows: int
    errors: List[CSVRowError] = []
    
    def get_error_summary(self) -> str:
        """Returns a human-readable summary of all errors."""
        if self.is_valid:
            return "CSV is valid"
        
        summary_lines = [f"Found {len(self.errors)} error(s) in CSV:"]
        for err in self.errors[:10]:  # Show first 10 errors
            summary_lines.append(
                f"  Row {err.row_number}: '{err.field}' - {err.error}"
            )
        
        if len(self.errors) > 10:
            summary_lines.append(f"  ... and {len(self.errors) - 10} more errors")
        
        return "\n".join(summary_lines)
