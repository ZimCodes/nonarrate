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
            FilterTag.KEEP_COMMON_QUOTED_CHARS.value,
            FilterTag.KEEP_ITALIC.value,
            FilterTag.KEEP_NARRATION.value,
        ]
        self.start(args, 13)

    def test_nargs(self):
        args = [
            "game/",
            FilterTag.KEEP_COMMON_QUOTED_CHARS.value,
            FilterTag.KEEP_ITALIC.value,
            FilterTag.KEEP_PARENTHESIS.value,
            FilterTag.KEEP_COMMON_OBJ_CHARS.value,
            FilterTag.KEEP_NARRATION.value,
            FilterTag.KEEP_EXPRESSION_CUES.value,
            FilterTag.KEEP_PUNCTUATIONS.value,
            FilterTag.KEEP_EMPTY_QUOTED_CHARS.value,
            FilterTag.KEEP_EMPTY_OBJ_CHARS.value,
            FilterTag.KEEP_GUILLEMETS.value,
            FilterTag.KEEP_NVL.value,
            FilterTag.QUOTED_CHARS.value,
            "ten",
            "narrator",
            FilterTag.TEXT_TAGS.value,
            "fzs",
            "pyw",
            FilterTag.OBJ_CHARS.value,
            "narr",
            "ben",
            "karla",
            FilterTag.RENPY_VARS.value,
            "naomi",
            "se",
            FilterTag.PYTHON_VARS.value,
            "myname",
            "llrd",
        ]
        self.start(args, 12)

    def test_regex_chain(self):
        args = [
            "game/",
            FilterTag.KEEP_COMMON_QUOTED_CHARS.value,
            FilterTag.KEEP_ITALIC.value,
            FilterTag.KEEP_PARENTHESIS.value,
            FilterTag.KEEP_COMMON_OBJ_CHARS.value,
            FilterTag.KEEP_NARRATION.value,
            FilterTag.KEEP_EMPTY_OBJ_CHARS.value,
            FilterTag.KEEP_EXPRESSION_CUES.value,
            FilterTag.KEEP_PUNCTUATIONS.value,
            FilterTag.KEEP_GUILLEMETS.value,
            FilterTag.KEEP_NVL.value,
            FilterTag.KEEP_EMPTY_QUOTED_CHARS.value,
            "--regex",
            FilterTag.QUOTED_CHARS.value,
            "ten{3}",
            "seco.+",
            FilterTag.TEXT_TAGS.value,
            "fzs?",
            "py[Ww]",
        ]
        self.start_escape(args, 3)

    def test_escaping_chain(self):
        args = [
            "game/",
            FilterTag.KEEP_COMMON_QUOTED_CHARS.value,
            FilterTag.KEEP_ITALIC.value,
            FilterTag.KEEP_PARENTHESIS.value,
            FilterTag.KEEP_COMMON_OBJ_CHARS.value,
            FilterTag.KEEP_NARRATION.value,
            FilterTag.KEEP_EMPTY_OBJ_CHARS.value,
            FilterTag.KEEP_EXPRESSION_CUES.value,
            FilterTag.KEEP_PUNCTUATIONS.value,
            FilterTag.KEEP_EMPTY_QUOTED_CHARS.value,
            FilterTag.KEEP_GUILLEMETS.value,
            FilterTag.KEEP_NVL.value,
            FilterTag.QUOTED_CHARS.value,
            "ten{3}",
            "seco.+",
            FilterTag.TEXT_TAGS.value,
            "fzs?",
            "py[Ww]",
        ]
        self.start_escape(args, 5)

    def test_forced_args(self):
        """Test arguments with forced multiple strategies."""
        args = [
            "game/",
            FilterTag.KEEP_COMMON_QUOTED_CHARS.value,
            FilterTag.KEEP_PARENTHESIS.value,
            FilterTag.KEEP_COMMON_OBJ_CHARS.value,
            FilterTag.KEEP_NARRATION.value,
            FilterTag.KEEP_EMPTY_OBJ_CHARS.value,
            FilterTag.KEEP_PUNCTUATIONS.value,
            FilterTag.KEEP_EMPTY_QUOTED_CHARS.value,
            FilterTag.KEEP_GUILLEMETS.value,
            FilterTag.KEEP_NVL.value,
        ]
        self.start(args, 5)

    def test_triple_quote_with_nargs(self):
        args = ["game/", FilterTag.TEXT_TAGS.value, "plw", "blq"]
        self.start(args, 9, True)
