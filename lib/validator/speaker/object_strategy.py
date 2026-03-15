import re
from lib.custom_types import FileInfo
from ..ivalidator_chain import IValidatorChain


class ObjectStrategy(IValidatorChain):
    """Base validator for validating speakers/characters stored in a Character() object.

    This validator will need to first look through all files where the Character object is initially defined
    to work properly.

    Example:
        define lily = Character("Lily")
    """

    def __init__(
        self,
        char_item: str | list[str] | None,
        next_validator: "IValidatorChain | None" = None,
    ) -> None:
        super().__init__(next_validator)
        self._obj_name_pat = re.compile(r"^(?:define|default)\s+(\w+)")
        self.__init_char_item(char_item)
        self._speaker_objects = set()

    def __init_char_item(self, char_item):
        if type(char_item) is list:
            char_item = "|".join(char_item)
        if char_item:
            self._char_item_pat = re.compile(rf"Character\(.*\b(?:{char_item})\b[^)]*\)")

    def define_speakers(self, file_infos: list[FileInfo]):
        """Gather object names of speakers saved to a Character() object.

        Any text inside the Character object's parenthesis can be used to target a specific
        speaker. For instance, in 'narr = Character(kind=base)', 'base' can be used to identify the Character object
        to target, which is 'narr'.

        Args:
            file_infos: list of all files and their content.
        """
        for file_info in file_infos:
            for line in (line for lines in file_info.values() for line in lines):
                if self._char_item_pat.search(line):
                    speaker_matches = self._obj_name_pat.match(line) if self._obj_name_pat else None
                    speaker = speaker_matches.group(1) if speaker_matches else None
                    if speaker:
                        self._speaker_objects.add(speaker)
        if self._speaker_objects:
            joined_speakers = "|".join(self._speaker_objects)
            self._validate_pat = re.compile(rf"\b(?:{joined_speakers})\b.+")
