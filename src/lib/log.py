from typing import final
from lib.stat import Stat


@final
class Log:
    """Provides tools for writing message to the terminal."""

    @staticmethod
    def log(text: str):
        print(text)

    @classmethod
    def wait(cls, text: str):
        cls.log(f"{text}...")

    @classmethod
    def mark(cls, text: str):
        dashes = "-" * 8
        cls.log(f"{dashes}> {text} <{dashes}")

    @classmethod
    def info(cls, title: str, value):
        cls.log(f"[{title}]: {value}")

    @classmethod
    def print_stats(cls):
        try:
            cls.log(f"""
            Stats:
            [Code Removed]: {Stat.total_lines - Stat.total_cleaned_lines} lines
            [Code Removed (%)]: {(Stat.total_lines - Stat.total_cleaned_lines) / Stat.total_lines * 100} %
            [Code Remaining (%)]: {(Stat.total_cleaned_lines / Stat.total_lines) * 100} %
            """)
        except ZeroDivisionError:
            raise ZeroDivisionError("!~ERROR~!: All rpy files are empty! No operations were made!")

