import re
from ..ivalidator_chain import IValidatorChain


class CharacterStrategy(IValidatorChain):
    """The base validator for validating characters/speakers surrounded by quotation marks.

    Multiple speakers can be validated all at once by making sure each speaker is joined together using '|'
    expression. Example: '|'.join(["apples","bananas","cherry"]).

    Example:
        "dev" "Thank you for playing my Ren'Py game!"
    """

    def __init__(
        self, speaker_name, next_validator: "IValidatorChain | None" = None
    ) -> None:
        super().__init__(next_validator)
        self._regexPat = re.compile(
            rf'".*(?:{speaker_name}).*"\s*"[^"]+"', re.IGNORECASE
        )
