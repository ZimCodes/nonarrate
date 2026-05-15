import argparse
from collections.abc import Sequence
from .append_unique import AppendUnique


class AppendUniqueLower(AppendUnique):
    """Argparse action for adding unique items in lowercase format.

    All new values added to the set will be lowercase. This argparse action only
    accepts string values.
    """

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
        if self._items is None:
            self._items = set()
        if type(values) is str:
            self._items.add(values.lower())
        else:
            self._items.update((value.lower() for value in values))
        setattr(namespace, self.dest, self._items)
