import fnmatch
from typing import override
from .file_filter import FileFilter


class RenpyFilter(FileFilter):
    """Tools for validating renpy files.

    Renpy files validated are '.rpy' files.
    """

    __file_ext: str = ".rpy"

    def __init__(
        self,
        invalid_folders: set[str] | None = None,
        invalid_files: set[str] | None = None,
        invalid_globs: set[str] | None = None,
    ):
        super().__init__(invalid_folders, invalid_files)
        self._invalid_globs = invalid_globs

    def __has_passed_literal(self, file_name: str) -> bool:
        """Validate file by its literal file name.

        Args:
            file_name: the file name including its extension.

        Returns:
            a boolean determining if a file is valid.
        """
        return self._invalid_files is None or file_name[:-4] not in self._invalid_files

    def __has_passed_glob(self, file_name: str) -> bool:
        """Validate a file by using file globs.

        Args:
            file_name: the file name including its extension.

        Returns:
            a boolean determining if a file is valid.
        """
        return self._invalid_globs is None or any(
            (
                file_name
                for pat in self._invalid_globs
                if not fnmatch.fnmatchcase(file_name, pat + RenpyFilter.__file_ext)
            )
        )

    @override
    def is_valid_file(self, file_name: str) -> bool:
        if not file_name.endswith(RenpyFilter.__file_ext):
            return False
        return self.__has_passed_literal(file_name) and self.__has_passed_glob(file_name)
