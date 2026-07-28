from abc import ABC, abstractmethod


class PrevState(ABC):
    """Holds previous line information of a file.

    Attributes:
        line: the most recent previous line.
    """

    def __init__(self):
        self.line = ""

    def reset(self):
        """Reset all previous information back to default values."""
        self.line = ""
        self._reset_state()

    @abstractmethod
    def _reset_state(self):
        pass
