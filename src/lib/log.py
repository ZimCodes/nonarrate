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
    def complete(cls, text: str):
        cls.log(f"{text} complete!")
