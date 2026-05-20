from abc import ABC
import re
from ..ivalidator_chain_solo import IValidatorChainSolo
from ..ivalidator_chain import IValidatorChain


class TQExpressionCueStrategy(IValidatorChainSolo, ABC):
    """Validates a line within a triple quote that are only expression cues.

    Example:
        mc\"""We need to get out of here!
            *Yells loudly*
            ~Shrieks~
        Ok! everything's fine!\"""
    """

    def __init__(self, cue_symbol: str, next_validator: "IValidatorChain | None" = None) -> None:
        super().__init__(next_validator)
        self._validate_pat = re.compile(
            rf'^(?:{{\w+(?:=[^}}]+)?}})*({cue_symbol}{{1,2}})[^{cue_symbol}]+\1(?:(?:{{/\w+}})*[.?!]?|[.?!]?(?:{{/\w+}})*)$')
