from ..ivalidator_chain_solo import IValidatorChainSolo
from ..ivalidator_chain import IValidatorChain
import re

class TQParenthesisStrategy(IValidatorChainSolo):
    """Validates a line within a triple quote surrounded by a parenthesis.

    Example:
        narr\"""Hello there!
            (I am inside a parenthesis.)
            We are in this together.\"""
    """

    def __init__(self, next_validator: "IValidatorChain | None" = None) -> None:
        super().__init__(next_validator)
        self._validate_pat = re.compile(r'^(?:{\w+(?:=[^}]+)?})*(?:\\|\\[\'"])?\([^()]+(?:\\?\)(?:\\[\'"])?)?(?:[.?!]?(?:{/\w+})*|(?:{/\w+})*[/?!]?)$')