import unittest
from lib.validator.dialogue import (
    ParenthesisStrategy,
    ItalicStrategy,
    CustomTextTagStrategy,
    BasicStrategy,
    ExpressionCueStrategy,
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
            11: 'mc "(He found a leprechaun in his walnut shell)    "',
            12: 'mc "(He found a leprechaun in his walnut shell)."',
            13: '"Narrator" "He found a (leprechaun in his walnut shell."',
            14: '"Narrator" "He found a (leprechaun in his walnut shell.)"',
            15: '"Narrator" "(He found a (leprechaun in his walnut shell.)"',
            16: '"Narrator" "(He found a (leprechaun in his walnut) shell.)"',
            17: '"Narrator" "He found a (leprechaun in his walnut) shell."',
            18: '"Narrator" "(He found a leprechaun in his walnut shell.)"',
            19: '"Narrator" "(He found a leprechaun in his walnut shell)."',
            20: '"Narrator" "(He found a leprechaun in his walnut shell)   "',
            21: 'myvar = "He found a (leprechaun in his walnut shell.)"',
            22: 'myvar = "He found a (leprechaun in his walnut shell."',
            23: 'myvar = "(He found a (leprechaun in his walnut shell.)"',
            24: 'myvar = "(He found a (leprechaun in his walnut) shell.)"',
            25: 'myvar = "He found a (leprechaun in his walnut) shell."',
            26: 'myvar = "(He found a leprechaun in his walnut shell.)"',
            # italic
            27: '"{i}Jim liked driving around town with his hazard lights on.{/i}"',
            28: 'mc "He found a {i}leprechaun in his walnut shell."',
            29: 'mc "He found a {i}leprechaun in his walnut shell.{/i}"',
            30: 'mc "{i}He found a {i}leprechaun in his walnut shell.{/i}"',
            31: 'mc "{i}He found a {i}leprechaun in his walnut{/i} shell.{/i}"',
            32: 'mc "He found a {i}leprechaun in his walnut{/i} shell."',
            33: 'mc "{i}He found a leprechaun in his walnut shell.{/i}"',
            34: 'mc "{i}He found a leprechaun in his walnut shell."',
            35: 'mc "{i}He found a leprechaun in his walnut shell{/i}."',
            36: 'mc "{i}He found a leprechaun in his walnut shell{/i}     "',
            37: '"Narrator" "He found a {i}leprechaun in his walnut shell."',
            38: '"Narrator" "He found a {i}leprechaun in his walnut shell.{/i}"',
            39: '"Narrator" "{i}He found a {i}leprechaun in his walnut shell.{/i}"',
            40: '"Narrator" "{i}He found a {i}leprechaun in his walnut{/i} shell.{/i}"',
            41: '"Narrator" "He found a {i}leprechaun in his walnut{/i} shell."',
            42: '"Narrator" "{i}He found a leprechaun in his walnut shell.{/i}"',
            43: '"Narrator" "{i}He found a leprechaun in his walnut shell."',
            44: '"Narrator" "{i}He found a leprechaun in his walnut shell{/i}."',
            45: '"Narrator" "{i}He found a leprechaun in his walnut shell{/i}     "',
            46: 'myvar = "He found a {i}leprechaun in his walnut shell.{/i}"',
            47: 'myvar = "He found a {i}leprechaun in his walnut shell."',
            48: 'myvar = "{i}He found a {i}leprechaun in his walnut shell.{/i}"',
            49: 'myvar = "{i}He found a {i}leprechaun in his walnut{/i} shell.{/i}"',
            50: 'myvar = "He found a {i}leprechaun in his walnut{/i} shell."',
            51: 'myvar = "{i}He found a leprechaun in his walnut shell.{/i}"',
            52: 'myvar = "{i}He found a leprechaun in his walnut shell."',
            # Custom
            53: '"{fzs}Jim liked driving around town with his hazard lights on.{/fzs}"',
            54: 'mc "He found a {fzs}leprechaun in his walnut shell."',
            55: 'mc "He found a {fzs}leprechaun in his walnut shell.{/fzs}"',
            56: 'mc "{fzs}He found a {fzs}leprechaun in his walnut shell.{/fzs}"',
            57: 'mc "{fzs}He found a {fzs}leprechaun in his walnut{/fzs} shell.{/fzs}"',
            58: 'mc "He found a {fzs}leprechaun in his walnut{/fzs} shell."',
            59: 'mc "{fzs}He found a leprechaun in his walnut shell.{/fzs}"',
            60: 'mc "{fzs}He found a leprechaun in his walnut shell."',
            61: 'mc "{fzs}He found a leprechaun in his walnut shell{/fzs}."',
            62: 'mc "{fzs}He found a leprechaun in his walnut shell{/fzs}      "',
            63: 'mc "{fzs=100}He found a leprechaun in his walnut shell.{/fzs}"',
            64: 'mc "{pyw=100}He found a leprechaun in his walnut shell.{/pyw}"',
            65: 'mc "{pyw=100}He found a leprechaun in his walnut shell."',
            66: 'mc "{pyw=100}He found a leprechaun in his walnut shell{/pyw}."',
            67: 'mc "{pyw=100}He found a leprechaun in his walnut shell{/pyw}       "',
            68: '"Narrator" "He found a {fzs}leprechaun in his walnut shell."',
            69: '"Narrator" "He found a {fzs}leprechaun in his walnut shell.{/fzs}"',
            70: '"Narrator" "{fzs}He found a {fzs}leprechaun in his walnut shell.{/fzs}"',
            71: '"Narrator" "{fzs}He found a {fzs}leprechaun in his walnut{/fzs} shell.{/fzs}"',
            72: '"Narrator" "He found a {fzs}leprechaun in his walnut{/fzs} shell."',
            73: '"Narrator" "{fzs}He found a leprechaun in his walnut shell.{/fzs}"',
            74: '"Narrator" "{fzs}He found a leprechaun in his walnut shell."',
            75: '"Narrator" "{fzs}He found a leprechaun in his walnut shell{/fzs}."',
            76: '"Narrator" "{fzs}He found a leprechaun in his walnut shell{/fzs}    "',
            77: '"Narrator" "{fzs=100}He found a leprechaun in his walnut shell.{/fzs}"',
            78: '"Narrator" "{fzs=100}He found a leprechaun in his walnut shell."',
            79: '"Narrator" "{fzs=100}He found a leprechaun in his walnut shell{/fzs}."',
            80: '"Narrator" "{fzs=100}He found a leprechaun in his walnut shell{/fzs}      "',
            81: '"Narrator" "{color}He found a leprechaun in his walnut shell.{/color}"',
            82: '"Narrator" "{color=100}He found a leprechaun in his walnut shell.{/color}"',
            83: '"Narrator" "{color=red}He found a leprechaun in his walnut shell.{/color}"',
            84: 'myvar = "He found a {fzs}leprechaun in his walnut shell.{/fzs}"',
            85: 'myvar = "He found a {fzs}leprechaun in his walnut shell."',
            86: 'myvar = "{fzs}He found a {fzs}leprechaun in his walnut shell.{/fzs}"',
            87: 'myvar = "{fzs}He found a {fzs}leprechaun in his walnut{/fzs} shell.{/fzs}"',
            88: 'myvar = "He found a {fzs}leprechaun in his walnut{/fzs} shell."',
            89: 'myvar = "{fzs}He found a leprechaun in his walnut shell.{/fzs}"',
            90: 'myvar = "{fzs}He found a leprechaun in his walnut shell."',
            91: 'myvar = "{fzs=100}He found a leprechaun in his walnut shell.{/fzs}"',
            92: 'myvar = "{pyw=100}He found a leprechaun in his walnut shell.{/pyw}"',
            93: 'myvar = "{pyw=100}He found a leprechaun in his walnut shell."',
            #  Expression Cues
            94: '"*Jim liked driving around town with his hazard lights on.*"',
            95: 'mc "Smiles *very softly."',
            96: 'mc "Smiles very *softly*"',
            97: 'mc "*Smiles very *softly*"',
            98: 'mc "*Smiles *very* softly*"',
            99: 'mc "Smiles *very* softly"',
            100: 'mc "*Smiles very softly*"',
            101: 'mc "*Smiles very softly*    "',
            102: 'mc "*Smiles very softly*."',
            103: '"Narrator" "Smiles *very softly."',
            104: '"Narrator" "Smiles *very softly*"',
            105: '"Narrator" "*Smiles *very softly*"',
            106: '"Narrator" "*Smiles *very* softly*"',
            107: '"Narrator" "Smiles *very* softly."',
            108: '"Narrator" "*Smiles very softly*"',
            109: '"Narrator" "*Smiles very softly*."',
            110: '"Narrator" "*Smiles very softly*   "',
            111: 'myvar = "Smiles *very softly*"',
            112: 'myvar = "Smiles *very softly"',
            113: 'myvar = "*Smiles *very softly*"',
            114: 'myvar = "*Smiles *very* softly*"',
            115: 'myvar = "Smiles *very* softly."',
            116: 'myvar = "*Smiles very softly*"',
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
        self.start(BasicStrategy(), [0, 4, 27, 53, 94])

    def test_parenthesis(self):
        self.start(ParenthesisStrategy(), [10, 11, 12, 18, 19, 20])

    def test_italic(self):
        self.start(ItalicStrategy(), [33, 34, 35, 36, 42, 43, 44, 45])

    def test_custom_tags(self):
        self.start(
            CustomTextTagStrategy("fzs|pyw"),
            [56, 57, 59, 60, 61, 62, 63, 64, 65, 66, 67, 70, 71, 73, 74, 75, 76, 77, 78, 79, 80],
        )

    def test_cues(self):
        self.start(ExpressionCueStrategy(), [100, 101, 108, 110])
