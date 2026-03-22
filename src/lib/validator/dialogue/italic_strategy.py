import re
from ..ivalidator_chain_solo import IValidatorChainSolo


class ItalicStrategy(IValidatorChainSolo):
    """Validator that checks if entire dialogue line is italic.

    Dialogue with italic narration is surrounded entirely by a `{i}line{/i}` tag. This
    usually indicate the speaker is thinking.

    Example:
        mc "{i}Maybe there's food left over.{/i}"
    """

    def __init__(self, next_validator: "IValidatorChainSolo | None" = None) -> None:
        super().__init__(next_validator)
        self._validate_pat = re.compile(r"[^=]+\"{i}(?:(?!{/?i}).)+(?:{/?i})?(?:\s*|\.)?\"")
