from typing import final
import re
import pathlib
import os
import enum

from lib.custom_types import RenpyError
from lib.file.deleter import Deleter
from lib.file.reader import Reader
from lib.file.writer import Writer
from lib.log import Log
from lib.narrator_handler import NarratorHandler


class ErrorType(enum.StrEnum):
    """Represents types of errors."""

    NON_EMPTY = "non-empty"
    INDENTED_LINE = "Line is indented"
    EXPECTED_STATEMENT = "expected statement"
    INDENT_MISMATCH = "Indentation mismatch"
    DUPLICATE = enum.auto()
    MENU_NO_CHOICES = "Menu does not contain any choices"


@final
class ErrorFixer:
    """Handles fixing common errors caused by nonarrate.

    Errors are most likely to occur when using nonarrate. ErrorFixer
    attempts to fix these errors cause by the tool.
    """

    _dest_pat: re.Pattern = re.compile(r"(?:and )?File\s+.+(game/.+\.rpy)")
    _line_num_pat: re.Pattern = re.compile(r".+line (\d+):")
    _type_pat: re.Pattern = re.compile(
        rf".+({ErrorType.NON_EMPTY}|{ErrorType.INDENTED_LINE}|{ErrorType.EXPECTED_STATEMENT}|{ErrorType.INDENT_MISMATCH}|{ErrorType.MENU_NO_CHOICES})"
    )
    _project_dir: str | None = None

    @staticmethod
    def __add_error(errors: dict[str, list[RenpyError]], error: RenpyError):
        if not error.file_loc:
            return
        if error.file_loc not in errors:
            errors[error.file_loc] = [error]
        else:
            errors[error.file_loc].append(error)

    @classmethod
    def __get_error(cls, line: str) -> RenpyError:
        file_url = cls._dest_pat.match(line).group(1) if cls._dest_pat.match(line) else None
        line_num = int(cls._line_num_pat.match(line).group(1)) if cls._line_num_pat.match(line) else None
        category = cls._type_pat.match(line).group(1) if cls._type_pat.match(line) else None
        if not category and line.startswith("and File"):
            category = ErrorType.DUPLICATE
        return RenpyError(file_url, line_num, category)

    @classmethod
    def get_errors(cls, errors_txt: pathlib.Path, reader: Reader) -> dict[str, list[RenpyError]]:
        """Parse the errors from Ren'Py's errors.txt file.

        This method needs to be used first as it initializes important properties
        and retrieves all error information needed to operate on.

        Args:
            errors_txt: a path to Ren'Py's errors.txt file.
            reader: class for reading file information.

        Returns:
            a list of Ren'Py errors acquired from errors.txt file.
        """

        cls._project_dir = os.path.dirname(errors_txt)
        file_info = reader.read_lines(errors_txt)
        errors = {}
        total_errors_log = 0
        for line in file_info.lines:
            strip_line = line.strip()
            if not strip_line.startswith("File") and not strip_line.startswith("and File"):
                continue
            error = cls.__get_error(line)
            if error.category:
                total_errors_log += 1
            cls.__add_error(errors, error)
        Log.log(f"Total errors detected: {total_errors_log}")
        return errors

    def __dedent_lines(self, lines: list[str], start_index: int, start_indent: int | None = None) -> list[str]:
        """Correct indentation by decreasing indent level by 1.

        Indentation will be decreased by 1 level (4 spaces) until a line with the
        same indentation level as the first indented dedented line is reached.

        Args:
            lines: lines of text found in a file
            start_index: the index of the line with the starting indentation problem specified by errors.txt

        Returns:
            a list including dedented lines.
        """
        min_indent = start_indent
        for i, line in enumerate(lines[start_index:], start_index):
            if min_indent is None:
                lines[i] = line[4:]
                min_indent = NarratorHandler.get_indent_num(lines[i])
            elif NarratorHandler.get_indent_num(line) > min_indent:
                lines[i] = line[4:]
            else:
                break
        return lines

    def __reverse_dedent_lines(self, lines: list[str], start_index: int) -> list[str]:
        """Correct indentation by decreasing indent level by 1 going up to preceding lines.

        All preceding lines with an indentation level higher than the starting line will be dedented 1 level.
        This is the case until a line with an indentation level equal or lesser than the starting line is reached.

        Args:
            lines: lines of text found in a found
            start_index: the index of the line with the starting indentation problem specified by errors.txt

        Returns:
            a list including dedented lines.
        """
        min_indent = NarratorHandler.get_indent_num(lines[start_index])
        start_index = start_index - 1
        for i in range(start_index, 0, -1):
            line = lines[i]
            line_indent = NarratorHandler.get_indent_num(line)
            if line_indent <= min_indent:
                break
            lines[i] = line[4:]
        return lines

    def fix(self, errors: list[RenpyError], reader: Reader, writer: Writer, deleter: Deleter):
        """Attempts to fix an error generated from 'errors.txt'.

        Args:
            error: error information
            reader: class for extracting content from a file.
        """
        if self._project_dir is None:
            return
        temp_err_loc = errors[0].file_loc if errors[0].file_loc else ""
        current_file_loc = os.path.join(self._project_dir, temp_err_loc)
        file_info = reader.read_lines(current_file_loc)
        errors.reverse()
        for error in errors:
            if error.category:
                if error.line_num:
                    if ErrorType.NON_EMPTY in error.category or ErrorType.EXPECTED_STATEMENT in error.category:
                        file_info.lines.pop(error.line_num - 1)
                    elif ErrorType.INDENTED_LINE in error.category:
                        file_info.lines = self.__dedent_lines(file_info.lines, error.line_num - 1)
                    elif ErrorType.INDENT_MISMATCH in error.category:
                        file_info.lines = self.__reverse_dedent_lines(file_info.lines, error.line_num - 1)
                    elif ErrorType.MENU_NO_CHOICES in error.category:
                        file_info.lines = self.__dedent_lines(
                            file_info.lines,
                            error.line_num,
                            NarratorHandler.get_indent_num(file_info.lines[error.line_num - 1]),
                        )
                        file_info.lines.pop(error.line_num - 1)
                elif ErrorType.DUPLICATE in error.category:
                    deleter.delete(current_file_loc)
        writer.write_lines(file_info)
