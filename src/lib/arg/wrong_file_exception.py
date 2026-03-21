"""Provides a user-defined exception for a wrong file.

This module defines an exception class, WrongFileError, for
acquiring the wrong file or folder.
"""

class WrongFileError(Exception):
    """Raised when the file/folder isn't correct."""
    pass
