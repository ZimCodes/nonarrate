import unittest
from tests.fixture import get_dialogue_list,validate_solo,validate_obj
from lib.validator import ObjectStrategy, IValidatorChain
from lib.custom_types import FileInfo
from lib.validator.rule import SpeakerRules


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
                    "define empty = Character()",
                    "define empty2 = Character(    )",
                    'define po = Character   ("")',
                    'define pop = Character( "" , what_color="FFFF00")',
                    'define pop2 = Character( " " , what_color="FFFF00")',
                    "define pop3 = Character( ' ' , what_color=\"FFFF00\")",
                    "define pop4 = Character( '' , what_color=\"FFFF00\")",
                    'define b_ = Character("Balum", what_italic=True)',
                    'define bi_ = Character("Bilf",what_color="#FFFF00", what_italic=True)',
                    'define bik_ = Character("Bikwaski", what_color="#FFFF00", what_italic= True)',
                    'define bik_g = Character("Big Guy", what_color="#FFFF00", what_italic = True)',
                    'default sind = Character("", what_color="#FFFF00", what_italic = True)',
                    'default nigel = Character("Nigel", "", what_italic = True)',
                    'define zy = Character(ctc="ctc_animation", ctc_position="fixed", window_top_padding = -60)',
                    "define none2 = Character(name=None)",
                    'define none3 = Character(None,ctc="ctc_animation", ctc_position="fixed", window_top_padding = -60)',
                    'define none4 = Character(name=None, ctc="ctc_animation", ctc_position="fixed", window_top_padding = -60)',
                    "default translate = Character(_())",
                    'default translate2 = Character(_(""))',
                    "default translate3 = Character(_(''))",
                    "default translate4 = Character( _(''))",
                    "default translate5 = Character( _( ' ' ))",
                    'define think = Character("{i}Thoughts{i}")',
                    'define ci = Character("[persistent.player_name]", color="#4169e1", what_suffix="{/i}", what_prefix="{i}")',
                    'define miami = Character("Miami\'s Inner Monologue")',
                    'define miami2 = Character("Miami\'s Inner voice")',
                    'define miami3 = Character("Miami\'s inner Monologue")',
                    'default dynamic = DynamicCharacter("My Mind")',
                    'default dynamic2 = DynamicCharacter("Marco")',
                    'default dynamic3 = DynamicCharacter("")',
                    'default dynamic4 = DynamicCharacter(_())',
                    'default nvl_narr = nvl_narrator',
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
            34: "'Caliek' 'Today I heard something new and unmemorable.",
            # Custom Object
            35: 'marco "And so the story would move forward."',
            36: 'kelly "And so the story would move forward."',
            37: 'Marco "And so the story would move forward."',
            38: 'marc "And so the story would move forward."',
            39: 'carsi "And so the story would move forward."',
            40: 'blanka "And so the story would move forward."',
            41: 'narr "And so the story would move forward."',
            42: 'nik_mind "And so the story would move forward."',
            43: 'miyai "And so the story would move forward."',
            44: 'miyaki "And so the story would move forward."',
            45: 'loval "And so the story would move forward."',
            46: 'none "And so the story would move forward."',
            47: 'not_here "And so the story would move forward."',
            48: 'ip "And so the story would move forward."',
            49: 'l "And so the story would move forward."',
            50: 'uma "And so the story would move forward."',
            51: 'not_now "And so the story would move forward."',
            52: 'b_ "And so the story would move forward."',
            53: 'bi_ "And so the story would move forward."',
            54: 'bik_ "And so the story would move forward."',
            55: 'bik_g "And so the story would move forward."',
            56: 'po "And so the story would move forward."',
            57: 'pop "And so the story would move forward."',
            58: 'sind "And so the story would move forward."',
            59: 'nigel "And so the story would move forward."',
            60: 'zy "And so the story would move forward."',
            61: 'none2 "And so the story would move forward."',
            62: 'none3 "And so the story would move forward."',
            63: 'none4 "And so the story would move forward."',
            64: 'pop2 "And so the story would move forward."',
            65: 'pop3 "And so the story would move forward."',
            66: 'pop4 "And so the story would move forward."',
            67: 'translate "And so the story would move forward."',
            68: 'translate2 "And so the story would move forward."',
            69: 'translate3 "And so the story would move forward."',
            70: 'translate4 "And so the story would move forward."',
            71: 'translate5 "And so the story would move forward."',
            72: 'empty "And so the story would move forward."',
            73: 'empty2 "And so the story would move forward."',
            # with clause
            74: '"Narrator" "Today I heard something new and unmemorable." with vpunch',
            75: '"maya" "Today I heard something new and unmemorable." with vpunch',
            76: "'Caliek' 'Today I heard something new and unmemorable.' with vpunch",
            77: 'marco "And so the story would move forward." with vpunch',
            78: 'carsi "And so the story would move forward." with vpunch',
            79: 'none "And so the story would move forward." with vpunch',
            80: 'b_ "And so the story would move forward." with vpunch',
            81: 'l "And so the story would move forward." with vpunch',
            82: 'think "And so the story would move forward." with vpunch',
            # Empty quote speaker
            83: '"" "But oh man, how wrong I was..."',
            84: '"  " "But oh man, how wrong I was..."',
            # what_prefix italics
            85: 'ci "Maybe I shouldn\'t have done that."',
            # More default narrators
            86: 'miami "Jason headed slowly to the car."',
            87: 'miami2 "Jason headed slowly to the car."',
            88: 'miami3 "Jason headed slowly to the car."',
            89: '"Miami\'s inner voice" "Jason headed slowly to the car."',
            90: '"Miami\'s inner monologue" "Jason headed slowly to the car."',
            91: '"Miami\'s Inner monologue" "Jason headed slowly to the car."',
            92: '"Miami\'s Inner Voice" "Jason headed slowly to the car."',
            # DynamicCharacter object
            93: 'dynamic "It was dusty and tattered, with strange symbols and markings."',
            94: 'dynamic2 "It was dusty and tattered, with strange symbols and markings."',
            95: 'dynamic3 "It was dusty and tattered, with strange symbols and markings."',
            96: 'dynamic4 "It was dusty and tattered, with strange symbols and markings."',
            # NVL narrator
            97: 'nvl_narr "The mystery deepened."',
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
            validate_solo(SpeakerRules.CHARACTER_BASIC.value),
            [3, 7, 8, 9, 10, 11, 12, 13, 14, 22, 23, 24, 25, 26, 27, 33, 74, 89, 90, 91, 92],
        )

    def test_custom_char(self):
        rule = SpeakerRules.CHARACTER.value("maya")
        obj = validate_solo(rule)
        self.start(obj, [21, 22, 23, 24, 25, 26, 27, 31, 32, 33, 75])
        # Single quotes and multi line test
        rule = SpeakerRules.CHARACTER.value("Caliek")
        obj = validate_solo(rule)
        self.start(obj, [34, 76])

    def test_object_char(self):
        rule = SpeakerRules.OBJECT.value("Marco")
        obj = validate_obj(rule)
        self.start_object(obj, [35, 77, 94])

    def test_object_char_item(self):
        rule = SpeakerRules.OBJECT.value("base")
        obj = validate_obj(rule)
        self.start_object(obj, [39, 40, 50, 78])

    def test_basic_object_char(self):
        obj = validate_obj(SpeakerRules.OBJECT_BASIC.value)
        self.start_object(obj, [35, 41, 42, 44, 45, 48, 77, 82, 86, 87, 88,93])

    def test_object_none_char_item(self):
        obj = validate_obj(SpeakerRules.OBJECT_NONE.value)
        self.start_object(
            obj,
            [46, 47, 51, 56, 57, 58, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 79,95,96]
        )

    def test_chaining(self):
        obj = validate_obj(SpeakerRules.OBJECT_BASIC.value, validate_obj(SpeakerRules.OBJECT.value("base")))
        self.start_object(obj,
                          [35, 39, 40, 41, 42, 44, 45, 48, 50, 77, 78, 82, 86, 87, 88,93])

    def test_spaces(self):
        """Test spaces between character object and calling parenthesis.

        Example:
            default n = Character     ('Nadia')
        """
        obj = validate_obj([SpeakerRules.OBJECT.value("Linda"),SpeakerRules.OBJECT.value("Umeha")])
        self.start_object(obj, [49, 50, 81])

    def test_italic_object(self):
        """Test if Character object has 'what_italic=True' parameter."""
        obj = validate_obj(SpeakerRules.OBJECT_ITALIC.value)
        self.start_object(obj, [52, 53, 54, 55, 58, 59, 80, 82, 85])

    def test_object_var(self):
        obj = validate_obj(SpeakerRules.OBJECT_VAR.value("pop"))
        self.start_object(obj, [57])

    def test_empty_char(self):
        obj = validate_solo(SpeakerRules.CHARACTER_NONE.value)
        self.start(obj, [83, 84])

    def test_nvl(self):
        obj = validate_obj(SpeakerRules.NVL_BASIC.value)
        self.start_object(obj,[97])