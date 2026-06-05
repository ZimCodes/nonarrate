from .rule import Rule

class SurroundRule(Rule):
    """Holds generic validator filter rule for surrounding an entire dialogue with a single open/close symbol."""

    def __init__(self, open_symbol:str, close_symbol:str):
        super().__init__(rf"(?:(['\"])(?:(?!\1).)+\1|\w+?) ([\"'])(?:{{\w+(?:=[^}}]+)?}})*\s*{open_symbol}[^{open_symbol}]+{close_symbol}\s*(?:(?:{{/\w+}})*[.?!]?|[.?!]?(?:{{/\w+}})*)\s*\2(?:\s*with .+|\s*\([^)]+\))?")
