from lib.info import AtlState, LineState, PauseState, PrevIndentState, PrevMultiState
from .custom_types import FileInfo, MultiLineType
import typing
import re


@typing.final
class NarratorHandler:
    """Handles operations involving the removal of narration and thoughts.

    This handler removes narration and thoughts detected in the contents of files. After the operation,
    attempts to clean up the file(s) are set in place.

    Attributes:
        PAUSE_STATEMENTS: represents Ren'Py's 'pause' statements.
    """

    PAUSE_STATEMENTS: tuple[str, str] = ("pause", "$ renpy.pause")
    __closing_pat: re.Pattern = re.compile(r"(?:\"|\"\s*with .+)$")
    __total_lines: int = 0
    __total_cleaned_lines: int = 0

    @staticmethod
    def get_indent_num(line: str) -> int:
        """Gets the current amount of indentation."""
        return len(line) - len(line.lstrip())

    @classmethod
    def __is_closing(cls, strip_line: str) -> bool:
        return True if cls.__closing_pat.search(strip_line) else False

    @classmethod
    def __reset_line_stats(cls):
        cls.__total_cleaned_lines = 0
        cls.__total_lines = 0

    @classmethod
    def line_stats(cls) -> tuple[int, int]:
        return cls.__total_cleaned_lines, cls.__total_lines

    @classmethod
    def remove(cls, file_infos: list[FileInfo], args) -> list[FileInfo]:
        """Removes narration & thoughts from file content.

        Along with the removal operation, cleanup operations are executed afterward.

        args:
            file_infos: a list of file information including their content and location.

        Returns:
            a list of file information and their modified content without the presence of a narrator or thought.
        """
        cls.__reset_line_stats()
        for file_info in file_infos:
            cls.__total_lines += len(file_info.lines)
            cleaned_lines = []
            line_state = LineState()
            atl_state = AtlState()
            prev_multi_state = PrevMultiState()
            for line in file_info.lines:
                line_state.setup(line)
                if (line_state.is_comment
                    # REF: https://www.renpy.org/doc/html/dialogue.html#special-characters
                    # 'extend' keyword
                        or prev_multi_state.is_narr and line_state.strip_line.startswith('extend ')):
                    continue

                # REF:https://www.renpy.org/doc/html/transforms.html#atl-animation-and-transformation-language
                # Example:
                # init -2 layeredimage augustina:
                #   "image_smile.png"
                if atl_state.is_atl:
                    if cls.get_indent_num(line) > atl_state.indent_num:
                        cleaned_lines.append(line)
                        continue
                    else:
                        atl_state.is_atl = False
                if atl_state.is_block(line_state.strip_line):
                    atl_state.is_atl = True
                    atl_state.indent_num = cls.get_indent_num(line)
                    cleaned_lines.append(line)
                    continue

                # If narrator is multiline. Ex:
                # narr ".....................
                # ....................."
                if prev_multi_state.multi_line.multi_type is not MultiLineType.NONE:
                    if prev_multi_state.multi_line.multi_type is MultiLineType.VALID_TRIPLE_QUOTE:
                        if line_state.is_triple_quote_end or line_state.has_triple_quote:
                            prev_multi_state.multi_line.multi_type = MultiLineType.NONE
                        is_narrator = args.quote_validator.is_valid(line_state.strip_line)
                        if not is_narrator:
                            cleaned_lines.append(line)
                    elif prev_multi_state.multi_line.multi_type is MultiLineType.VALID_SINGLE_QUOTE:
                        if cls.__is_closing(line_state.strip_line):
                            prev_multi_state.multi_line.multi_type = MultiLineType.NONE
                        is_narrator = args.quote_validator.is_valid(line_state.strip_line)
                        if not is_narrator:
                            cleaned_lines.append(line)
                    else:
                        if (
                                prev_multi_state.multi_line.multi_type is MultiLineType.SINGLE_QUOTE and cls.__is_closing(
                            line_state.strip_line)
                        ) or (
                                prev_multi_state.multi_line.multi_type is MultiLineType.TRIPLE_QUOTE and line_state.is_triple_quote_end):
                            prev_multi_state.multi_line.multi_type = MultiLineType.NONE
                            if args.pauses:
                                # Replaces narration with pauses
                                cleaned_lines.append(
                                    f"{' ' * cls.get_indent_num(line)}{cls.PAUSE_STATEMENTS[0]}\n"
                                )
                        prev_multi_state.multi_line.append_line(line)
                    continue

                if not line_state.is_menu and line_state.strip_line != "":
                    prev_multi_state.multi_line.clear()

                is_narrator = args.validator.is_valid(line_state.strip_line)

                if prev_multi_state.multi_line.is_choice_menu or not is_narrator:
                    if not line_state.is_triple_quote_start:
                        cleaned_lines.append(line)
                elif (
                        args.pauses
                        and is_narrator
                        and not prev_multi_state.line.strip().startswith(cls.PAUSE_STATEMENTS)
                        and len(cleaned_lines)
                        and not cleaned_lines[len(cleaned_lines) - 1].strip().startswith(
                    cls.PAUSE_STATEMENTS)
                ):
                    # Replaces narration with pauses
                    cleaned_lines.append(f"{' ' * cls.get_indent_num(line)}{cls.PAUSE_STATEMENTS[0]}\n")

                # Keeps the narrator during choice menu appearance
                if line_state.is_menu:
                    prev_multi_state.multi_line.is_choice_menu = True
                    if prev_multi_state.is_narr:
                        length = len(cleaned_lines)
                        cleaned_lines.insert(length - 1, prev_multi_state.line)
                    elif not prev_multi_state.multi_line.is_empty():
                        last_cleaned_line = cleaned_lines.pop()
                        cleaned_lines.extend(prev_multi_state.multi_line.get_lines())
                        cleaned_lines.append(last_cleaned_line)
                        prev_multi_state.multi_line.clear()
                elif prev_multi_state.multi_line.is_choice_menu and len(line_state.strip_line) != 0:
                    prev_multi_state.multi_line.is_choice_menu = False

                if prev_multi_state.multi_line.multi_type is MultiLineType.NONE:
                    if (line_state.is_triple_quote_start
                            or (
                                    is_narrator and line_state.has_triple_quote and not line_state.is_triple_quote_end and not line_state.more_triple_quotes)
                            or (is_narrator and line_state.is_triple_quote_end and not line_state.more_triple_quotes)):
                        prev_multi_state.multi_line.multi_type = MultiLineType.TRIPLE_QUOTE
                    elif line_state.has_loose_double_quote() and not cls.__is_closing(
                            line_state.strip_line) and not line_state.has_triple_quote:
                        prev_multi_state.multi_line.multi_type = MultiLineType.SINGLE_QUOTE if is_narrator else MultiLineType.VALID_SINGLE_QUOTE
                    elif not is_narrator and line_state.has_triple_quote and not line_state.more_triple_quotes:
                        # linda """You are not narrator
                        prev_multi_state.multi_line.multi_type = MultiLineType.VALID_TRIPLE_QUOTE

                    if prev_multi_state.multi_line.multi_type is not MultiLineType.NONE:
                        prev_multi_state.multi_line.clear()
                        if (prev_multi_state.multi_line.multi_type is not MultiLineType.VALID_TRIPLE_QUOTE
                                and prev_multi_state.multi_line.multi_type is not MultiLineType.VALID_SINGLE_QUOTE):
                            prev_multi_state.multi_line.append_line(line)
                        continue

                if line_state.strip_line != "":
                    prev_multi_state.is_narr = is_narrator
                    prev_multi_state.line = line

            file_info.lines = cleaned_lines
        if args.pauses:
            file_infos = cls.__pause_filter(file_infos)
        return cls.__correct_indent(file_infos)

    @classmethod
    def __correct_indent(cls, file_infos: list[FileInfo]) -> list[FileInfo]:
        """Attempts to correct indentation for each line in a file content.

        In order to do this, all file contents will be looped through again.

        Args:
            file_infos: list holding all files and their content.

        Returns:
            a list of all file info and their content.
        """
        for file_info in file_infos:
            cleaned_lines = []
            prev_indent_state = PrevIndentState()
            for line in file_info.lines:
                strip_line = line.strip()
                if strip_line.endswith(":") and prev_indent_state.has_reset:
                    prev_indent_state.recent_line = line
                    prev_indent_state.indent_num = cls.get_indent_num(line)
                elif strip_line.endswith(":") and not prev_indent_state.has_reset:
                    cleaned_lines.append(prev_indent_state.recent_line)
                    cleaned_lines.append(line)
                    prev_indent_state.reset()
                elif not prev_indent_state.has_reset:
                    line_indent_num = cls.get_indent_num(line)
                    if (
                            (prev_indent_state.indent_num < line_indent_num)
                            # labels do not need to follow strict indentation. Also,
                            # if previous is a statement , '<block-name>:', allow it through.
                            # Valid example:
                            # label my_cool_label:
                            # scene 103
                            # mc "esvebrewsgr"
                            or prev_indent_state.indent_num == line_indent_num
                            and prev_indent_state.recent_line.rstrip().endswith(":")
                    ):
                        cleaned_lines.append(prev_indent_state.recent_line)
                        cleaned_lines.append(line)
                    elif not strip_line:
                        cleaned_lines.append(prev_indent_state.recent_line)
                    else:
                        cleaned_lines.append(line)

                    prev_indent_state.reset()
                else:
                    cleaned_lines.append(line)
            file_info.lines = cleaned_lines
            cls.__total_cleaned_lines += len(cleaned_lines)
        return file_infos

    @classmethod
    def __pause_filter(cls, file_infos: list[FileInfo]) -> list[FileInfo]:
        """Removes subsequent pause statements.

        Args:
            file_infos: a list of file information.
        """
        for file_info in file_infos:
            cleaned_lines = []
            pause_info = PauseState()
            for line in file_info.lines:
                strip_line = line.strip()
                pause_info.set_pause(strip_line.startswith(cls.PAUSE_STATEMENTS))
                if pause_info.is_duplicate():
                    continue
                cleaned_lines.append(line)
                if strip_line:
                    pause_info.snapshot_pause_state()
            file_info.lines = cleaned_lines
        return file_infos
