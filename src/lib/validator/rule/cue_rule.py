from .rule import Rule

class CueRule(Rule):
    """Holds validator filter rule for expression cue rule."""

    def __init__(self,cue_symbol:str):
        super().__init__(rf"[^=]+([\"'])(?:{{\w+(?:=[^}}]+)?}})*\s*({cue_symbol}{{1,2}})[^{cue_symbol}]+\2\s*(?:(?:{{/\w+}})*[.?!]?|[.?!]?(?:{{/\w+}})*)\s*\1(?:\s*with .+)?")
