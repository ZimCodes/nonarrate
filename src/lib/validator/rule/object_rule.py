from .rule import Rule

class ObjectRule(Rule):
    """Holds rules for custom speaker names in Character object."""

    def __init__(self, char_object_item: str):
        super().__init__(rf"(?:Dynamic)?Character\s*\([^)]*(?:{char_object_item})[^)]*\)")

