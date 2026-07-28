from .rule import Rule


class VarObjectRule(Rule):
    """Holds rule for filtering character objects by variable name through Ren'Py syntax.

    There are multiple ways to define a variable in Ren'Py. This case uses Ren'Py's native keywords,
    'define' or 'default' to define a variable.

    For Example:
    define myVar = Character(...)
    define myVar = "narrator"
    default myObjVar = "narrator"
    default myObjVar = Character(...)
    """

    def __init__(self, var_items: str | list[str]):
        if type(var_items) is list:
            var_items = "|".join(var_items)
        super().__init__(rf"(?:define|default)\s+\b(?:{var_items})\b")
