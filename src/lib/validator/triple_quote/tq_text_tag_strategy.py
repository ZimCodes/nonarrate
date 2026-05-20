import re
from ..ivalidator_chain_solo import IValidatorChainSolo
from ..ivalidator_chain_solo import IValidatorChain

class TQTextTagStrategy(IValidatorChainSolo):
    """Validates a line in a multiline triple quote surrounded by a custom text tag.

    Example:
        mc\"""
            {bgc=100}This is a dialogue sequence{/bgc}
        \"""
    """

    def __init__(self, tag_name:str, next_validator: "IValidatorChain | None" = None) -> None:
        super().__init__(next_validator)
        self._validate_pat = re.compile(rf'^(?!.*"""){{(?:{tag_name})(?:=[^}}]+)?}}.+(?:{{/?(?:{tag_name})}})?[.?!]?$')