import re
from lib.custom_types import FileInfo
from lib.validator.rule import Rule
from .ivalidator_chain import IValidatorChain


class ObjectStrategy(IValidatorChain):
    """Base validator for validating speakers/characters stored in a Character() object.

    This validator will need to first look through all files where the Character object is initially defined
    to work properly.

    Example:
        define lily = Character("Lily")
    """

    __obj_name_pat = re.compile(r"^\s*(?:\$|(?:define|default))\s+(\w+)")
    _speaker_objects: set[str] = set()
    _char_item_pats: list[re.Pattern] = list()
    _validate_pat: "re.Pattern | None" = None

    def __init__(
        self,
            char_items: Rule | list[Rule],
            next_validator: "IValidatorChain | None" = None,
    ) -> None:
        super().__init__(next_validator)
        if type(char_items) is list:
            self.__init_char_items(char_items)
        else:
            self.__init_char_items([char_items])

    @classmethod
    def __init_char_items(cls, char_items: list[Rule]):
        for rule in char_items:
            cls._char_item_pats.append(rule.pattern)

    @classmethod
    def reset(cls):
        """Reset class attributes and compiled regex."""
        cls._char_item_pats[:] = []
        cls._speaker_objects.clear()

    @classmethod
    def define_speakers(cls, file_infos: list[FileInfo]):
        """Gather object names of speakers saved to a Character() object.

        Any text inside the Character object's parenthesis can be used to target a specific
        speaker. For instance, in 'narr = Character(kind=base)', 'base' can be used to identify the Character object
        to target, which is 'narr'.

        Args:
            file_infos: list of all files and their content.
        """
        for file_info in file_infos:
            for line in file_info.lines:
                if any(char_pat.search(line) for char_pat in cls._char_item_pats):
                    speaker_matches = cls.__obj_name_pat.match(line) if cls.__obj_name_pat else None
                    speaker = speaker_matches.group(1) if speaker_matches else None
                    if speaker:
                        cls._speaker_objects.add(speaker)
        if cls._speaker_objects:
            joined_speakers = "|".join(cls._speaker_objects)
            cls._validate_pat = re.compile(rf"\b(?:{joined_speakers})\b.+")

    def is_valid(self, line: str) -> bool:
        if self._validate_pat and self._validate_pat.match(line):
            return True
        elif self._next_validator:
            return self._next_validator.is_valid(line)
        return False
