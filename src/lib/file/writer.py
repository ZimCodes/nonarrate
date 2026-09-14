import json
from lib.custom_types import FileInfo


class Writer:
    """Tools for writing content to files."""

    def write_lines(self, file_info: FileInfo):
        """Write lines to a file.

        Args:
            file_info: Class that holds file information.
        """
        with open(file_info.url, "w", encoding="utf-8") as f:
            f.writelines(file_info.lines)

    @staticmethod
    def dump_stats(total_lines: int, total_cleaned: int):
        results = {
            "stats": {
                "code_removed_by_line": total_lines - total_cleaned,
                "code_removed_by_percentage": (total_lines - total_cleaned) / total_lines * 100,
                "code_remaining_by_percentage": (total_cleaned / total_lines) * 100,
            }
        }
        with open("./stats.json", "w", encoding="utf-8") as f:
            json.dump(results, f)
