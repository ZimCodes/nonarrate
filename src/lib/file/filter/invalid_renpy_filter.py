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
        return self._glob_filter_set is None or any(
            (
                file_name
                for pat in self._glob_filter_set
                if not fnmatch.fnmatchcase(file_name, pat + RenpyFilter._file_ext)
            )
        )

    @override
    def is_invalid_folder(self, dirpath: str) -> bool:
        dir_base_name = os.path.basename(dirpath)
        return self._folder_filter_set is not None and any(( x == dir_base_name for x in self._folder_filter_set ))
