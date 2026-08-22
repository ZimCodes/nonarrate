from typing import final
import os

from lib.error.typing import RenpyError
from lib.error import error_fixes
from lib.file.deleter import Deleter
from lib.file.reader import Reader
from lib.file.writer import Writer


@final
class ErrorFixer:
    """Handles fixing common errors caused by nonarrate.

    Errors are most likely to occur when using nonarrate. ErrorFixer
    attempts to fix these errors cause by the tool.
    """

    def fix(self, errors: list[RenpyError], reader: Reader, writer: Writer, deleter: Deleter):
        """Attempts to fix an error generated from 'errors.txt'.

        Args:
            errors: collection of error information
            reader: class for extracting content from a file.
            writer: class for writing content to a file.
            deleter: class for deleting an entire file.
        """

        if errors[0].project_dir is None:
            return
        temp_err_loc = errors[0].file_loc if errors[0].file_loc else ""
        current_file_loc = os.path.join(errors[0].project_dir, temp_err_loc)
        file_info = reader.read_lines(current_file_loc)
        for error in reversed(errors):
            file_info.lines = error_fixes.apply_fix(file_info.lines, error, deleter, current_file_loc)
        writer.write_lines(file_info)
