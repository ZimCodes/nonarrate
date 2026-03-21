import pathlib
import shutil

from lib.custom_types import FileInfo
from lib.log import Log


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
    def backup_dir(file_paths: list[str], backup_dir_path: pathlib.Path):
        """Backup files to a specified directory.

        Args:
            file_paths: a list of paths pointing to a file.
            backup_dir_path: the destination directory to backup the files to.
        """
        Log.wait(f"Backing up files to {backup_dir_path}. This may take a while")
        backup_dir_path.mkdir(parents=True, exist_ok=True)
        for file_path in file_paths:
            shutil.copy(file_path, backup_dir_path)
        Log.complete("Backup")
