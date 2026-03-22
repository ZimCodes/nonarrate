import argparse
from collections.abc import Sequence


class AppendUnique(argparse.Action):
    """Argparse action for adding unique items."""

    def __init__(
        self,
        option_strings: Sequence[str],
        dest: str,
        nargs: int | str | None = None,
        const=None,
        default=None,
        type=None,
        choices=None,
        required: bool = False,
        help=None,
        metavar=None,
        deprecated: bool = False,
    ) -> None:
        super().__init__(option_strings, dest, "*", const, default, type, choices, required, help, metavar, deprecated)

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: str | Sequence[str] | None,
        option_string: str | None = None,
    ) -> None:
        if not values:
            return
        self._items = getattr(namespace, self.dest, set())
        if type(values) is str:
            self._items.add(values)
        else:
            self._items.update(values)
        setattr(namespace, self.dest, self._items)
