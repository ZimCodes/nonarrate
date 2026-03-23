from enum import Enum
from dataclasses import dataclass


class FilterTag(Enum):
    BASIC_NARR = "--basic-narr"
    BASIC_CHAR_OBJ = "--basic-char-obj"
    ITALIC_NARR = "--italic-narr"
    PARENTHESIS_NARR = "--parenthesis-narr"
    BASIC_CHAR = "--basic-char"
    NONE_CHAR_OBJ = "--none-char-obj"
    NO_CUSTOM_TEXT_TAGS = "--no-custom-tags"
    NO_CUSTOM_CHARS = "--no-custom-chars"
    NO_CUSTOM_CHAR_OBJS = "--no-custom-char-objs"


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
