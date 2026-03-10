import os


class Deleter:
    """Tools for deleting a file."""

    def delete(self, file_url: str):
        """Delete a file.

        Args:
            file_url: Path to a file.
        """
        try:
            os.remove(file_url)
        except FileNotFoundError:
            print(f"File cannot be found! -> {file_url}")
        except OSError:
            print(f"Error: File path is a directory -> {file_url}")
