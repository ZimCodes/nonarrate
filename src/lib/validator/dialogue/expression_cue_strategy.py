import re
from ..ivalidator_chain_solo import IValidatorChainSolo
from ..ivalidator_chain import IValidatorChain


class ExpressionCueStrategy(IValidatorChainSolo):
    """Filter for removing lines that is only an expression cue.

    Example of expression cues:
        *smiles*
        *Eyes wide in shock*
        *laughing loudly*
        *Raise eyebrows in confusion*
        *blushes*
    """

    def __init__(self, next_validator: "IValidatorChain | None" = None) -> None:
        super().__init__(next_validator)
        self._validate_pat = re.compile(r"[^=]+\"\*[^\*]+\*\s*\"")
