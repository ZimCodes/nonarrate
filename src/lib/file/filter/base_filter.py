from abc import abstractmethod, ABC


class BaseFilter(ABC):
    """Base filter providing tools for validating files and folders.

    Validates whether a file should be operated on.
    """

    def __init__(
            self,
            folder_filter_set: set[str] | None = None,
            file_filter_set: set[str] | None = None,
    ):
        self._folder_filter_set = folder_filter_set
        self._file_filter_set = file_filter_set

    @abstractmethod
    def is_invalid_folder(self, dirpath: str,sub_dirs: list[str]) -> bool:
        """Removes invalid subdirectories and check if current folder is valid.

        Args:
            dirpath: absolute directory path
            sub_dirs: collection of subdirectory names
        """
        pass

    @abstractmethod
    def is_valid_file(self, file_name: str) -> bool:
        """Checks if file can be operated on.

        Args:
            file_name: File name with extension included

        Returns:
            A boolean determining if a file is valid or not.
        """
        pass