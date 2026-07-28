from typing import override
from .prev_state import PrevState
from .multi_line_state import MultiLineState


class PrevMultiState(PrevState):
    """Holds multiple previous line information of a file.

    Attributes:
        is_narr: determines if recent previous line is narration
    """

    def __init__(self):
        super().__init__()
        self.is_narr = False
        self.multi_line = MultiLineState()

    @override
    def _reset_state(self):
        self.is_narr = False
        self.multi_line.clear()
