class FileFilter:
    """Tools for ignoring files and folders.

    Validates whether a file should be operated on.
    """

    def __init__(
        self,
        invalid_folders: set[str] | None = None,
        invalid_files: set[str] | None = None,
    ):
        self._invalid_folders = invalid_folders
        self._invalid_files = invalid_files

    def is_invalid_folder(self, dirpath: str) -> bool:
        """Checks if folder is invalid.

        Args:
            dirpath: Directory path

        Returns:
            A boolean determining if a folder is valid or not.
        """
        return self._invalid_folders is not None and any([x in dirpath for x in self._invalid_folders])

    def is_valid_file(self, file_name: str) -> bool:
        """Checks if file can be operated on.

        Args:
            file_name: File name with extension included

        Returns:
            A boolean determining if a file is valid or not.
        """
        return self._invalid_files is None or file_name not in self._invalid_files
