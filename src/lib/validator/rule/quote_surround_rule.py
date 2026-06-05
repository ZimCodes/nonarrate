from .rule import Rule


class QuoteSurroundRule(Rule):
    """Quote rule for dialogue surrounded by open/close symbol."""

    def __init__(self, open_symbol: str, close_symbol: str):
        super().__init__(
            rf'^(?:{{\w+(?:=[^}}]+)?}})*\s*{open_symbol}[^{open_symbol}]+{close_symbol}\s*(?:(?:{{/\w+}})*[.?!]?|[.?!]?(?:{{/\w+}})*)$')
