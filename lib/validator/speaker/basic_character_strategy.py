from .character_strategy import CharacterStrategy
from ..ivalidator_chain import IValidatorChain


class BasicCharacterStrategy(CharacterStrategy):
    """Validator that validates if a character/speaker is a commonly known narrator.

    The speaker must be surrounded by quotes, followed by their dialogue.

    Example:
        "Narrator" "The man grabs his bag and flashes his I.D."
    """

    def __init__(self, next_validator: "IValidatorChain | None" = None) -> None:
        narrators = ["thinking", "thought", "narrator"]
        super().__init__("|".join(narrators), next_validator)
