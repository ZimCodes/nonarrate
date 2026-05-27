from typing import final


@final
class LineInfo:
    """Holds line information from a file."""
    __DOUBLE_QUOTE: str = '"'
    __SINGLE_QUOTE: str = "'"
    __HASH: str = '#'
    __SINGLE_TRIPLE_QUOTE = "'''"
    __DOUBLE_TRIPLE_QUOTE = '"""'

    def __init__(self, line: str | None = None) -> None:
        if line is not None:
            self._strip_line = LineInfo.__strip_inline_comment(line.strip())
            self._is_comment = LineInfo.__is_a_comment(self._strip_line)
            self._is_triple_quote_start = LineInfo.__startswith_triple_quote(self._strip_line)
            self._is_triple_quote_end = LineInfo.__endswith_triple_quote(self._strip_line)
            self._has_triple_quote = LineInfo.__has_triple_quote(self._strip_line)
            self._is_menu = LineInfo.__is_choice_menu(self._strip_line)

    @staticmethod
    def __can_remove_hash(hash_index: int, double_quote_index: int, single_quote_index: int) -> bool:
        return (double_quote_index != -1 and hash_index > double_quote_index) or (
                single_quote_index != -1 and hash_index > single_quote_index)

    @classmethod
    def __strip_inline_comment(cls, strip_line: str) -> str:
        most_hash_index = strip_line.rfind(cls.__HASH)
        least_hash_index = strip_line.find(cls.__HASH)
        if most_hash_index == -1 and least_hash_index == -1:
            return strip_line
        double_quote_index = strip_line.rfind(cls.__DOUBLE_QUOTE)
        single_quote_index = strip_line.rfind(cls.__SINGLE_QUOTE)
        if cls.__can_remove_hash(least_hash_index, double_quote_index, single_quote_index):
            return strip_line[:least_hash_index].rstrip()
        elif cls.__can_remove_hash(most_hash_index, double_quote_index, single_quote_index):
            return strip_line[:most_hash_index].rstrip()
        return strip_line

    @classmethod
    def __is_a_comment(cls, strip_line: str) -> bool:
        return strip_line.startswith("\ufeff#") or strip_line.startswith(cls.__HASH)

    @classmethod
    def __startswith_triple_quote(cls, strip_line: str) -> bool:
        return strip_line.startswith(cls.__DOUBLE_TRIPLE_QUOTE) or strip_line.startswith(cls.__SINGLE_TRIPLE_QUOTE)

    @classmethod
    def __endswith_triple_quote(cls, strip_line: str) -> bool:
        return strip_line.endswith(cls.__SINGLE_TRIPLE_QUOTE) or strip_line.endswith(cls.__DOUBLE_TRIPLE_QUOTE)

    @classmethod
    def __has_triple_quote(cls, strip_line: str) -> bool:
        return cls.__DOUBLE_TRIPLE_QUOTE in strip_line or cls.__SINGLE_TRIPLE_QUOTE in strip_line

    @staticmethod
    def __is_choice_menu(strip_line: str) -> bool:
        return strip_line.startswith("menu") and strip_line.endswith(":")

    def has_loose_double_quote(self) -> bool:
        """Check for unpaired double quote."""
        no_escaped_quotes = self._strip_line.replace(r'\"', "|")
        return no_escaped_quotes.count(LineInfo.__DOUBLE_QUOTE) % 2 != 0

    def setup(self, line: str):
        self._strip_line = LineInfo.__strip_inline_comment(line.strip())
        self._is_comment = LineInfo.__is_a_comment(self._strip_line)
        self._is_triple_quote_start = LineInfo.__startswith_triple_quote(self._strip_line)
        self._is_triple_quote_end = LineInfo.__endswith_triple_quote(self._strip_line)
        self._has_triple_quote = LineInfo.__has_triple_quote(self._strip_line)
        self._is_menu = LineInfo.__is_choice_menu(self._strip_line)

    @property
    def strip_line(self):
        return self._strip_line

    @property
    def is_comment(self):
        return self._is_comment

    @property
    def is_triple_quote_start(self):
        return self._is_triple_quote_start

    @property
    def is_triple_quote_end(self):
        return self._is_triple_quote_end

    @property
    def has_triple_quote(self):
        return self._has_triple_quote

    @property
    def is_menu(self):
        """Checks if line is a choice menu."""
        return self._is_menu
