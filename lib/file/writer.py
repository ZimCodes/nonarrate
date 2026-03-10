class Writer:
    """Tools for writing content to files."""

    def write_lines(self, file_url: str, lines: list[str]):
        """Write lines to a file.

        Args:
            file_url: Path to a file.
            lines: list of text content to write to file
        """
        with open(file_url, "w", encoding="utf-8") as f:
            f.writelines(lines)
