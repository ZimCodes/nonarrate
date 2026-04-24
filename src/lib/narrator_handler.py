from .custom_types import FileInfo
import typing
import re


@typing.final
class NarratorHandler:
    """Handles operations involving the removal of narration and thoughts.

    This handler removes narration and thoughts detected in the contents of files. After the operation,
    attempts to cleanup the file(s) are set in place.

    Attributes:
        PAUSE_STATEMENTS: represents Ren'Py's 'pause' statements.
    """

    PAUSE_STATEMENTS: tuple[str, str] = ("pause", "$ renpy.pause")
    __alt_pat: re.Pattern = re.compile(r".*\b(?:image|layeredimage|show|scene|transform)\b[^:]+:")
    __closing_pat: re.Pattern = re.compile(r"(?:[\"']|[\"']\s*with .+)$")

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
        return strip_line.startswith("\ufeff#") or strip_line.startswith("#")

    def __is_atl_block(self, strip_line: str) -> bool:
        return True if self.__alt_pat.match(strip_line) else False

    def __is_closing(self,strip_line: str) -> bool:
        return True if self.__closing_pat.search(strip_line) else False

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
            prev_line_info = {"is_narr": False, "line": "", "multiline": list()}
            is_multi_line = False
            alt_info = {"indent": 0, "is": False}
            for line in file_info.lines:
                strip_line = line.strip()
                if self.__is_comment(strip_line):
                    continue
                # REF:https://www.renpy.org/doc/html/transforms.html#atl-animation-and-transformation-language
                # Example:
                # init -2 layeredimage augustina:
                #   "image_smile.png"
                if alt_info["is"]:
                    if self.get_indent_num(line) > alt_info["indent"]:
                        cleaned_lines.append(line)
                        continue
                    else:
                        alt_info["is"] = False
                elif self.__is_atl_block(strip_line):
                    alt_info["is"] = True
                    alt_info["indent"] = self.get_indent_num(line)
                    cleaned_lines.append(line)
                    continue

                # If narrator is multiline. Ex:
                # narr ".....................
                # ....................."
                if is_multi_line:
                    if self.__is_closing(strip_line):
                        is_multi_line = False
                        if args.pauses:
                            # Replaces narration with pauses
                            cleaned_lines.append(
                                f"{' ' * self.get_indent_num(line)}{NarratorHandler.PAUSE_STATEMENTS[0]}\n"
                            )
                    prev_line_info["multiline"].append(line)
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
                            and not prev_line_info["line"].strip().startswith(NarratorHandler.PAUSE_STATEMENTS)
                            and len(cleaned_lines)
                            and not cleaned_lines[len(cleaned_lines) - 1]
                            .strip()
                            .startswith(NarratorHandler.PAUSE_STATEMENTS)
                    ):
                        # Replaces narration with pauses
                        cleaned_lines.append(
                            f"{' ' * self.get_indent_num(line)}{NarratorHandler.PAUSE_STATEMENTS[0]}\n"
                        )

                    # Keeps the narrator during choice menu appearance
                    if strip_line.startswith("menu:"):
                        label_check["is_choice_menu"] = True
                        if prev_line_info["is_narr"]:
                            length = len(cleaned_lines)
                            cleaned_lines.insert(length - 1, prev_line_info["line"])
                        elif len(prev_line_info["multiline"]):
                            last_cleaned_line = cleaned_lines.pop()
                            cleaned_lines.extend(prev_line_info["multiline"])
                            cleaned_lines.append(last_cleaned_line)
                            prev_line_info["multiline"].clear()
                    elif label_check["is_choice_menu"] and len(strip_line) != 0:
                        label_check["is_choice_menu"] = False
                else:
                    cleaned_lines.append(line)

                if is_narrator and not is_multi_line and not self.__is_closing(strip_line):
                    is_multi_line = True
                    prev_line_info["multiline"].clear()
                    prev_line_info["multiline"].append(line)
                    continue
                    
                if strip_line != "":
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
                strip_line = line.strip()
                is_pause = strip_line.startswith(NarratorHandler.PAUSE_STATEMENTS)
                if is_pause and is_prev_pause:
                    continue
                cleaned_lines.append(line)
                if strip_line:
                    is_prev_pause = is_pause
            file_info.lines = cleaned_lines
        return file_infos
