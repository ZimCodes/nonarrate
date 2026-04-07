import re
from ..ivalidator_chain_solo import IValidatorChainSolo


class CustomTextTagStrategy(IValidatorChainSolo):
    """Validator that checks if dialogue line is surrounded by a custom text tag.

    A text tag is created by a developer to add custom effects. It can usually indicate thoughts & narration.
    The syntax of a text tag is seen as so, `{tag}{/tag}` OR `{tag=value}{/tag}`.

    Example:
        elnor "{fzs}This is a small bold font tag.{/fzs}
        gabby "{ba=100}Big bold asterisk text!{/ba}
    """

    def __init__(self, tag_name: str, next_validator: "IValidatorChainSolo | None" = None) -> None:
        super().__init__(next_validator)
        self._validate_pat = re.compile(rf'[^=]+([\'"]){{(?:{tag_name})(?:=[^}}]+)?}}.+(?:{{/?(?:{tag_name})}})?[.?!]?\s*(?:\1|\1\s*with .+)?')