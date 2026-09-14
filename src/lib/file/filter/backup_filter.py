from typing import override
from .file_filter import FileFilter


class BackupFilter(FileFilter):
    """Tools for validating backup files and folders."""

    FILE_EXT: str = ".rpybu"

    def __init__(self, file_filter_set: set[str] | None = None):
        super().__init__(file_filter_set)

    @override
    def is_valid_file(self, file_name: str) -> bool:
        return file_name.endswith(self.FILE_EXT)
