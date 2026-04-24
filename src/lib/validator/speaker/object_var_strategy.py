import re
from .object_strategy import ObjectStrategy
from ..ivalidator_chain import IValidatorChain

class ObjectVarStrategy(ObjectStrategy):
    """Validator that validates Character objects by their variable name.

    Validate Character objects based on their variable name.
    Example:
        define pt = Character("Kat")
        'pt' is the variable name of the character object.
        pt "...."
        Whenever variable 'pt' is present, it will be removed.
    """

    def __init__(self, var_items: str | list[str], next_validator: "IValidatorChain | None" = None) -> None:
        super().__init__(None, next_validator)
        if type(var_items) is list:
            var_items = "|".join(var_items)
        ObjectVarStrategy._char_item_pats.append(re.compile(rf"^(?:define|default)\s+\b(?:{var_items})\b"))