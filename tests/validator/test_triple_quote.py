import unittest

from lib.validator.triple_quote import *


class TestTripleQuote(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.phrase = "Water is very important, Martha!"

    def test_parenthesis(self):
        validator = TQParenthesisStrategy()
        self.assertTrue(validator.is_valid(f"({self.phrase})"), "plain parenthesis")
        self.assertFalse(validator.is_valid(f"(){self.phrase})"), "invalid plain parenthesis")
        self.assertTrue(validator.is_valid(f"{{bzs}}({self.phrase}){{/bzs}}"), "parenthesis surrounded by text tag")
        self.assertFalse(validator.is_valid(f"{{bzs}}(){self.phrase}){{/bzs}}"),
                         "invalid parenthesis surrounded by text tag")
        self.assertFalse(validator.is_valid(f'({self.phrase})"""'), "plain parenthesis w/ triple quote end")
        self.assertFalse(validator.is_valid(f'"""({self.phrase})'), "plain parenthesis w/ triple quote start")

    def test_asterisk_cue(self):
        validator = TQExpressionCueAsteriskStrategy()
        self.assertTrue(validator.is_valid("*Pop!*"), "single asterisk cue")
        self.assertTrue(validator.is_valid("{gha}*Pop!*{/gha}"), "single asterisk cue surrounded by text tag")
        self.assertTrue(validator.is_valid("**Pop!**"), "double asterisks cue")
        self.assertTrue(validator.is_valid("{gha}**Pop!**{/gha}"), "double asterisks cue surrounded by text tag")
        self.assertFalse(validator.is_valid('*Pop!*"""'), "single asterisk cue w/ triple quote end")
        self.assertFalse(validator.is_valid('"""*Pop!*'), "single asterisk cue w/ triple quote start")

    def test_tilda_cue(self):
        validator = TQExpressionCueTildaStrategy()
        self.assertTrue(validator.is_valid("~Pop!~"), "single tilda cue")
        self.assertTrue(validator.is_valid("{gha}~Pop!~{/gha}"), "single tilda cue surrounded by text tag")
        self.assertTrue(validator.is_valid("~~Pop!~~"), "double tildas cue")
        self.assertTrue(validator.is_valid("{gha}~~Pop!~~{/gha}"), "double tildas cue surrounded by text tag")

    def test_only_punctuation(self):
        validator = TQOnlyPunctuationStrategy()
        self.assertTrue(validator.is_valid("......."), "only periods")
        self.assertTrue(validator.is_valid("{fe}.......{/fe}"), "only periods surrounded by text tag")
        self.assertTrue(validator.is_valid("!!!!!!!"), "only exclamation marks")
        self.assertTrue(validator.is_valid("{fe}!!!!!!!{/fe}"), "only exclamation marks surrounded by text tag")
        self.assertTrue(validator.is_valid("???????"), "only question marks")
        self.assertTrue(validator.is_valid("{fe}???????{/fe}"), "only question marks surrounded by text tag")
        self.assertFalse(validator.is_valid("Hey???????"), "invalid only question marks")
        self.assertFalse(validator.is_valid('""".......'), "only periods w/ triple quote start")
        self.assertFalse(validator.is_valid('......."""'), "only periods w/ triple quote end")

    def test_italic(self):
        validator = TQItalicStrategy()
        self.assertTrue(validator.is_valid(f'{{i}}{self.phrase}{{/i}}'), "italic tags")
        self.assertTrue(validator.is_valid(f'{{fe}}{{i}}{self.phrase}{{/i}}{{/fe}}'),
                        "italic tags surrounded by text tag")
        self.assertFalse(validator.is_valid(f'{{i}}{self.phrase}{{/i}}"""'), "italic tags w/ triple quote end")
        self.assertFalse(validator.is_valid(f'"""{{i}}{self.phrase}{{/i}}'), "italic tags w/ triple quote start")

    def test_text_tag(self):
        validator = TQTextTagStrategy("poi")
        self.assertTrue(validator.is_valid(f'{{poi}}{self.phrase}{{/poi}}'), "text tag")
        self.assertFalse(validator.is_valid(f'"""{{poi}}{self.phrase}{{/poi}}'), "text tag w/ triple quote start")
        self.assertFalse(validator.is_valid(f'{{poi}}{self.phrase}{{/poi}}"""'), "text tag w/ triple quote end")
