from enum import Enum
from dataclasses import dataclass


class FilterTag(Enum):
    NO_BASIC_NARR = "--no-basic-narr"
    NO_BASIC_CHAR_OBJ = "--no-basic-char-obj"
    NO_ITALIC_NARR = "--no-italic-narr"
    NO_PARENTHESIS_NARR = "--no-parenthesis-narr"
    NO_BASIC_CHAR = "--no-basic-char"
    CUSTOM_TEXT_TAG = "--custom-tag"
    CUSTOM_CHAR = "--custom-char"
    CUSTOM_CHAR_OBJ = "--custom-char-obj"


@dataclass
class FileInfo:
    """Class to hold file information."""

    url: str
    lines: list[str]


@dataclass
class RenpyError:
    """Represents an error from the 'errors.txt' file."""

    file_loc: str | None
    line_num: int | None
    category: str | None
