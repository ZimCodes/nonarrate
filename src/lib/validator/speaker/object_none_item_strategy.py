import re
from .object_strategy import ObjectStrategy
from ..ivalidator_chain import IValidatorChain


class ObjectNoneItemStrategy(ObjectStrategy):
    """Validator that validates a Character(None) object.

    Speakers saved with, Character(None) or Character(), are narrators, as only the dialogue of the speaker will
    be present.
    """

    def __init__(
        self,
        next_validator: "IValidatorChain | None" = None,
    ) -> None:
        super().__init__(None, next_validator)
        ObjectNoneItemStrategy._char_item_pats.append(re.compile(r"Character\s*\(\s*(?:name\s*=\s*)?None.*\)"))
        ObjectNoneItemStrategy._char_item_pats.append(re.compile(r"Character\s*\(\s*\)"))
        ObjectNoneItemStrategy._char_item_pats.append(re.compile(r"Character\s*\(\s*[\"\']\s*[\"\']\s*.*\)"))
        ObjectNoneItemStrategy._char_item_pats.append(
            re.compile(r"Character\s*\((?!\s*[\"\']{2}|\s*name\s?=|\s*None)(?:\s*[\w_]+\s*=\s*.+)+\)")
        )
        # Filters empty translation function, '_()' and '_("")'
        # Ref: https://www.renpy.org/doc/html/translation.html#menu-and-string-translations
        ObjectNoneItemStrategy._char_item_pats.append(re.compile(r"Character\s*\(\s*_\(\s*(?:[\"\']\s*[\"\']\s*)?\)"))
