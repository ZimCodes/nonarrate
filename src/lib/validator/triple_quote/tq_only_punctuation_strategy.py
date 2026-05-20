import re
from ..ivalidator_chain_solo import IValidatorChainSolo
from ..ivalidator_chain import IValidatorChain

class TQOnlyPunctuationStrategy(IValidatorChainSolo):
    """Validates a line in a multi-line triple quote containing only a punctuation.

    Example:
        mc\"""
            ......
        \"""
    """

    def __init__(self, next_validator: "IValidatorChain | None" = None) -> None:
        super().__init__(next_validator)
        self._validate_pat = re.compile(r'^(?:{\w+(?:=[^}]+)?})*[.?!]+(?:{/\w+})*$')
