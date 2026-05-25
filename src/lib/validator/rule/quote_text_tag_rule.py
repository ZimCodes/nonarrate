from .rule import Rule

class QuoteTextTagRule(Rule):
    """Quote rule for text tags."""

    def __init__(self, tag_name: str):
        super().__init__(rf'^(?!.*"""){{(?:{tag_name})(?:=[^}}]+)?}}.+(?:{{/?(?:{tag_name})}})?[.?!]?(?<!")$')

