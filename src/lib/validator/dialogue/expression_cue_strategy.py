import abc
from ..ivalidator_chain_solo import IValidatorChainSolo
from ..ivalidator_chain import IValidatorChain
import re


class ExpressionCueStrategy(IValidatorChainSolo,abc.ABC):
    """Filter for removing lines that is only expression cue(s)."""

    def __init__(self, cue_symbol:str, next_validator: "IValidatorChain | None" = None) -> None:
        super().__init__(next_validator)
        self._validate_pat = re.compile(rf"[^=]+([\"'])(?:{{\w+(?:=[^}}]+)?}})*({cue_symbol}{{1,2}})[^{cue_symbol}]+\2(?:(?:{{/\w+}})*[.?!]?|[.?!]?(?:{{/\w+}})*)\s*\1(?:\s*with .+)?")
