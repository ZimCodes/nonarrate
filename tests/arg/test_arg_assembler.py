import unittest

from lib.arg.arg_assembler import ArgAssembler
from lib.arg.cli_parser import CLIParser
from lib.validator.null_strategy import NullStrategy
from tests import fixture
from lib.custom_types import FilterTag
from lib.validator.speaker import ObjectNoneItemStrategy, ObjectStrategy, CharacterStrategy, BasicObjectStrategy
from lib.validator.dialogue import CustomTextTagStrategy, ParenthesisStrategy


class TestArgAssembler(unittest.TestCase):
    def setUp(self) -> None:
        self._parser = CLIParser()

    def eval_validator_chain(self, arg_namespace, correct_type_list):
        ArgAssembler.assemble(arg_namespace)
        current_validator = arg_namespace.validator
        while current_validator:
            self.assertIn(type(current_validator), correct_type_list)
            current_validator = current_validator.next_validator

    def start(self, args, correct_type_list):
        arg_namespace = fixture.get_args(self._parser, args)
        self.eval_validator_chain(arg_namespace, correct_type_list)

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
            FilterTag.ITALIC_NARR.value,
            FilterTag.BASIC_NARR.value,
        ]
        self.start(args, {NullStrategy, ObjectNoneItemStrategy, ParenthesisStrategy, BasicObjectStrategy})

    def test_nargs(self):
        args = [
            "game/",
            FilterTag.BASIC_CHAR.value,
            FilterTag.ITALIC_NARR.value,
            FilterTag.PARENTHESIS_NARR.value,
            FilterTag.BASIC_CHAR_OBJ.value,
            FilterTag.BASIC_NARR.value,
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
        ]
        self.start(
            args, {NullStrategy, ObjectNoneItemStrategy, CustomTextTagStrategy, CharacterStrategy, ObjectStrategy}
        )

    def test_regex_chain(self):
        args = [
            "game/",
            FilterTag.BASIC_CHAR.value,
            FilterTag.ITALIC_NARR.value,
            FilterTag.PARENTHESIS_NARR.value,
            FilterTag.BASIC_CHAR_OBJ.value,
            FilterTag.BASIC_NARR.value,
            FilterTag.NONE_CHAR_OBJ.value,
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
            FilterTag.ITALIC_NARR.value,
            FilterTag.PARENTHESIS_NARR.value,
            FilterTag.BASIC_CHAR_OBJ.value,
            FilterTag.BASIC_NARR.value,
            FilterTag.NONE_CHAR_OBJ.value,
            FilterTag.NO_CUSTOM_CHARS.value,
            "ten{3}",
            "seco.+",
            FilterTag.NO_CUSTOM_TEXT_TAGS.value,
            "fzs?",
            "py[Ww]",
        ]
        self.start_escape(args, 5)
