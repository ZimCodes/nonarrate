"""Provides a class for validating arguments.

This module provides a static class, ArgChecker, to check parsed arguments
for validity.
"""

from argparse import Namespace
from pathlib import Path

from .wrong_file_exception import WrongFileError
from typing import final


@final
class ArgChecker:
    """A class for checking parsed arguments for errors."""

    @classmethod
    def check_args(cls, args: Namespace):
        """Checks the parsed arguments for validity.

        Args:
            args: an argparse Namespace containing parsed arguments
        """
        cls.__validate_folder_or_file_arg(args.folder_or_file)

    @staticmethod
    def __validate_folder_or_file_arg(folder_or_file_arg: Path):
        if not folder_or_file_arg.exists():
            raise FileNotFoundError(f"The file/folder, {folder_or_file_arg}, cannot be found!")
        if folder_or_file_arg.is_file() and folder_or_file_arg.name != "errors.txt":
            raise WrongFileError("Only accepts a file called 'errors.txt' or a folder. Preferably the 'game' folder.")

