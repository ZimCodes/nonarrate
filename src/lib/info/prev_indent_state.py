from typing import override
from .prev_state import PrevState


class PrevIndentState(PrevState):
    """Holds previous line indentation information."""

    def __init__(self):
        super().__init__()
        self._indent_num = 0
        self._has_reset = True

    @property
    def recent_line(self) -> str:
        return self.line

    @recent_line.setter
    def recent_line(self, value: str):
        self.line = value
        self._has_reset = False

    @property
    def indent_num(self) -> int:
        return self._indent_num

    @indent_num.setter
    def indent_num(self, value: int):
        self._indent_num = value
        self._has_reset = False

    @override
    def _reset_state(self):
        self._indent_num = 0
        self._has_reset = True

    @property
    def has_reset(self) -> bool:
        """Determine if previous indentation information has been reset.

        Returns:
            a boolean checking if previous indent information is resetted.
        """
        return self._has_reset