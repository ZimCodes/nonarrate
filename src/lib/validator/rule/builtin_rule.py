from .rule import Rule


class BuiltinRule(Rule):
    """Holds rule for filtering usage of builtin narrators."""

    def __init__(self, narrator: str):
        super().__init__(rf"^{narrator} ", False)
