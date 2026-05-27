from typing import final


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
        dashes = '-' * 8
        cls.log(f"{dashes}> {text} <{dashes}")

    @classmethod
    def info(cls, title: str, value):
        cls.log(f"[{title}]: {value}")


    @classmethod
    def print_stats(cls, total_lines: int, total_cleaned: int):
        try:
            cls.log(f"""
            Stats:
            [Code Removed]: {total_lines - total_cleaned} lines
            [Code Removed (%)]: {(total_lines - total_cleaned) / total_lines * 100} %
            [Code Remaining (%)]: {(total_cleaned / total_lines) * 100} %
            """)
        except ZeroDivisionError:
            raise ZeroDivisionError("!~ERROR~!: All rpy files are empty! No operations were made!")