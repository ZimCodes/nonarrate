from typing import final

@final
class PauseState:
    """Holds information about subsequent  pause statements."""

    def __init__(self):
        self._is_pause = False
        self._is_prev_pause = False

    def is_duplicate(self) -> bool:
        """Determines if subsequent pause statements are used."""
        return self._is_pause and self._is_prev_pause

    def set_pause(self,value:bool):
        """Set pause status.

        Args:
            value: new pause status
        """
        self._is_pause = value

    def snapshot_pause_state(self):
        """Save current pause status to previous pause status."""
        self._is_prev_pause = self._is_pause
