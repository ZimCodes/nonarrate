import fnmatch
import os.path
from .renpy_filter import RenpyFilter
from typing import override


class InvalidRenpyFilter(RenpyFilter):
    """Tools for filtering out invalid renpy files."""

    @override
    def _has_passed_file_literal(self, file_name: str) -> bool:
        return self._file_filter_set is None or file_name[:-4].lower() not in self._file_filter_set

    @override
    def _has_passed_file_glob(self, file_name: str) -> bool:
        if self._glob_filter_set is None:
            return True
        return not any(
            (
                fnmatch.fnmatchcase(file_name, pat + RenpyFilter._file_ext)
                for pat in self._glob_filter_set
            )
        )

    @override
    def is_invalid_folder(self, dirpath: str, sub_dirs: list[str]) -> bool:
        if self._folder_filter_set is None:
            return False
        sub_dirs[:] = [sub_dir for sub_dir in sub_dirs if sub_dir not in self._folder_filter_set]
        dir_base_name = os.path.basename(dirpath)
        return any((x == dir_base_name for x in self._folder_filter_set))
