import unittest

from lib.validator.rule import QuoteRules
from tests.fixture import validate_solo


class TestQuote(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.phrase = "Water is very important, Martha!"

    def valid(self, validator, test_phrase, fail_msg):
        self.assertTrue(validator.is_valid(test_phrase), fail_msg)

    def invalid(self, validator, test_phrase, fail_msg):
        self.assertFalse(validator.is_valid(test_phrase), fail_msg)

    def test_parenthesis(self):
        validator = validate_solo(QuoteRules.PARENTHESIS.value)
        self.valid(validator,f"({self.phrase})", "plain parenthesis")
        self.invalid(validator,f"(){self.phrase})", "invalid plain parenthesis")
        self.valid(validator,f"{{bzs}}({self.phrase}){{/bzs}}", "parenthesis surrounded by text tag")
        self.valid(validator,f"{{bzs}} ({self.phrase}) {{/bzs}}",
                        "spaced parenthesis surrounded by text tag")
        self.invalid(validator,f"{{bzs}}(){self.phrase}){{/bzs}}",
                         "invalid parenthesis surrounded by text tag")
        self.invalid(validator,f'({self.phrase})"""', "plain parenthesis w/ triple quote end")
        self.invalid(validator,f'"""({self.phrase})', "plain parenthesis w/ triple quote start")
        self.invalid(validator,f'({self.phrase})"', "plain parenthesis w/ single quote end")
        self.invalid(validator,f'"({self.phrase})', "plain parenthesis w/ single quote start")

    def test_asterisk_cue(self):
        validator = validate_solo(QuoteRules.EXPRESSION_CUE_ASTERISK.value)
        self.valid(validator,"*Pop!*", "single asterisk cue")
        self.valid(validator,"{gha}*Pop!*{/gha}", "single asterisk cue surrounded by text tag")
        self.valid(validator,"**Pop!**", "double asterisks cue")
        self.valid(validator,"{gha}**Pop!**{/gha}", "double asterisks cue surrounded by text tag")
        self.valid(validator,"{gha} **Pop!** {/gha}",
                        "spaced double asterisks cue surrounded by text tag")
        self.invalid(validator,'*Pop!*"""', "single asterisk cue w/ triple quote end")
        self.invalid(validator,'"""*Pop!*', "single asterisk cue w/ triple quote start")
        self.invalid(validator,'*Pop!*"', "single asterisk cue w/ single quote end")
        self.invalid(validator,'"*Pop!*', "single asterisk cue w/ single quote start")

    def test_tilda_cue(self):
        validator = validate_solo(QuoteRules.EXPRESSION_CUE_TILDA.value)
        self.valid(validator,"~Pop!~", "single tilda cue")
        self.valid(validator,"{gha}~Pop!~{/gha}", "single tilda cue surrounded by text tag")
        self.valid(validator,"{gha} ~Pop!~ {/gha}", "spaced single tilda cue surrounded by text tag")
        self.valid(validator,"~~Pop!~~", "double tildas cue")
        self.valid(validator,"{gha}~~Pop!~~{/gha}", "double tildas cue surrounded by text tag")
        self.valid(validator,"{gha} ~~Pop!~~ {/gha}", "spaced double tildas cue surrounded by text tag")

    def test_only_punctuation(self):
        validator = validate_solo(QuoteRules.ONLY_PUNCTUATION.value)
        self.valid(validator,".......", "only periods")
        self.valid(validator,"{fe}.......{/fe}", "only periods surrounded by text tag")
        self.valid(validator,"!!!!!!!", "only exclamation marks")
        self.valid(validator,"{fe}!!!!!!!{/fe}", "only exclamation marks surrounded by text tag")
        self.valid(validator,"???????", "only question marks")
        self.valid(validator,"{fe}???????{/fe}", "only question marks surrounded by text tag")
        self.valid(validator,"{fe} ??????? {/fe}", "spaced only question marks surrounded by text tag")
        self.invalid(validator,"Hey???????", "invalid only question marks")
        self.invalid(validator,'""".......', "only periods w/ triple quote start")
        self.invalid(validator,'......."""', "only periods w/ triple quote end")
        self.invalid(validator,'".......', "only periods w/ single quote start")
        self.invalid(validator,'......."', "only periods w/ single quote end")

    def test_italic(self):
        validator = validate_solo(QuoteRules.ITALIC.value)
        self.valid(validator,f'{{i}}{self.phrase}{{/i}}', "italic tags")
        self.valid(validator,f'{{fe}}{{i}}{self.phrase}{{/i}}{{/fe}}',
                        "italic tags surrounded by text tag")
        self.valid(validator, f'{{fe}} {{i}}{self.phrase}{{/i}} {{/fe}}',
                   "spaced italic tags surrounded by text tag")
        self.invalid(validator, f'{{i}}{self.phrase}{{/i}}"""', "italic tags w/ triple quote end")
        self.invalid(validator, f'"""{{i}}{self.phrase}{{/i}}', "italic tags w/ triple quote start")
        self.invalid(validator, f'{{i}}{self.phrase}{{/i}}"', "italic tags w/ single quote end")
        self.invalid(validator, f'"{{i}}{self.phrase}{{/i}}', "italic tags w/ single quote start")

    def test_text_tag(self):
        rule = QuoteRules.TEXT_TAG.value("poi")
        validator = validate_solo(rule)
        self.valid(validator, f'{{poi}}{self.phrase}{{/poi}}', "text tag")
        self.invalid(validator, f'"""{{poi}}{self.phrase}{{/poi}}', "text tag w/ triple quote start")
        self.invalid(validator, f'{{poi}}{self.phrase}{{/poi}}"""', "text tag w/ triple quote end")
        self.invalid(validator, f'"{{poi}}{self.phrase}{{/poi}}', "text tag w/ single quote start")
        self.invalid(validator, f'{{poi}}{self.phrase}{{/poi}}"', "text tag w/ single quote end")

    def test_guillemets(self):
        # Single Guillemets
        SINGLE = ['‹', '›']
        validator = validate_solo(QuoteRules.GUILLEMET_SINGLE.value)
        self.valid(validator,f'{SINGLE[0]}{self.phrase}{SINGLE[1]}',"single guillemets")
        self.valid(validator,f'{{tag}}{SINGLE[0]}{self.phrase}{SINGLE[1]}{{/tag}}',"single guillemets w/ text tag")
        self.invalid(validator,f'"""{SINGLE[0]}{self.phrase}{SINGLE[1]}',"single guillemets w/ triple quote start")
        self.invalid(validator,f'{SINGLE[0]}{self.phrase}{SINGLE[1]}"""',"single guillemets w/ triple quote end")
        # Double Guillemets
        DOUBLE = ['«', '»']
        validator = validate_solo(QuoteRules.GUILLEMET_DOUBLE.value)
        self.valid(validator,f'{DOUBLE[0]}{self.phrase}{DOUBLE[1]}',"double guillemets")
        self.valid(validator,f'{{tag}}{DOUBLE[0]}{self.phrase}{DOUBLE[1]}{{/tag}}',"double guillemets w/ text tag")
        self.invalid(validator,f'"""{DOUBLE[0]}{self.phrase}{DOUBLE[1]}',"double guillemets w/ triple quote start")
        self.invalid(validator,f'{DOUBLE[0]}{self.phrase}{DOUBLE[1]}"""',"double guillemets w/ triple quote end")
