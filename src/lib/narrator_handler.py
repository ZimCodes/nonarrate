from .custom_types import FileInfo
import typing


@typing.final
class NarratorHandler:
    """Handles operations involving the removal of narration and thoughts.

    This handler removes narration and thoughts detected in the contents of files. After the operation,
    attempts to cleanup the file(s) are set in place.

    Attributes:
        PAUSE_STATEMENT: represents Ren'Py's 'pause' statement.
    """

    PAUSE_STATEMENT: str = "pause"

    def __init__(self) -> None:
        self._total_lines = 0
        self._total_cleaned_lines = 0

    @staticmethod
    def get_indent_num(line: str) -> int:
        """Gets the current amount of indentation."""
        return len(line) - len(line.lstrip())

    def __is_image_label(self, strip_line: str) -> bool:
        return strip_line.startswith("image ") and strip_line.endswith(":")

    def __is_comment(self, strip_line: str) -> bool:
        return strip_line.startswith("\uFEFF#") or strip_line.startswith("#")

    def __reset_line_stats(self):
        self._total_cleaned_lines = 0
        self._total_lines = 0

    def line_stats(self) -> tuple[int, int]:
        return self._total_cleaned_lines, self._total_lines

    def remove(self, file_infos: list[FileInfo], args) -> list[FileInfo]:
        """Removes narration & thoughts from file content.

        Along with the removal operation, cleanup operations are executed afterwards.

        Args:
            file_infos: a list of file information including their content and location.

        Returns:
            a list of file information and their modified content without the presence of a narrator or thought.
        """
        self.__reset_line_stats()
        label_check = {"is_choice_menu": False, "is_image_label": False}
        for file_info in file_infos:
            self._total_lines += len(file_info.lines)
            cleaned_lines = []
            image_label_indent = 0
            prev_line_info = {"is_narr": False, "line": ""}
            is_multi_line = False
            for line in file_info.lines:
                strip_line = line.strip()
                if self.__is_comment(strip_line):
                    continue
                endswith_quote = strip_line.endswith('"')
                # If narrator is multiline. Ex:
                # narr ".....................
                # ....................."
                if is_multi_line:
                    if endswith_quote:
                        is_multi_line = False
                        if args.pauses:
                            # Replaces narration with pauses
                            cleaned_lines.append(f"{' ' * self.get_indent_num(line)}{NarratorHandler.PAUSE_STATEMENT}\n")
                    continue
                is_narrator = args.validator.is_valid(strip_line)

                # An 'image <label_name>:' is in use.
                if not label_check["is_image_label"] and self.__is_image_label(strip_line):
                    label_check["is_image_label"] = True
                    image_label_indent = self.get_indent_num(line)
                elif (
                    label_check["is_image_label"]
                    and self.get_indent_num(line) <= image_label_indent
                    and not self.__is_image_label(strip_line)
                ):
                    label_check["is_image_label"] = False

                if not label_check["is_image_label"]:
                    if label_check["is_choice_menu"] or not is_narrator:
                        cleaned_lines.append(line)
                    elif (
                        args.pauses
                        and is_narrator
                        and not prev_line_info["line"].strip().startswith(NarratorHandler.PAUSE_STATEMENT)
                        and len(cleaned_lines)
                        and not cleaned_lines[len(cleaned_lines) - 1]
                        .strip()
                        .startswith(NarratorHandler.PAUSE_STATEMENT)
                    ):
                        # Replaces narration with pauses
                        cleaned_lines.append(f"{' ' * self.get_indent_num(line)}{NarratorHandler.PAUSE_STATEMENT}\n")

                    # Keeps the narrator during choice menu appearance
                    if strip_line.startswith("menu:"):
                        label_check["is_choice_menu"] = True
                        if prev_line_info["is_narr"]:
                            length = len(cleaned_lines)
                            cleaned_lines.insert(length - 1, prev_line_info["line"])
                    elif label_check["is_choice_menu"] and len(strip_line) != 0:
                        label_check["is_choice_menu"] = False
                else:
                    cleaned_lines.append(line)

                if is_narrator and not is_multi_line and not endswith_quote:
                    is_multi_line = True
                    continue
                prev_line_info["is_narr"] = is_narrator
                prev_line_info["line"] = line

            file_info.lines = cleaned_lines
        if args.pauses:
            file_infos = self.__pause_filter(file_infos)
        return self.__correct_indent(file_infos)

    def __correct_indent(self, file_infos: list[FileInfo]) -> list[FileInfo]:
        """Attempts to correct indentation for each line in a file content.

        In order to do this, all file contents will be looped through again.

        Args:
            file_infos: list holding all files and their content.

        Returns:
            a list of all file info and their content.
        """
        for file_info in file_infos:
            cleaned_lines = []
            prev_indent_info = dict()
            for line in file_info.lines:
                strip_line = line.strip()
                if strip_line.endswith(":") and not len(prev_indent_info):
                    prev_indent_info["line"] = line
                    prev_indent_info["indent"] = self.get_indent_num(line)
                elif strip_line.endswith(":") and len(prev_indent_info):
                    cleaned_lines.append(prev_indent_info["line"])
                    cleaned_lines.append(line)
                    prev_indent_info.clear()
                elif len(prev_indent_info):
                    line_indent_num = self.get_indent_num(line)
                    if (
                        (prev_indent_info["indent"] < line_indent_num)
                        # labels do not need to follow strict indentation
                        # Valid example:
                        # label my_cool_label:
                        # scene 103
                        # mc "esvebrewsgr"
                        or prev_indent_info["indent"] == line_indent_num
                        and prev_indent_info["line"].lstrip().startswith("label ")
                    ):
                        cleaned_lines.append(prev_indent_info["line"])
                        cleaned_lines.append(line)
                    elif not strip_line:
                        cleaned_lines.append(prev_indent_info["line"])
                    else:
                        cleaned_lines.append(line)

                    prev_indent_info.clear()
                else:
                    cleaned_lines.append(line)
            file_info.lines = cleaned_lines
            self._total_cleaned_lines += len(cleaned_lines)
        return file_infos

    def __pause_filter(self, file_infos: list[FileInfo]) -> list[FileInfo]:
        """Removes subsequent pause statements.

        Args:
            file_infos: a list of file information.
        """
        for file_info in file_infos:
            cleaned_lines = []
            is_prev_pause = False
            for line in file_info.lines:
                is_pause = line.strip().startswith(NarratorHandler.PAUSE_STATEMENT)
                if is_pause and is_prev_pause:
                    continue
                cleaned_lines.append(line)
                is_prev_pause = is_pause
            file_info.lines = cleaned_lines
        return file_infos
