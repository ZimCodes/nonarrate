from ..ivalidator_chain_solo import IValidatorChainSolo
from ..ivalidator_chain import IValidatorChain
import re

class TQItalicStrategy(IValidatorChainSolo):
    """Validates italics inside a mutli-line triple quote dialogue.

    Example:
        mc\"""
        {i}This is a piece of dialogue.{/i}
        \"""
    """

    def __init__(self, next_validator: "IValidatorChain | None" = None) -> None:
        super().__init__(next_validator)
        self._validate_pat = re.compile(r'^(?:{\w+(?:=[^}]+)?})*\{i\}((?:(?!\{/?i\}).)+)(?:\{/?i\})?(?:[.?!]?(?:{/\w+})*|(?:{/\w+})*[/?!]?)$')