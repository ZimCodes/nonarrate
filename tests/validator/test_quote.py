import unittest

from lib.validator.rule import QuoteRules
from tests.fixture import validate_solo


class TestQuote(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.phrase = "Water is very important, Martha!"

    def test_parenthesis(self):
        validator = validate_solo(QuoteRules.PARENTHESIS.value)
        self.assertTrue(validator.is_valid(f"({self.phrase})"), "plain parenthesis")
        self.assertFalse(validator.is_valid(f"(){self.phrase})"), "invalid plain parenthesis")
        self.assertTrue(validator.is_valid(f"{{bzs}}({self.phrase}){{/bzs}}"), "parenthesis surrounded by text tag")
        self.assertTrue(validator.is_valid(f"{{bzs}} ({self.phrase}) {{/bzs}}"), "spaced parenthesis surrounded by text tag")
        self.assertFalse(validator.is_valid(f"{{bzs}}(){self.phrase}){{/bzs}}"),
                         "invalid parenthesis surrounded by text tag")
        self.assertFalse(validator.is_valid(f'({self.phrase})"""'), "plain parenthesis w/ triple quote end")
        self.assertFalse(validator.is_valid(f'"""({self.phrase})'), "plain parenthesis w/ triple quote start")
        self.assertFalse(validator.is_valid(f'({self.phrase})"'), "plain parenthesis w/ single quote end")
        self.assertFalse(validator.is_valid(f'"({self.phrase})'), "plain parenthesis w/ single quote start")

    def test_asterisk_cue(self):
        validator = validate_solo(QuoteRules.EXPRESSION_CUE_ASTERISK.value)
        self.assertTrue(validator.is_valid("*Pop!*"), "single asterisk cue")
        self.assertTrue(validator.is_valid("{gha}*Pop!*{/gha}"), "single asterisk cue surrounded by text tag")
        self.assertTrue(validator.is_valid("**Pop!**"), "double asterisks cue")
        self.assertTrue(validator.is_valid("{gha}**Pop!**{/gha}"), "double asterisks cue surrounded by text tag")
        self.assertTrue(validator.is_valid("{gha} **Pop!** {/gha}"), "spaced double asterisks cue surrounded by text tag")
        self.assertFalse(validator.is_valid('*Pop!*"""'), "single asterisk cue w/ triple quote end")
        self.assertFalse(validator.is_valid('"""*Pop!*'), "single asterisk cue w/ triple quote start")
        self.assertFalse(validator.is_valid('*Pop!*"'), "single asterisk cue w/ single quote end")
        self.assertFalse(validator.is_valid('"*Pop!*'), "single asterisk cue w/ single quote start")

    def test_tilda_cue(self):
        validator = validate_solo(QuoteRules.EXPRESSION_CUE_TILDA.value)
        self.assertTrue(validator.is_valid("~Pop!~"), "single tilda cue")
        self.assertTrue(validator.is_valid("{gha}~Pop!~{/gha}"), "single tilda cue surrounded by text tag")
        self.assertTrue(validator.is_valid("{gha} ~Pop!~ {/gha}"), "spaced single tilda cue surrounded by text tag")
        self.assertTrue(validator.is_valid("~~Pop!~~"), "double tildas cue")
        self.assertTrue(validator.is_valid("{gha}~~Pop!~~{/gha}"), "double tildas cue surrounded by text tag")
        self.assertTrue(validator.is_valid("{gha} ~~Pop!~~ {/gha}"), "spaced double tildas cue surrounded by text tag")

    def test_only_punctuation(self):
        validator = validate_solo(QuoteRules.ONLY_PUNCTUATION.value)
        self.assertTrue(validator.is_valid("......."), "only periods")
        self.assertTrue(validator.is_valid("{fe}.......{/fe}"), "only periods surrounded by text tag")
        self.assertTrue(validator.is_valid("!!!!!!!"), "only exclamation marks")
        self.assertTrue(validator.is_valid("{fe}!!!!!!!{/fe}"), "only exclamation marks surrounded by text tag")
        self.assertTrue(validator.is_valid("???????"), "only question marks")
        self.assertTrue(validator.is_valid("{fe}???????{/fe}"), "only question marks surrounded by text tag")
        self.assertTrue(validator.is_valid("{fe} ??????? {/fe}"), "spaced only question marks surrounded by text tag")
        self.assertFalse(validator.is_valid("Hey???????"), "invalid only question marks")
        self.assertFalse(validator.is_valid('""".......'), "only periods w/ triple quote start")
        self.assertFalse(validator.is_valid('......."""'), "only periods w/ triple quote end")
        self.assertFalse(validator.is_valid('".......'), "only periods w/ single quote start")
        self.assertFalse(validator.is_valid('......."'), "only periods w/ single quote end")

    def test_italic(self):
        validator = validate_solo(QuoteRules.ITALIC.value)
        self.assertTrue(validator.is_valid(f'{{i}}{self.phrase}{{/i}}'), "italic tags")
        self.assertTrue(validator.is_valid(f'{{fe}}{{i}}{self.phrase}{{/i}}{{/fe}}'),
                        "italic tags surrounded by text tag")
        self.assertTrue(validator.is_valid(f'{{fe}} {{i}}{self.phrase}{{/i}} {{/fe}}'),
                        "spaced italic tags surrounded by text tag")
        self.assertFalse(validator.is_valid(f'{{i}}{self.phrase}{{/i}}"""'), "italic tags w/ triple quote end")
        self.assertFalse(validator.is_valid(f'"""{{i}}{self.phrase}{{/i}}'), "italic tags w/ triple quote start")
        self.assertFalse(validator.is_valid(f'{{i}}{self.phrase}{{/i}}"'), "italic tags w/ single quote end")
        self.assertFalse(validator.is_valid(f'"{{i}}{self.phrase}{{/i}}'), "italic tags w/ single quote start")

    def test_text_tag(self):
        rule = QuoteRules.TEXT_TAG.value("poi")
        validator = validate_solo(rule)
        self.assertTrue(validator.is_valid(f'{{poi}}{self.phrase}{{/poi}}'), "text tag")
        self.assertFalse(validator.is_valid(f'"""{{poi}}{self.phrase}{{/poi}}'), "text tag w/ triple quote start")
        self.assertFalse(validator.is_valid(f'{{poi}}{self.phrase}{{/poi}}"""'), "text tag w/ triple quote end")
        self.assertFalse(validator.is_valid(f'"{{poi}}{self.phrase}{{/poi}}'), "text tag w/ single quote start")
        self.assertFalse(validator.is_valid(f'{{poi}}{self.phrase}{{/poi}}"'), "text tag w/ single quote end")
