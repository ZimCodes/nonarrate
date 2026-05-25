from .rule import Rule

class QuoteCueRule(Rule):
    """Quote rule for exspression cues."""

    def __init__(self, cue_symbol: str):
        super().__init__(rf'^(?:{{\w+(?:=[^}}]+)?}})*({cue_symbol}{{1,2}})[^{cue_symbol}]+\1(?:(?:{{/\w+}})*[.?!]?|[.?!]?(?:{{/\w+}})*)$')

