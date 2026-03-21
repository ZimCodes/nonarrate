from .object_strategy import ObjectStrategy
from ..ivalidator_chain import IValidatorChain


class BasicObjectStrategy(ObjectStrategy):
    """Validator that validates common speaker names saved to a Character() object.

    This validator will need to first look through all files where the Character object is initially defined
    to work properly.

    Example:
        define narr = Character("Narrator")
    """

    def __init__(
        self,
        next_validator: "IValidatorChain | None" = None,
    ) -> None:
        super().__init__(["[Tt]hinking", "[Tt]houghts?", "[Nn]arrator", "[Mm]ind"], next_validator)
