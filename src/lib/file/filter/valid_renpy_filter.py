import fnmatch
import os.path
from typing import override
from .renpy_filter import RenpyFilter


class ValidRenpyFilter(RenpyFilter):
    """Tools for filtering valid renpy files."""

    @override
    def _has_passed_file_literal(self, file_name: str) -> bool:
        return self._file_filter_set is None or file_name[:-4].lower() in self._file_filter_set

    @override
    def _has_passed_file_glob(self, file_name: str) -> bool:
        return self._glob_filter_set is None or any(
            (
                file_name
                for pat in self._glob_filter_set
                if fnmatch.fnmatchcase(file_name, pat + RenpyFilter._file_ext)
            )
        )

    @override
    def is_invalid_folder(self, dirpath: str, sub_dirs: list[str]) -> bool:
        if self._folder_filter_set is None:
            return False
        sub_dirs[:] = [sub_dir for sub_dir in sub_dirs if sub_dir in self._folder_filter_set]
        dir_base_name = os.path.basename(dirpath)
        return any((x != dir_base_name for x in self._folder_filter_set))
