import typing
import re
import pathlib
from .typing import ErrorType, RenpyError
from lib.file.reader import Reader
from lib.log import Log


@typing.final
class ErrorParser:
    """Parse Ren'Py error logs into structured errors objects."""

    _dest_pat: re.Pattern = re.compile(r"(?:and )?File\s+.+?(game/.+\.rpy)")
    _line_num_pat: re.Pattern = re.compile(r".+line (\d+):")

    @staticmethod
    def _regex_match(pattern: re.Pattern | None, line: str, transform_func=None) -> typing.Any:
        if pattern is None:
            return None
        regex_match = pattern.match(line)
        if transform_func is not None:
            return transform_func(regex_match.group(1)) if regex_match else None
        return regex_match.group(1) if regex_match else None

    @staticmethod
    def _add_error(errors: dict[str, list[RenpyError]], error: RenpyError):
        if not error.file_loc:
            return
        if error.file_loc not in errors:
            errors[error.file_loc] = [error]
        else:
            errors[error.file_loc].append(error)

    @staticmethod
    def _parse_error_type(line: str) -> ErrorType | None:
        for error_type in ErrorType:
            if error_type == ErrorType.DUPLICATE:
                continue
            if re.search(error_type, line):
                return error_type
        if line.startswith("and File"):
            return ErrorType.DUPLICATE
        return None

    @classmethod
    def _parse_error(cls, line: str) -> RenpyError:
        file_url = cls._regex_match(cls._dest_pat, line)
        line_num = cls._regex_match(cls._line_num_pat, line, int)
        category = cls._parse_error_type(line)
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

        file_info = reader.read_lines(errors_txt)
        errors = {}
        total_errors_log = 0
        for line in file_info.lines:
            strip_line = line.strip()
            if not strip_line.startswith("File") and not strip_line.startswith("and File"):
                continue
            error = cls._parse_error(line)
            if error.category is not None:
                total_errors_log += 1
            cls._add_error(errors, error)
        Log.info("Errors detected", total_errors_log)
        return errors
