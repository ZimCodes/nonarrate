from lib.file.deleter import Deleter
from .typing import ErrorType, RenpyError
from lib.narrator_handler import NarratorHandler


def reverse_dedent_lines(lines: list[str], start_index: int) -> list[str]:
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
        if not line.lstrip():
            continue
        line_indent = NarratorHandler.get_indent_num(line)
        if line_indent <= min_indent:
            break
        lines[i] = line[4:]
    return lines


def dedent_lines(lines: list[str], start_index: int, start_indent: int | None = None) -> list[str]:
    """Correct indentation by decreasing indent level by 1.

    Indentation will be decreased by 1 level (4 spaces) until a line with the
    same indentation level as the first indented dedented line is reached.

    Args:
        lines: lines of text found in a file
        start_index: the index of the line with the starting indentation problem specified by errors.txt
        start_index: number of spaces as starting indentation

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


def remove_cur_line(lines: list[str], error: RenpyError) -> list[str]:
    if error.line_num is None:
        return lines
    lines.pop(error.line_num - 1)
    return lines


def delete_file(deleter: Deleter, current_file_loc: str):
    deleter.delete(current_file_loc)


def menu_no_choice_fix(lines: list[str], error: RenpyError) -> list[str]:
    if error.line_num is None:
        return lines
    lines = dedent_lines(
        lines,
        error.line_num,
        NarratorHandler.get_indent_num(lines[error.line_num - 1]),
    )
    return remove_cur_line(lines, error)


FIXES = {
    ErrorType.EXPECTED_STATEMENT: remove_cur_line,
    ErrorType.NON_EMPTY: remove_cur_line,
    ErrorType.INDENTED_LINE: lambda lines, error: dedent_lines(lines, error.line_num - 1),
    ErrorType.INDENT_MISMATCH: lambda lines, error: reverse_dedent_lines(lines, error.line_num - 1),
    ErrorType.DUPLICATE: lambda deleter, current_file_loc: delete_file(deleter, current_file_loc),
    ErrorType.MENU_NO_CHOICES: menu_no_choice_fix,
}
