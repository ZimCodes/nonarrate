import unittest

from lib.arg.arg_assembler import ArgAssembler
from lib.arg.cli_parser import CLIParser
from lib.validator.null_strategy import NullStrategy
from tests import fixture
from lib.custom_types import FilterTag
from lib.validator.speaker import ObjectNoneItemStrategy, ObjectStrategy, CharacterStrategy, BasicObjectStrategy, \
    ItalicObjectStrategy, ObjectVarStrategy
from lib.validator.dialogue import CustomTextTagStrategy, ParenthesisStrategy, ExpressionCueAsteriskStrategy, \
    ExpressionCueTildaStrategy, ItalicStrategy


class TestArgAssembler(unittest.TestCase):
    def setUp(self) -> None:
        self._parser = CLIParser()

    def eval_validator_chain(self, arg_namespace, correct_type_list):
        ArgAssembler.assemble(arg_namespace)
        current_validator = arg_namespace.validator
        validators = set()
        while current_validator:
            validators.add(type(current_validator))
            current_validator = current_validator.next_validator
        self.assertCountEqual(validators, correct_type_list, "Validators does not match correct list.")

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
        self.start(args, {NullStrategy, ObjectNoneItemStrategy, ParenthesisStrategy, BasicObjectStrategy,
                          ExpressionCueAsteriskStrategy,ExpressionCueTildaStrategy})

    def test_nargs(self):
        args = [
            "game/",
            FilterTag.BASIC_CHAR.value,
            FilterTag.ITALIC_NARR.value,
            FilterTag.PARENTHESIS_NARR.value,
            FilterTag.BASIC_CHAR_OBJ.value,
            FilterTag.BASIC_NARR.value,
            FilterTag.EXPRESSION_CUES.value,
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
        self.start(
            args, {NullStrategy, ObjectNoneItemStrategy, CustomTextTagStrategy, CharacterStrategy, ObjectStrategy,ObjectVarStrategy}
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
            FilterTag.EXPRESSION_CUES.value,
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
            FilterTag.EXPRESSION_CUES.value,
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
            FilterTag.PARENTHESIS_NARR.value,
            FilterTag.BASIC_CHAR_OBJ.value,
            FilterTag.BASIC_NARR.value,
            FilterTag.NONE_CHAR_OBJ.value,
        ]
        self.start(
            args, {NullStrategy, ItalicStrategy,ItalicObjectStrategy,ExpressionCueTildaStrategy,ExpressionCueAsteriskStrategy}
        )