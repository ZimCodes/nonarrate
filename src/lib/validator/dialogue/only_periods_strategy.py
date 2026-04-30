import re
from ..ivalidator_chain_solo import IValidatorChainSolo


class OnlyPeriodsStrategy(IValidatorChainSolo):
    """Validator that checks if dialogue only consists of periods.

    Dialogue with only periods is a form of silent narration or signify a pause.

    Example:
        mc "............."
        mc "{tag}........................{/tag}"
    """

    def __init__(self, next_validator: "IValidatorChainSolo | None" = None) -> None:
        super().__init__(next_validator)
        self._validate_pat = re.compile(r'^[^=]+([\'"])(?:{\w+(?:=[^}]+)?})*\.+(?:{/\w+})*\s*(?:\1|\1\s*with .+)?$')
