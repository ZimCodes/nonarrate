import re
from ..ivalidator_chain_solo import IValidatorChainSolo


class ParenthesisStrategy(IValidatorChainSolo):
    """Validator that checks if dialogue line is surrounded by a parenthesis pair.

    Dialogue surrounded by a `()` pair are known to indicate the speaker is thinking.

    Example:
        mc "(It's got to be here somewhere.)"
    """

    def __init__(self, next_validator: "IValidatorChainSolo | None" = None) -> None:
        super().__init__(next_validator)
        self._validate_pat = re.compile(r'^[^=]+"\([^()]+\)"$')
