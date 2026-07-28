from lib.custom_types import MultiLineType


class MultiLineState:
    """Holds multiple line information.

    Mostly used to hold previous multiple lines.

    Attributes:
        multi_type: Type of multiple lines used
        is_choice_menu:
            Is label a choice menu? Used to keep narration before and during a choice menu.
    """

    def __init__(self) -> None:
        self._lines = list()
        self.multi_type = MultiLineType.NONE
        self.is_choice_menu = False

    def clear(self):
        """Clear collection of multiple lines stored."""
        self._lines.clear()

    def append_line(self, line: str):
        """Add a line to the collection of lines.

        Args:
            line: a line of strings.
        """
        self._lines.append(line)

    def is_empty(self) -> bool:
        """Checks if multiple lines are stored."""
        return len(self._lines) == 0

    def reset(self):
        """Reset all values to default."""
        self._lines = list()
        self.multi_type = MultiLineType.NONE
        self.is_choice_menu = False

    def get_lines(self) -> list[str]:
        """Gets a collection of lines."""
        return self._lines
