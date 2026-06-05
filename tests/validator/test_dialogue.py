import unittest
from lib.validator import IValidatorChain
from lib.validator.rule import DialogueRules
from tests.fixture import get_dialogue_list, validate_solo


class TestDialogue(unittest.TestCase):
    """Test all dialogue related validators."""

    @classmethod
    def setUpClass(cls):
        cls.dialogues = {
            0: '"Jim liked driving around town with his hazard lights on."',
            1: 'mc "Today I heard something new and unmemorable."',
            2: 'my_var = "Today I heard something new and unmemorable."',
            3: '"Narrator" "Today I heard something new and unmemorable."',
            4: "'Today I heard something new and unmemorable.'",
            5: "'Today I heard something new and unmemorable.",
            # parenthesis
            6: '"(Jim liked driving around town with his hazard lights on.)"',
            7: 'mc "He found a (leprechaun in his walnut shell."',
            8: 'mc "He found a (leprechaun in his walnut shell.)"',
            9: 'mc "(He found a (leprechaun in his walnut shell.)"',
            10: 'mc "(He found a (leprechaun in his walnut) shell.)"',
            11: 'mc "He found a (leprechaun in his walnut) shell."',
            12: 'mc "(He found a leprechaun in his walnut shell.)"',
            13: 'mc "(He found a leprechaun in his walnut shell)    "',
            14: 'mc "(He found a leprechaun in his walnut shell)."',
            15: 'mc "(He found a leprechaun in his walnut shell).      "',
            16: 'mc "(He found a leprechaun in his walnut shell).',
            17: "mc '(He found a leprechaun in his walnut shell.)'",
            18: "mc '(He found a leprechaun in his walnut shell.)",
            19: '"Narrator" "He found a (leprechaun in his walnut shell."',
            20: '"Narrator" "He found a (leprechaun in his walnut shell.)"',
            21: '"Narrator" "(He found a (leprechaun in his walnut shell.)"',
            22: '"Narrator" "(He found a (leprechaun in his walnut) shell.)"',
            23: '"Narrator" "He found a (leprechaun in his walnut) shell."',
            24: '"Narrator" "(He found a leprechaun in his walnut shell.)"',
            25: '"Narrator" "(He found a leprechaun in his walnut shell)."',
            26: '"Narrator" "(He found a leprechaun in his walnut shell).      "',
            27: '"Narrator" "(He found a leprechaun in his walnut shell)   "',
            28: "'Narrator' '(He found a leprechaun in his walnut shell).'",
            29: "'Narrator' '(He found a leprechaun in his walnut shell)",
            30: '"Narrator" "(He found a leprechaun in his walnut shell).',
            31: 'myvar = "He found a (leprechaun in his walnut shell.)"',
            32: 'myvar = "He found a (leprechaun in his walnut shell."',
            33: 'myvar = "(He found a (leprechaun in his walnut shell.)"',
            34: 'myvar = "(He found a (leprechaun in his walnut) shell.)"',
            35: 'myvar = "He found a (leprechaun in his walnut) shell."',
            36: 'myvar = "(He found a leprechaun in his walnut shell.)"',
            37: "myvar = '(He found a leprechaun in his walnut shell.)'",
            # italic
            38: '"{i}Jim liked driving around town with his hazard lights on.{/i}"',
            39: 'mc "He found a {i}leprechaun in his walnut shell."',
            40: 'mc "He found a {i}leprechaun in his walnut shell.{/i}"',
            41: 'mc "{i}He found a {i}leprechaun in his walnut shell.{/i}"',
            42: 'mc "{i}He found a {i}leprechaun in his walnut{/i} shell.{/i}"',
            43: 'mc "He found a {i}leprechaun in his walnut{/i} shell."',
            44: 'mc "{i}He found a leprechaun in his walnut shell.{/i}"',
            45: 'mc "{i}He found a leprechaun in his walnut shell."',
            46: 'mc "{i}He found a leprechaun in his walnut shell{/i}."',
            47: 'mc "{i}He found a leprechaun in his walnut shell{/i}.     "',
            48: 'mc "{i}He found a leprechaun in his walnut shell{/i}     "',
            49: "mc '{i}He found a leprechaun in his walnut shell.'",
            50: "mc '{i}He found a leprechaun in his walnut shell.",
            51: 'mc "{i}He found a leprechaun in his walnut shell.',
            52: '"Narrator" "He found a {i}leprechaun in his walnut shell."',
            53: '"Narrator" "He found a {i}leprechaun in his walnut shell.{/i}"',
            54: '"Narrator" "{i}He found a {i}leprechaun in his walnut shell.{/i}"',
            55: '"Narrator" "{i}He found a {i}leprechaun in his walnut{/i} shell.{/i}"',
            56: '"Narrator" "He found a {i}leprechaun in his walnut{/i} shell."',
            57: '"Narrator" "{i}He found a leprechaun in his walnut shell.{/i}"',
            58: '"Narrator" "{i}He found a leprechaun in his walnut shell."',
            59: '"Narrator" "{i}He found a leprechaun in his walnut shell{/i}."',
            60: '"Narrator" "{i}He found a leprechaun in his walnut shell{/i}.    "',
            61: '"Narrator" "{i}He found a leprechaun in his walnut shell{/i}     "',
            62: "'Narrator' '{i}He found a leprechaun in his walnut shell.'",
            63: "'Narrator' '{i}He found a leprechaun in his walnut shell.",
            64: '"Narrator" "{i}He found a leprechaun in his walnut shell.',
            65: 'myvar = "He found a {i}leprechaun in his walnut shell.{/i}"',
            66: 'myvar = "He found a {i}leprechaun in his walnut shell."',
            67: 'myvar = "{i}He found a {i}leprechaun in his walnut shell.{/i}"',
            68: 'myvar = "{i}He found a {i}leprechaun in his walnut{/i} shell.{/i}"',
            69: 'myvar = "He found a {i}leprechaun in his walnut{/i} shell."',
            70: 'myvar = "{i}He found a leprechaun in his walnut shell.{/i}"',
            71: 'myvar = "{i}He found a leprechaun in his walnut shell."',
            72: "myvar = '{i}He found a leprechaun in his walnut shell.'",
            # Custom
            73: '"{fzs}Jim liked driving around town with his hazard lights on.{/fzs}"',
            74: 'mc "He found a {fzs}leprechaun in his walnut shell."',
            75: 'mc "He found a {fzs}leprechaun in his walnut shell.{/fzs}"',
            76: 'mc "{fzs}He found a {fzs}leprechaun in his walnut shell.{/fzs}"',
            77: 'mc "{fzs}He found a {fzs}leprechaun in his walnut{/fzs} shell.{/fzs}"',
            78: 'mc "He found a {fzs}leprechaun in his walnut{/fzs} shell."',
            79: 'mc "{fzs}He found a leprechaun in his walnut shell.{/fzs}"',
            80: 'mc "{fzs}He found a leprechaun in his walnut shell."',
            81: 'mc "{fzs}He found a leprechaun in his walnut shell{/fzs}."',
            82: 'mc "{fzs}He found a leprechaun in his walnut shell{/fzs}.     "',
            83: 'mc "{fzs}He found a leprechaun in his walnut shell{/fzs}      "',
            84: "mc '{fzs}He found a leprechaun in his walnut shell{/fzs}.'",
            85: "mc '{fzs}He found a leprechaun in his walnut shell{/fzs}.",
            86: 'mc "{fzs}He found a leprechaun in his walnut shell{/fzs}.',
            87: 'mc "{fzs=100}He found a leprechaun in his walnut shell.{/fzs}"',
            88: 'mc "{pyw=100}He found a leprechaun in his walnut shell.{/pyw}"',
            89: 'mc "{pyw=100}He found a leprechaun in his walnut shell."',
            90: 'mc "{pyw=100}He found a leprechaun in his walnut shell{/pyw}."',
            91: 'mc "{pyw=100}He found a leprechaun in his walnut shell{/pyw}.     "',
            92: 'mc "{pyw=100}He found a leprechaun in his walnut shell{/pyw}       "',
            93: 'mc "{pyw=100}He found a leprechaun in his walnut shell.{/pyw}',
            94: "mc '{pyw=100}He found a leprechaun in his walnut shell.{/pyw}'",
            95: "mc '{pyw=100}He found a leprechaun in his walnut shell.{/pyw}",
            96: '"Narrator" "He found a {fzs}leprechaun in his walnut shell."',
            97: '"Narrator" "He found a {fzs}leprechaun in his walnut shell.{/fzs}"',
            98: '"Narrator" "{fzs}He found a {fzs}leprechaun in his walnut shell.{/fzs}"',
            99: '"Narrator" "{fzs}He found a {fzs}leprechaun in his walnut{/fzs} shell.{/fzs}"',
            100: '"Narrator" "He found a {fzs}leprechaun in his walnut{/fzs} shell."',
            101: '"Narrator" "{fzs}He found a leprechaun in his walnut shell.{/fzs}"',
            102: '"Narrator" "{fzs}He found a leprechaun in his walnut shell."',
            103: '"Narrator" "{fzs}He found a leprechaun in his walnut shell{/fzs}."',
            104: '"Narrator" "{fzs}He found a leprechaun in his walnut shell{/fzs}.      "',
            105: '"Narrator" "{fzs}He found a leprechaun in his walnut shell{/fzs}    "',
            106: "'Narrator' '{fzs}He found a leprechaun in his walnut shell.{/fzs}'",
            107: "'Narrator' '{fzs}He found a leprechaun in his walnut shell.{/fzs}",
            108: '"Narrator" "{fzs}He found a leprechaun in his walnut shell.{/fzs}',
            109: '"Narrator" "{fzs=100}He found a leprechaun in his walnut shell.{/fzs}"',
            110: '"Narrator" "{fzs=100}He found a leprechaun in his walnut shell."',
            111: '"Narrator" "{fzs=100}He found a leprechaun in his walnut shell{/fzs}."',
            112: '"Narrator" "{fzs=100}He found a leprechaun in his walnut shell{/fzs}.     "',
            113: '"Narrator" "{fzs=100}He found a leprechaun in his walnut shell{/fzs}      "',
            114: '"Narrator" "{color}He found a leprechaun in his walnut shell.{/color}"',
            115: '"Narrator" "{color=100}He found a leprechaun in his walnut shell.{/color}"',
            116: '"Narrator" "{color=red}He found a leprechaun in his walnut shell.{/color}"',
            117: "'Narrator' '{color}He found a leprechaun in his walnut shell.{/color}'",
            118: "'Narrator' '{color}He found a leprechaun in his walnut shell.{/color}",
            119: '"Narrator" "{color}He found a leprechaun in his walnut shell.{/color}',
            120: 'myvar = "He found a {fzs}leprechaun in his walnut shell.{/fzs}"',
            121: 'myvar = "He found a {fzs}leprechaun in his walnut shell."',
            122: 'myvar = "{fzs}He found a {fzs}leprechaun in his walnut shell.{/fzs}"',
            123: 'myvar = "{fzs}He found a {fzs}leprechaun in his walnut{/fzs} shell.{/fzs}"',
            124: 'myvar = "He found a {fzs}leprechaun in his walnut{/fzs} shell."',
            125: 'myvar = "{fzs}He found a leprechaun in his walnut shell.{/fzs}"',
            126: 'myvar = "{fzs}He found a leprechaun in his walnut shell."',
            127: "myvar = '{fzs}He found a leprechaun in his walnut shell.{/fzs}'",
            128: 'myvar = "{fzs=100}He found a leprechaun in his walnut shell.{/fzs}"',
            129: 'myvar = "{pyw=100}He found a leprechaun in his walnut shell.{/pyw}"',
            130: 'myvar = "{pyw=100}He found a leprechaun in his walnut shell."',
            131: "myvar = '{pyw=100}He found a leprechaun in his walnut shell.'",
            #  Expression Cues
            132: '"*Jim liked driving around town with his hazard lights on.*"',
            133: 'mc "Smiles *very softly."',
            134: 'mc "Smiles very *softly*"',
            135: 'mc "*Smiles very *softly*"',
            136: 'mc "*Smiles *very* softly*"',
            137: 'mc "Smiles *very* softly"',
            138: 'mc "*Smiles very softly*"',
            139: 'mc "*Smiles very softly*    "',
            140: 'mc "*Smiles very softly*."',
            141: 'mc "*Smiles very softly*.    "',
            142: 'mc "*Smiles very softly*.',
            143: "mc '*Smiles very softly*.'",
            144: "mc '*Smiles very softly*.",
            145: "mc '**Smiles very softly**.'",
            146: '"Narrator" "Smiles *very softly."',
            147: '"Narrator" "Smiles *very softly*"',
            148: '"Narrator" "*Smiles *very softly*"',
            149: '"Narrator" "*Smiles *very* softly*"',
            150: '"Narrator" "Smiles *very* softly."',
            151: '"Narrator" "*Smiles very softly*"',
            152: '"Narrator" "*Smiles very softly*."',
            153: '"Narrator" "*Smiles very softly*.    "',
            154: '"Narrator" "*Smiles very softly*   "',
            155: '"Narrator" "*Smiles very softly*.',
            156: "'Narrator' '*Smiles very softly*'",
            157: "'Narrator' '*Smiles very softly*",
            158: "'Narrator' '**Smiles very softly**'",
            159: 'myvar = "Smiles *very softly*"',
            160: 'myvar = "Smiles *very softly"',
            161: 'myvar = "*Smiles *very softly*"',
            162: 'myvar = "*Smiles *very* softly*"',
            163: 'myvar = "Smiles *very* softly."',
            164: 'myvar = "*Smiles very softly*"',
            165: "myvar = '*Smiles very softly*'",
            166: "myvar = '**Smiles very softly**'",
            167: '"~Jim liked driving around town with his hazard lights on.~"',
            168: 'mc "Smiles ~very softly."',
            169: 'mc "Smiles very ~softly~"',
            170: 'mc "~Smiles very ~softly~"',
            171: 'mc "~Smiles ~very~ softly~"',
            172: 'mc "Smiles ~very~ softly"',
            173: 'mc "~Smiles very softly~"',
            174: 'mc "~Smiles very softly~    "',
            175: 'mc "~Smiles very softly~."',
            176: 'mc "~Smiles very softly~.     "',
            177: 'mc "~Smiles very softly~',
            178: "mc '~Smiles very softly~'",
            179: "mc '~Smiles very softly~",
            180: '"Narrator" "Smiles ~very softly."',
            181: '"Narrator" "Smiles ~very softly~"',
            182: '"Narrator" "~Smiles ~very softly~"',
            183: '"Narrator" "~Smiles ~very~ softly~"',
            184: '"Narrator" "Smiles ~very~ softly."',
            185: '"Narrator" "~Smiles very softly~"',
            186: '"Narrator" "~Smiles very softly~."',
            187: '"Narrator" "~Smiles very softly~.    "',
            188: '"Narrator" "~Smiles very softly~   "',
            189: '"Narrator" "~Smiles very softly~',
            190: "'Narrator' '~Smiles very softly~'",
            191: "'Narrator' '~Smiles very softly~",
            192: 'myvar = "Smiles ~very softly~"',
            193: 'myvar = "Smiles ~very softly"',
            194: 'myvar = "~Smiles ~very softly~"',
            195: 'myvar = "~Smiles ~very~ softly~"',
            196: 'myvar = "Smiles ~very~ softly."',
            197: 'myvar = "~Smiles very softly~"',
            198: "myvar = '~Smiles very softly~'",
            199: '"Hey! That was not berry nices!',
            200: '"Hey! That was not berry nices!:',
            # with clause
            201: '"Hey! That was not berry nices!" with vpunch',
            202: 'mc "{i}Hey! That was not berry nices!" with vpunch',
            203: 'mc "{i}Hey! That was not berry nices!{/i}" with vpunch',
            204: '"Narrator" "{i}Hey! That was not berry nices!" with vpunch',
            205: '"Narrator" "{i}Hey! That was not berry nices!{/i}" with vpunch',
            206: 'mc "(Hey! That was not berry nices!" with vpunch',
            207: 'mc "(Hey! That was not berry nices!)" with vpunch',
            208: '"Narrator" "(Hey! That was not berry nices!" with vpunch',
            209: '"Narrator" "(Hey! That was not berry nices!)" with vpunch',
            210: 'mc "{fzs}Hey! That was not berry nices!" with vpunch',
            211: 'mc "{fzs}(Hey! That was not berry nices!{/fzs}" with vpunch',
            212: '"Narrator" "{fzs}Hey! That was not berry nices!" with vpunch',
            213: '"Narrator" "{fzs}(Hey! That was not berry nices!{/fzs}" with vpunch',
            214: 'mc "{fzs=100}Hey! That was not berry nices!" with vpunch',
            215: 'mc "{fzs=100}(Hey! That was not berry nices!{/fzs}" with vpunch',
            216: '"Narrator" "{fzs=100}Hey! That was not berry nices!" with vpunch',
            217: '"Narrator" "{fzs=100}(Hey! That was not berry nices!{/fzs}" with vpunch',
            218: 'mc "*Hey! That was not berry nices!*" with vpunch',
            219: 'mc "~Hey! That was not berry nices!~" with vpunch',
            220: '"Narrator" "*Hey! That was not berry nices!*" with vpunch',
            221: '"Narrator" "~Hey! That was not berry nices!~" with vpunch',
            222: '"Narrator" "**Hey! That was not berry nices!**" with vpunch',
            # Italic
            223: 'mc "{i}He found a leprechaun in his walnut shell.{i}"',
            # Custom text tag as parent
            224: 'mc "{tag=10}*Smiles very softly*{/tag}"',
            225: 'mc "{tag}*Smiles very softly*{/tag}"',
            226: 'mc "{tag=10}~Smiles very softly~{/tag}"',
            227: 'mc "{tag}~Smiles very softly~{/tag}"',
            228: 'mc "{tag=10}{i}Smiles very softly{/i}{/tag}"',
            229: 'mc "{tag}{i}Smiles very softly{/i}{/tag}"',
            230: 'mc "{tag=10}(Smiles very softly){/tag}"',
            231: 'mc "{tag}(Smiles very softly){/tag}"',
            232: 'mc "{tag=10}*Smiles very softly*{/tag}" with vpunch',
            233: 'mc "{tag=10}~Smiles very softly~{/tag}" with vpunch',
            234: 'mc "{tag=10}{i}Smiles very softly{/i}{/tag}" with vpunch',
            235: 'mc "{tag=10}(Smiles very softly){/tag}" with vpunch',
            236: 'mc "{tag}*Smiles very softly*"',
            237: 'mc "{tag}~Smiles very softly~"',
            238: 'mc "{tag}{i}Smiles very softly{/i}"',
            239: 'mc "{tag}{i}Smiles very softly"',
            240: 'mc "{tag}(Smiles very softly)"',
            241: 'mc "{tag}(Smiles very softly"',
            # Parentheses
            242: 'mc "(Whenever you are ready! Okay?"',
            243: 'mc "\\(This is going to be difficult to explain.\\)"',
            # Only Periods
            244: 'mc "................."',
            245: 'mc "................." with vpunch',
            246: 'mc "{tag}...............{/tag}"',
            247: 'mc "{tag}...............{/tag}" with vpunch',
            # Parentheses surrounded by escaped quotes
            248: r'mc "\"(Why is this so hard to understand!)\""',
            249: r'mc "\'(Why is this so hard to understand!)\'"',
            # Only Punctuations
            250: 'mc "?????????"',
            251: 'mc "!!!"',
            # space between custom tag and types
            252: 'mc "{tag} {i}Do not move! It will only take a minute...{/i} {/tag}"',
            253: 'mc "{tag} (Do not move! It will only take a minute...) {/tag}"',
            254: 'mc "{tag} **alert!** {/tag}"',
            255: 'mc "{tag} ~~alert!~~ {/tag}"',
            256: 'mc "{tag} .......... {/tag}"',
            # dialogue with arguments
            257: 'mc "Don’t worry about it." (window_background="gui/transparent_textbox.png")',
            258: '"A green hand." (window_background="gui/transparent_textbox.png")',
            259: 'mc "{i}Don’t worry about it.{/i}" (window_background="gui/transparent_textbox.png")',
            260: 'mc "{pyw}Don’t worry about it.{/pyw}" (window_background="gui/transparent_textbox.png")',
            261: 'mc "........." (window_background="gui/transparent_textbox.png")',
            262: 'mc "**groans**" (window_background="gui/transparent_textbox.png")',
            263: 'mc "~~whispers~~" (window_background="gui/transparent_textbox.png")',
            264: 'mc "(Don’t worry about it.)" (window_background="gui/transparent_textbox.png")',
            # Basic narrator with escaped quotes
            265: '"It is almost \\"7:00\\" now!"',
            266: "'It is almost \\'7:00\\' now!'",
            # Guillemets
            267: 'mc "«I am currently thinking about things!»"',
            268: 'mc "‹I am currently thinking about things!›"',
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
        obj = validate_solo(DialogueRules.BASIC.value)
        self.start(obj, [0, 4, 5, 6, 38, 73, 132, 167, 199, 201,258,265,266])

    def test_parenthesis(self):
        obj = validate_solo(DialogueRules.PARENTHESIS.value)
        self.start(obj,
                   [12, 13, 14, 15, 16, 17, 18, 24, 25, 26, 27, 28, 29, 30, 206, 207, 208, 209, 211, 213, 215, 217, 230,
                    231, 235, 240, 241, 242, 243, 248, 249, 253,264])

    def test_italic(self):
        obj = validate_solo(DialogueRules.ITALIC.value)
        self.start(obj,
                   [44, 45, 46, 47, 48, 49, 50, 51, 57, 58, 59, 60, 61, 62, 63, 64, 202, 203, 204, 205, 223, 228, 229,
                    234, 238, 239, 252,259])

    def test_custom_tags(self):
        rule = DialogueRules.TEXT_TAG.value("fzs|pyw")
        obj = validate_solo(rule)
        self.start(
            obj,
            [76, 77, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 98, 99, 101, 102, 103, 104,
             105, 106, 107, 108, 109, 110, 111, 112, 113, 210, 211, 212, 213, 214, 215, 216, 217,260],
        )

    def test_cues_asterisk(self):
        obj = validate_solo(DialogueRules.EXPRESSION_CUE_ASTERISK.value)
        self.start(obj,
                   [138, 139, 140, 141, 143, 145, 151, 152, 153, 154, 156, 158, 218, 220, 222, 224, 225, 232, 236, 254,262])

    def test_cues_tilda(self):
        obj = validate_solo(DialogueRules.EXPRESSION_CUE_TILDA.value)
        self.start(obj,
                   [173, 174, 175, 176, 178, 185, 186, 187, 188, 190, 219, 221, 226, 227, 233, 237, 255,263])

    def test_only_punctuations(self):
        obj = validate_solo(DialogueRules.ONLY_PUNCTUATION.value)
        self.start(obj, [244, 245, 246, 247, 250, 251, 256,261])

    def test_double_guillemet(self):
        obj = validate_solo(DialogueRules.GUILLEMET_DOUBLE.value)
        self.start(obj, [267])

    def test_single_guillemet(self):
        obj = validate_solo(DialogueRules.GUILLEMET_SINGLE.value)
        self.start(obj, [268])