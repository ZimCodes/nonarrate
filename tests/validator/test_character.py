import unittest
from ..fixture import get_dialogue_list
from lib.validator.speaker import (
    ObjectNoneItemStrategy,
    BasicCharacterStrategy,
    CharacterStrategy,
    ObjectStrategy,
    BasicObjectStrategy,
)
from lib.validator.ivalidator_chain import IValidatorChain
from lib.custom_types import FileInfo


class TestCharacter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.character_definitions = [
            FileInfo(
                "file.rpy",
                [
                    'define narr = Character("Narrator")',
                    'default narr = Character("Narrator")',
                    'define nik_mind = Character("Nik\'s Mind")',
                    'default nik_mind = Character("Nik\'s Mind")',
                    'define miyaki = Character("Miyaki Thoughts")',
                    'default miyaki = Character("Miyaki Thoughts")',
                    'define loval = Character("Loval Thought")',
                    'default loval = Character("Loval Thought")',
                    'default marco = Character("Marco Thinking")',
                    'define marco = Character("Marco Thinking")',
                    'define carsi = Character("Carsi", kind=base)',
                    'default blanka = Character("Blanka", kind=base)',
                    "define none = Character(None)",
                    "default not_here = Character(None)",
                    "default not_now = Character     (None)",
                    'default ip = Character ("Ipol Thought")',
                    'define uma = Character  ("Umeha", kind=base)',
                    'define l = Character   ("Linda")',
                ],
            )
        ]
        cls.dialogues = {
            0: '"Jim liked driving around town with his hazard lights on."',
            1: 'mc "Today I heard something new and unmemorable."',
            2: 'my_var = "Today I heard something new and unmemorable."',
            3: '"Narrator" "Today I heard something new and unmemorable."',
            4: '"developer" "Today I heard something new and unmemorable."',
            5: 'dev" "Today I heard something new and unmemorable."',
            6: '"dev "Today I heard something new and unmemorable."',
            7: '"narrator" "Today I heard something new and unmemorable."',
            8: '"nichole thinking" "Today I heard something new and unmemorable."',
            9: '"Mira Thinking" "Today I heard something new and unmemorable."',
            10: '"Leon\'s thoughts" "Today I heard something new and unmemorable."',
            11: '"angela\'s Thoughts" "Today I heard something new and unmemorable."',
            12: '"angela\'s Thought" "Today I heard something new and unmemorable."',
            13: '"My Mind" "Today I heard something new and unmemorable."',
            14: '"My mind" "Today I heard something new and unmemorable."',
            15: '"Mymind" "Today I heard something new and unmemorable."',
            16: '"MyMind" "Today I heard something new and unmemorable."',
            17: 'narrator" "Today I heard something new and unmemorable."',
            18: '"narrator "Today I heard something new and unmemorable."',
            19: 'narrator "Today I heard something new and unmemorable."',
            # Custom basic
            20: '"mayaa" "Today I heard something new and unmemorable."',
            21: '"maya" "Today I heard something new and unmemorable."',
            22: '"maya thinking" "Today I heard something new and unmemorable."',
            23: '"maya Thinking" "Today I heard something new and unmemorable."',
            24: '"maya thoughts" "Today I heard something new and unmemorable."',
            25: '"maya Thoughts" "Today I heard something new and unmemorable."',
            26: '"maya\'s mind" "Today I heard something new and unmemorable."',
            27: '"maya\'s Mind" "Today I heard something new and unmemorable."',
            28: 'maya" "Today I heard something new and unmemorable."',
            29: '"maya "Today I heard something new and unmemorable."',
            30: 'maya "Today I heard something new and unmemorable."',
            31: '"maya cornstarke" "Today I heard something new and unmemorable."',
            32: '"Maya" "Today I heard something new and unmemorable."',
            33: '"Maya\'s Mind" "Today I heard something new and unmemorable."',
            # Custom Object
            34: 'marco "And so the story would move forward."',
            35: 'kelly "And so the story would move forward."',
            36: 'Marco "And so the story would move forward."',
            37: 'marc "And so the story would move forward."',
            38: 'carsi "And so the story would move forward."',
            39: 'blanka "And so the story would move forward."',
            40: 'narr "And so the story would move forward."',
            41: 'nik_mind "And so the story would move forward."',
            42: 'miyai "And so the story would move forward."',
            43: 'miyaki "And so the story would move forward."',
            44: 'loval "And so the story would move forward."',
            45: 'none "And so the story would move forward."',
            46: 'not_here "And so the story would move forward."',
            47: 'ip "And so the story would move forward."',
            48: 'l "And so the story would move forward."',
            49: 'uma "And so the story would move forward."',
            50: 'not_now "And so the story would move forward."',
        }

    def setUp(self) -> None:
        ObjectStrategy.reset()

    def validate_lines(self):
        valid_lines, invalid_lines = get_dialogue_list(self.valid_indexes, TestCharacter.dialogues)
        for line in valid_lines:
            with self.subTest(line=line):
                self.assertTrue(self.validator.is_valid(line), line)
        for line in invalid_lines:
            with self.subTest(line=line):
                self.assertFalse(self.validator.is_valid(line), line)

    def start(self, strategy: IValidatorChain, valid_indexes: list[int]):
        self.validator = strategy
        self.valid_indexes = valid_indexes
        self.validate_lines()

    def start_object(self, strategy: ObjectStrategy, valid_indexes: list[int]):
        strategy.define_speakers(TestCharacter.character_definitions)
        self.start(strategy, valid_indexes)

    def test_basic_char(self):
        self.start(
            BasicCharacterStrategy(),
            [3, 7, 8, 9, 10, 11, 12, 13, 14, 22, 23, 24, 25, 26, 27, 33],
        )

    def test_custom_char(self):
        self.start(CharacterStrategy("maya"), [21, 22, 23, 24, 25, 26, 27, 31, 32, 33])

    def test_object_char(self):
        self.start_object(ObjectStrategy("Marco"), [34])

    def test_object_char_item(self):
        self.start_object(ObjectStrategy("base"), [38, 39, 49])

    def test_basic_object_char(self):
        self.start_object(BasicObjectStrategy(), [34, 40, 41, 43, 44, 47])

    def test_object_none_char_item(self):
        self.start_object(ObjectNoneItemStrategy(), [45, 46, 50])

    def test_chaining(self):
        self.start_object(BasicObjectStrategy(ObjectStrategy("base")), [34, 38, 39, 40, 41, 43, 44, 47, 49])

    def test_spaces(self):
        """Test spaces between character object and calling parenthesis.

        Example:
            default n = Character     ('Nadia')
        """
        self.start_object(ObjectStrategy(["Linda", "Umeha"]), [48, 49])
