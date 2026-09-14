from .folder_filter import FolderFilter
from .file_filter import FileFilter


class FSFilter(FileFilter, FolderFilter):
    """Base filter providing tools for validating files and folders."""

    def __init__(
        self,
        folder_filter_set: set[str] | None = None,
        file_filter_set: set[str] | None = None,
    ):
        self._folder_filter_set = folder_filter_set
        self._file_filter_set = file_filter_set
