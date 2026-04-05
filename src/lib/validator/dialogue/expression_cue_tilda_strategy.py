import re
from ..ivalidator_chain import IValidatorChain
from .expression_cue_strategy import ExpressionCueStrategy

class ExpressionCueTildaStrategy(ExpressionCueStrategy):
    """Filter for validating lines that are an expression cue surrounded by a tilda.

    Examples:
        mc "~yawns~"
        "~pounces~"
    """

    def __init__(self, next_validator: "IValidatorChain | None" = None) -> None:
        super().__init__(next_validator)
        self._validate_pat = re.compile(r"[^=]+(['\"])~[^~]+~[?.!]?\s*\1")
