import os
import pathlib
from ..custom_types import FileInfo


class Reader:
    """Read content from file(s)."""

    def read_lines(self, file_url: str | pathlib.Path) -> FileInfo:
        """Retrieve lines from a file.

        Args:
            file_url: Path to file

        Returns:
            An object that holds file information.
        """
        lines = []
        with open(file_url, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return FileInfo(str(file_url), lines)

    def walk_files(self, root_dir: str) -> list[str]:
        """Retrieve all file paths recursively.

        While walking through directories, retrieve all paths to each file.

        Args:
            root_dir: The starting directory to walk through.

        Returns:
            A list of paths to a file.
        """
        files = []
        for dirpath, _, file_names in os.walk(root_dir):
            for file_name in file_names:
                files.append(os.path.join(dirpath, file_name))
        return files
