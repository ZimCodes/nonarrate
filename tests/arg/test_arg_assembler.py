import unittest

from lib.arg.arg_assembler import ArgAssembler
from lib.arg.cli_parser import CLIParser
from tests import fixture
from lib.custom_types import FilterTag


class TestArgAssembler(unittest.TestCase):
    def setUp(self) -> None:
        self._parser = CLIParser()

    def eval_validator_chain(self, arg_namespace, correct_count: int, is_quote: bool = False):
        ArgAssembler.assemble(arg_namespace)
        current_validator = arg_namespace.quote_validator if is_quote else arg_namespace.validator
        count = 0
        while current_validator:
            count += 1
            current_validator = current_validator.next_validator
        self.assertEqual(count, correct_count, "Validators does not match correct list.")

    def start(self, args, correct_count: int, is_quote: bool = False):
        arg_namespace = fixture.get_args(self._parser, args)
        self.eval_validator_chain(arg_namespace, correct_count, is_quote)

    def start_escape(self, args, correct_count: int):
        arg_namespace = fixture.get_args(self._parser, args)
        ArgAssembler.assemble(arg_namespace)
        count = 0
        validator = arg_namespace.validator
        while validator:
            count += 1
            validator = validator.next_validator
        self.assertEqual(count, correct_count, "Incorrect number of validators created.")

    def test_no_args(self):
        args = [
            "game/",
            FilterTag.BASIC_CHAR.value,
            FilterTag.ITALIC.value,
            FilterTag.NARRATOR.value,
        ]
        self.start(args, 10)

    def test_nargs(self):
        args = [
            "game/",
            FilterTag.BASIC_CHAR.value,
            FilterTag.ITALIC.value,
            FilterTag.PARENTHESIS.value,
            FilterTag.BASIC_CHAR_OBJ.value,
            FilterTag.NARRATOR.value,
            FilterTag.EXPRESSION_CUES.value,
            FilterTag.ONLY_PUNCTUATIONS.value,
            FilterTag.NONE_CHAR.value,
            FilterTag.NONE_CHAR_OBJ.value,
            FilterTag.GUILLEMETS.value,
            FilterTag.NO_CUSTOM_CHARS.value,
            "ten",
            "narrator",
            FilterTag.NO_CUSTOM_TEXT_TAGS.value,
            "fzs",
            "pyw",
            FilterTag.NO_CUSTOM_CHAR_OBJS.value,
            "narr",
            "ben",
            "karla",
            FilterTag.NO_CUSTOM_CHAR_VAR_OBJS.value,
            "naomi",
            "se",
        ]
        self.start(args, 10)

    def test_regex_chain(self):
        args = [
            "game/",
            FilterTag.BASIC_CHAR.value,
            FilterTag.ITALIC.value,
            FilterTag.PARENTHESIS.value,
            FilterTag.BASIC_CHAR_OBJ.value,
            FilterTag.NARRATOR.value,
            FilterTag.NONE_CHAR_OBJ.value,
            FilterTag.EXPRESSION_CUES.value,
            FilterTag.ONLY_PUNCTUATIONS.value,
            FilterTag.GUILLEMETS.value,
            FilterTag.NONE_CHAR.value,
            "--regex",
            FilterTag.NO_CUSTOM_CHARS.value,
            "ten{3}",
            "seco.+",
            FilterTag.NO_CUSTOM_TEXT_TAGS.value,
            "fzs?",
            "py[Ww]",
        ]
        self.start_escape(args, 3)

    def test_escaping_chain(self):
        args = [
            "game/",
            FilterTag.BASIC_CHAR.value,
            FilterTag.ITALIC.value,
            FilterTag.PARENTHESIS.value,
            FilterTag.BASIC_CHAR_OBJ.value,
            FilterTag.NARRATOR.value,
            FilterTag.NONE_CHAR_OBJ.value,
            FilterTag.EXPRESSION_CUES.value,
            FilterTag.ONLY_PUNCTUATIONS.value,
            FilterTag.NONE_CHAR.value,
            FilterTag.GUILLEMETS.value,
            FilterTag.NO_CUSTOM_CHARS.value,
            "ten{3}",
            "seco.+",
            FilterTag.NO_CUSTOM_TEXT_TAGS.value,
            "fzs?",
            "py[Ww]",
        ]
        self.start_escape(args, 5)

    def test_forced_args(self):
        """Test arguments with forced multiple strategies."""
        args = [
            "game/",
            FilterTag.BASIC_CHAR.value,
            FilterTag.PARENTHESIS.value,
            FilterTag.BASIC_CHAR_OBJ.value,
            FilterTag.NARRATOR.value,
            FilterTag.NONE_CHAR_OBJ.value,
            FilterTag.ONLY_PUNCTUATIONS.value,
            FilterTag.NONE_CHAR.value,
            FilterTag.GUILLEMETS.value,
        ]
        self.start(args,5)

    def test_triple_quote_with_nargs(self):
        args = ["game/", FilterTag.NO_CUSTOM_TEXT_TAGS.value, "plw", "blq"]
        self.start(args, 9, True)
