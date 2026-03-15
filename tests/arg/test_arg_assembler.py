import unittest

from lib.arg.arg_assembler import ArgAssembler
from lib.arg.cli_parser import CLIParser
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

    def test_no_args(self):
        args = [
            "game/",
            FilterTag.NO_BASIC_CHAR.value,
            FilterTag.NO_ITALIC_NARR.value,
            FilterTag.NO_BASIC_NARR.value,
        ]
        self.start(args, {ObjectNoneItemStrategy, ParenthesisStrategy, BasicObjectStrategy})

    def test_nargs(self):
        args = [
            "game/",
            FilterTag.NO_BASIC_CHAR.value,
            FilterTag.NO_ITALIC_NARR.value,
            FilterTag.NO_PARENTHESIS_NARR.value,
            FilterTag.NO_BASIC_CHAR_OBJ.value,
            FilterTag.NO_BASIC_NARR.value,
            FilterTag.CUSTOM_CHAR.value,
            "ten",
            "narrator",
            FilterTag.CUSTOM_TEXT_TAG.value,
            "fzs",
            "pyw",
            FilterTag.CUSTOM_CHAR_OBJ.value,
            "narr",
            "ben",
            "karla",
        ]
        self.start(args, {ObjectNoneItemStrategy, CustomTextTagStrategy, CharacterStrategy, ObjectStrategy})
