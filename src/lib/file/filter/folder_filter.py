from abc import ABC, abstractmethod


class FolderFilter(ABC):
    """Tools for validating directories."""

    def __init__(self, folder_filter_set: set[str] | None = None) -> None:
        self._folder_filter_set = folder_filter_set

    @abstractmethod
    def is_invalid_folder(self, dirpath: str, sub_dirs: list[str]) -> bool:
        """Removes invalid subdirectories and check if current folder is valid.

        Args:
            dirpath: absolute directory path
            sub_dirs: collection of subdirectory names
        """
        pass
