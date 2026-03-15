from enum import Enum

type FileInfo = dict[str, list[str]]


class FilterTag(Enum):
    NO_BASIC_NARR = "--no-basic-narr"
    NO_BASIC_CHAR_OBJ = "--no-basic-char-obj"
    NO_ITALIC_NARR = "--no-italic-narr"
    NO_PARENTHESIS_NARR = "--no-parenthesis-narr"
    NO_BASIC_CHAR = "--no-basic-char"
    CUSTOM_TEXT_TAG = "--custom-tag"
    CUSTOM_CHAR = "--custom-char"
    CUSTOM_CHAR_OBJ = "--custom-char-obj"
