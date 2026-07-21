from .rule import Rule

class VarObjectRule(Rule):
    """Holds rule for filtering character objects by variable name."""

    def __init__(self, var_items: str | list[str]):
        if type(var_items) is list:
            var_items = "|".join(var_items)
        super().__init__(rf"(?:\$|(?:define|default))\s+\b(?:{var_items})\b")

