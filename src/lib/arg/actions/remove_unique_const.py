"""Provides a RemoveUniqueConst class for removing 'const' values.

This module includes an argparse Action class, RemoveUniqueConst, for removing values from
a collection of unique constants.
"""
from .unique_const import UniqueConst

class RemoveUniqueConst(UniqueConst):
    """Represents an argparse action for removing unique constant values.

    This class provides argument parsing action for removing unique constant values
    when the option this class is bound to is selected.
    """

    def _modify_set(self, option_string: str):
        """Remove a constant value from a set

        Args:
            option_string: Name of the argument used to call this action

        Raises:
            ValueError: If a 'default' list is not set for the current 'dest'
        """
        if self._shared_list is None:
            raise ValueError(f"RemoveConst requires at least 1 dest={self.dest} to have a 'default' list set")
        self._shared_list.remove(option_string)
