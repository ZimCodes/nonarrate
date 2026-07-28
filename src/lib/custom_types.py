from enum import Enum, auto
from dataclasses import dataclass


class FilterTag(Enum):
    KEEP_NARRATION = "--keep-narr"
    KEEP_COMMON_OBJ_CHARS = "--keep-common-obj-chars"
    KEEP_ITALIC = "--keep-italic"
    KEEP_PARENTHESIS = "--keep-parenthesis"
    KEEP_COMMON_QUOTED_CHARS = "--keep-common-quoted-chars"
    KEEP_EMPTY_QUOTED_CHARS = "--keep-empty-quoted-chars"
    KEEP_EMPTY_OBJ_CHARS = "--keep-empty-obj-chars"
    KEEP_EXPRESSION_CUES = "--keep-cues"
    KEEP_PUNCTUATIONS = "--keep-punctuations"
    KEEP_GUILLEMETS = "--keep-guillemets"
    KEEP_NVL = "--keep-nvl"
    TEXT_TAGS = "--text-tags"
    QUOTED_CHARS = "--quoted-chars"
    OBJ_CHARS = "--obj-chars"
    RENPY_VARS = "--renpy-vars"
    PYTHON_VARS = "--python-vars"

class MultiLineType(Enum):
    NONE = 0
    SINGLE_QUOTE = auto()
    TRIPLE_QUOTE = auto()
    VALID_TRIPLE_QUOTE = auto()
    VALID_SINGLE_QUOTE = auto()

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
