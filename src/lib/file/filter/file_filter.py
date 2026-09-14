from abc import ABC, abstractmethod


class FileFilter(ABC):
    """Tools for validating files."""

    FILE_EXT: str

    def __init__(self, file_filter_set: set[str] | None = None) -> None:
        self._file_filter_set = file_filter_set

    @abstractmethod
    def is_valid_file(self, file_name: str) -> bool:
        """Checks if file can be operated on.

        Args:
            file_name: File name with extension included

            Returns:
                A boolean determining if a file is valid or not.
        """
        pass
