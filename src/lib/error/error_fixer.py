from typing import final
import os

from lib.error.typing import RenpyError, ErrorType
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

    def fix(self, error_txt_dir: str, errors: list[RenpyError], reader: Reader, writer: Writer, deleter: Deleter):
        """Attempts to fix an error generated from 'errors.txt'.

        Args:
            error_txt_dir: directory path of errors.txt file
            errors: collection of error information
            reader: class for extracting content from a file.
            writer: class for writing content to a file.
            deleter: class for deleting an entire file.
        """

        file_loc = errors[0].file_loc if errors[0].file_loc else ""
        current_file_loc = os.path.join(error_txt_dir, file_loc)
        file_info = reader.read_lines(current_file_loc)
        is_file_deleted = False
        for error in reversed(errors):
            if error.category:
                match error.category:
                    case ErrorType.DUPLICATE:
                        error_fixes.FIXES[error.category](deleter, current_file_loc)
                        is_file_deleted = True
                        break
                    case _:
                        file_info.lines = error_fixes.FIXES[error.category](file_info.lines, error)
        if not is_file_deleted:
            writer.write_lines(file_info)
