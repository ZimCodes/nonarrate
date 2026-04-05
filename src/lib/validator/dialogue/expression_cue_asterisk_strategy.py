import re
from ..ivalidator_chain import IValidatorChain
from .expression_cue_strategy import ExpressionCueStrategy

class ExpressionCueAsteriskStrategy(ExpressionCueStrategy):
    """Filter for validating lines that is an expression cue sourrounded by asterisk.

    Example of asterisk expression cues:
        *smiles*
        *Eyes wide in shock*
        *laughing loudly*
        *Raise eyebrows in confusion*
        *blushes*
    """

    def __init__(self, next_validator: "IValidatorChain | None" = None) -> None:
        super().__init__(next_validator)
        self._validate_pat = re.compile(r"[^=]+([\"'])\*[^*]+\*[.?!]?\s*\1")