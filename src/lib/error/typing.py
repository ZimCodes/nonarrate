from dataclasses import dataclass
import enum


class ErrorType(enum.StrEnum):
    """Represents types of error messages."""

    NON_EMPTY = "non-empty"
    INDENTED_LINE = "Line is indented"
    EXPECTED_STATEMENT = "expected statement"
    INDENT_MISMATCH = "[Ii]ndentation mismatch"
    DUPLICATE = enum.auto()
    MENU_NO_CHOICES = "Menu does not contain any choices"


@dataclass
class RenpyError:
    """Represents an error from the 'errors.txt' file."""

    file_loc: str | None
    line_num: int | None
    category: ErrorType | None
