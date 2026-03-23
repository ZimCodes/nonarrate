import os
from typing import override
from .reader import Reader


class RenpyReader(Reader):
    """Reader for reading contents from renpy file(s)."""

    @override
    def walk_files(
        self, root_dir: str, invalid_folders: set[str] | None = None, invalid_files: set[str] | None = None
    ) -> list[str]:
        """Retrieve all file paths recursively.

        While walking through directories, retrieve all paths to each file.

        Args:
            root_dir: The starting directory to walk through.

        Returns:
            A list of paths to a renpy file (.rpy).
        """
        rpy_file_ext = "rpy"
        renpy_files = []
        for dirpath, _, file_names in os.walk(root_dir):
            if invalid_folders and any([x in dirpath for x in invalid_folders]):
                continue
            for file_name in file_names:
                if file_name.endswith(rpy_file_ext) and (not invalid_files or file_name[:-4] not in invalid_files):
                    renpy_files.append(os.path.join(dirpath, file_name))
        return renpy_files
