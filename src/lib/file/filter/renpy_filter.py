import abc
from abc import abstractmethod
from typing import override

from .base_filter import BaseFilter


class RenpyFilter(BaseFilter, abc.ABC):
    """Tools for validating renpy files.

    Renpy files validated are '.rpy' files.
    """

    _file_ext: str = ".rpy"

    def __init__(
            self,
            folder_filter_set: set[str] | None = None,
            file_filter_set: set[str] | None = None,
            glob_filter_set: set[str] | None = None,
    ):
        super().__init__(folder_filter_set, file_filter_set)
        self._glob_filter_set = glob_filter_set

    @abstractmethod
    def _has_passed_file_glob(self, file_name: str) -> bool:
        """Validate a file by using file globs.

        Args:
            file_name: the file name including its extension.

        Returns:
            a boolean determining if a file is valid.
        """
        pass

    @abstractmethod
    def _has_passed_file_literal(self, file_name: str) -> bool:
        pass

    def _is_empty_glob_set(self) -> bool:
        return self._glob_filter_set is None

    @override
    def is_valid_file(self, file_name: str) -> bool:
        return file_name.endswith(RenpyFilter._file_ext)
