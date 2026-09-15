import typing


@typing.final
class Stat:
    """Hold global stats of the work done by nonarrate.

    Attributes:
        total_lines: a sum of all total lines found in every file.
        total_cleaned_lines: a sum of all total lines found in every file after removal of narration.
        file_urls: list of file url that were modified
    """

    total_lines: int = 0
    total_cleaned_lines: int = 0
    file_urls: list[str] = list()

    @classmethod
    def reset_stats(cls):
        cls.total_lines = 0
        cls.total_cleaned_lines = 0
        cls.file_urls = list()
