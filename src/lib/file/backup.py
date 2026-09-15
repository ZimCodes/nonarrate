import shutil
import typing
import os.path
from lib.file.filter.backup_filter import BackupFilter
from lib.file.filter.renpy_filter import RenpyFilter
from lib.log import Log


@typing.final
class Backup:
    """Tools for backing up and recovering files."""

    @staticmethod
    def backup_files(file_paths: list[str]):
        """Create backup files in the same directory as the original files.

        Args:
            file_paths: a list of paths pointing to a file.
        """
        Log.wait("Backing up files. This may take a while!")
        Backup.__copy_files(file_paths, BackupFilter.FILE_EXT)

    @staticmethod
    def restore_files(file_paths: list[str]):
        """Restore original files from their backup.

        Args:
            file_paths: list of file paths
        """
        Log.wait("Restoring files to their original state. This may take a while!")
        Backup.__copy_files(file_paths, RenpyFilter.FILE_EXT)
        Log.info("Files restored", len(file_paths))

    @staticmethod
    def __copy_files(file_paths: list[str], file_ext: str):
        for file_path in file_paths:
            copy_path = f"{os.path.splitext(file_path)[0]}{file_ext}"  # *.rpy <-> *.rpybu
            shutil.copy(file_path, copy_path)
