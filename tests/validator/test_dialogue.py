import unittest
from lib.validator.dialogue import (
    ParenthesisStrategy,
    ItalicStrategy,
    CustomTextTagStrategy,
    BasicStrategy,
)
from lib.validator.ivalidator_chain import IValidatorChain
from ..fixture import get_dialogue_list


class TestDialogue(unittest.TestCase):
    """Test all dialogue related validators."""

    @classmethod
    def setUpClass(cls):
        cls.dialogues = {
            0: '"Jim liked driving around town with his hazard lights on."',
            1: 'mc "Today I heard something new and unmemorable."',
            2: 'my_var = "Today I heard something new and unmemorable."',
            3: '"Narrator" "Today I heard something new and unmemorable."',
            # parenthesis
            4: '"(Jim liked driving around town with his hazard lights on.)"',
            5: 'mc "He found a (leprechaun in his walnut shell."',
            6: 'mc "He found a (leprechaun in his walnut shell.)"',
            7: 'mc "(He found a (leprechaun in his walnut shell.)"',
            8: 'mc "(He found a (leprechaun in his walnut) shell.)"',
            9: 'mc "He found a (leprechaun in his walnut) shell."',
            10: 'mc "(He found a leprechaun in his walnut shell.)"',
            11: '"Narrator" "He found a (leprechaun in his walnut shell."',
            12: '"Narrator" "He found a (leprechaun in his walnut shell.)"',
            13: '"Narrator" "(He found a (leprechaun in his walnut shell.)"',
            14: '"Narrator" "(He found a (leprechaun in his walnut) shell.)"',
            15: '"Narrator" "He found a (leprechaun in his walnut) shell."',
            16: '"Narrator" "(He found a leprechaun in his walnut shell.)"',
            17: 'myvar = "He found a (leprechaun in his walnut shell.)"',
            18: 'myvar = "He found a (leprechaun in his walnut shell."',
            19: 'myvar = "(He found a (leprechaun in his walnut shell.)"',
            20: 'myvar = "(He found a (leprechaun in his walnut) shell.)"',
            21: 'myvar = "He found a (leprechaun in his walnut) shell."',
            22: 'myvar = "(He found a leprechaun in his walnut shell.)"',
            # italic
            23: '"{i}Jim liked driving around town with his hazard lights on.{/i}"',
            24: 'mc "He found a {i}leprechaun in his walnut shell."',
            25: 'mc "He found a {i}leprechaun in his walnut shell.{/i}"',
            26: 'mc "{i}He found a {i}leprechaun in his walnut shell.{/i}"',
            27: 'mc "{i}He found a {i}leprechaun in his walnut{/i} shell.{/i}"',
            28: 'mc "He found a {i}leprechaun in his walnut{/i} shell."',
            29: 'mc "{i}He found a leprechaun in his walnut shell.{/i}"',
            30: '"Narrator" "He found a {i}leprechaun in his walnut shell."',
            31: '"Narrator" "He found a {i}leprechaun in his walnut shell.{/i}"',
            32: '"Narrator" "{i}He found a {i}leprechaun in his walnut shell.{/i}"',
            33: '"Narrator" "{i}He found a {i}leprechaun in his walnut{/i} shell.{/i}"',
            34: '"Narrator" "He found a {i}leprechaun in his walnut{/i} shell."',
            35: '"Narrator" "{i}He found a leprechaun in his walnut shell.{/i}"',
            36: 'myvar = "He found a {i}leprechaun in his walnut shell.{/i}"',
            37: 'myvar = "He found a {i}leprechaun in his walnut shell."',
            38: 'myvar = "{i}He found a {i}leprechaun in his walnut shell.{/i}"',
            39: 'myvar = "{i}He found a {i}leprechaun in his walnut{/i} shell.{/i}"',
            40: 'myvar = "He found a {i}leprechaun in his walnut{/i} shell."',
            41: 'myvar = "{i}He found a leprechaun in his walnut shell.{/i}"',
            # Custom
            42: '"{fzs}Jim liked driving around town with his hazard lights on.{/fzs}"',
            43: 'mc "He found a {fzs}leprechaun in his walnut shell."',
            44: 'mc "He found a {fzs}leprechaun in his walnut shell.{/fzs}"',
            45: 'mc "{fzs}He found a {fzs}leprechaun in his walnut shell.{/fzs}"',
            46: 'mc "{fzs}He found a {fzs}leprechaun in his walnut{/fzs} shell.{/fzs}"',
            47: 'mc "He found a {fzs}leprechaun in his walnut{/fzs} shell."',
            48: 'mc "{fzs}He found a leprechaun in his walnut shell.{/fzs}"',
            49: 'mc "{fzs=100}He found a leprechaun in his walnut shell.{/fzs}"',
            50: 'mc "{pyw=100}He found a leprechaun in his walnut shell.{/pyw}"',
            51: '"Narrator" "He found a {fzs}leprechaun in his walnut shell."',
            52: '"Narrator" "He found a {fzs}leprechaun in his walnut shell.{/fzs}"',
            53: '"Narrator" "{fzs}He found a {fzs}leprechaun in his walnut shell.{/fzs}"',
            54: '"Narrator" "{fzs}He found a {fzs}leprechaun in his walnut{/fzs} shell.{/fzs}"',
            55: '"Narrator" "He found a {fzs}leprechaun in his walnut{/fzs} shell."',
            56: '"Narrator" "{fzs}He found a leprechaun in his walnut shell.{/fzs}"',
            57: '"Narrator" "{fzs=100}He found a leprechaun in his walnut shell.{/fzs}"',
            58: 'myvar = "He found a {fzs}leprechaun in his walnut shell.{/fzs}"',
            59: 'myvar = "He found a {fzs}leprechaun in his walnut shell."',
            60: 'myvar = "{fzs}He found a {fzs}leprechaun in his walnut shell.{/fzs}"',
            61: 'myvar = "{fzs}He found a {fzs}leprechaun in his walnut{/fzs} shell.{/fzs}"',
            62: 'myvar = "He found a {fzs}leprechaun in his walnut{/fzs} shell."',
            63: 'myvar = "{fzs}He found a leprechaun in his walnut shell.{/fzs}"',
            64: 'myvar = "{fzs=100}He found a leprechaun in his walnut shell.{/fzs}"',
            65: 'myvar = "{pyw=100}He found a leprechaun in his walnut shell.{/pyw}"',
        }

    def validate_lines(self):
        valid_lines, invalid_lines = get_dialogue_list(self.valid_indexes, TestDialogue.dialogues)
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

    def test_basic(self):
        self.start(BasicStrategy(), [0, 4, 23, 42])

    def test_parenthesis(self):
        self.start(ParenthesisStrategy(), [10, 16])

    def test_italic(self):
        self.start(ItalicStrategy(), [29, 35])

    def test_custom(self):
        self.start(CustomTextTagStrategy("fzs|pyw"), [45, 46, 48, 49, 50, 53, 54, 56, 57])
