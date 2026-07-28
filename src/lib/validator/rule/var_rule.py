from .rule import Rule


class VarRule(Rule):
    """Holds rule for filtering by variable name through Python syntax.

    There are multiple ways to define a variable in Ren'Py. This case uses Python to declare variables.
    Python is denoted with the '$' syntax.

    For Example:
    $ myVar = 'narrator'
    $ myObjVar = Character(...)
    """

    def __init__(self, var_items: str | list[str]):
        if type(var_items) is list:
            var_items = "|".join(var_items)
        super().__init__(rf"\$\s+\b(?:{var_items})\b")
