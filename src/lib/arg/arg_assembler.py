import re
from argparse import Namespace
from typing import final
from lib.validator.dialogue import ParenthesisStrategy, ItalicStrategy, BasicStrategy, CustomTextTagStrategy
from lib.validator.ivalidator_chain import IValidatorChain
from lib.validator.speaker import (
    ObjectNoneItemStrategy,
    ObjectStrategy,
    BasicCharacterStrategy,
    CharacterStrategy,
    BasicObjectStrategy,
)
from lib.custom_types import FilterTag


@final
class ArgAssembler:
    """Provides a class for converting parsed arguments into something more useful."""

    __validators: dict[str, type] = {
        FilterTag.NO_BASIC_NARR.value: BasicStrategy,
        FilterTag.NO_BASIC_CHAR_OBJ.value: BasicObjectStrategy,
        FilterTag.NO_ITALIC_NARR.value: ItalicStrategy,
        FilterTag.NO_PARENTHESIS_NARR.value: ParenthesisStrategy,
        FilterTag.NO_BASIC_CHAR.value: BasicCharacterStrategy,
        FilterTag.CUSTOM_TEXT_TAG.value: CustomTextTagStrategy,
        FilterTag.CUSTOM_CHAR.value: CharacterStrategy,
        FilterTag.CUSTOM_CHAR_OBJ.value: ObjectStrategy,
    }

    @classmethod
    def assemble(cls, args: Namespace):
        """Convert parsed arguments to useful types.

        Args:
            args: Namespace class containing parsed arguments.
        """
        cls.__convert_filters(args)

    @classmethod
    def __convert_filters(cls, args: Namespace):
        """Convert parsed argument for filters in validators.

        At the end, the results are placed in the arg.validator attribute.

        Args:
            args: Namespace class containing parsed arguments.
        """
        args.validator = ObjectNoneItemStrategy()
        current_validator = args.validator
        if args.narr_types:
            for narr_type in args.narr_types:
                current_validator.next_validator = cls.__validators[narr_type]()
                current_validator = current_validator.next_validator
        current_validator = cls.__narg_filter(
            current_validator, cls.__escape(args, args.custom_tag), FilterTag.CUSTOM_TEXT_TAG.value
        )
        current_validator = cls.__narg_filter(
            current_validator, cls.__escape(args, args.custom_char), FilterTag.CUSTOM_CHAR.value
        )
        current_validator = cls.__narg_filter(
            current_validator, cls.__escape(args, args.custom_char_obj), FilterTag.CUSTOM_CHAR_OBJ.value
        )

    @staticmethod
    def __escape(args, arg_filter_val: list[str] | None) -> str | list[str] | None:
        """Convert filter value into a literal expression if '--regex' is enabled."""
        if not arg_filter_val:
            return
        if not args.regex:
            for i in range(len(arg_filter_val)):
                arg_filter_val[i] = re.escape(arg_filter_val[i])
            return arg_filter_val
        else:
            return "|".join(arg_filter_val)

    @classmethod
    def __narg_filter(cls, validator, arg_filter: str | list[str] | None, filter_name: str):
        if not arg_filter:
            return validator
        if type(arg_filter) is str:
            # Regex is On
            validator.next_validator = cls.__validators[filter_name](arg_filter)
        else:
            # Regex is Off
            arg_filter_len = len(arg_filter)
            for i in range(arg_filter_len):
                validator.next_validator = cls.__validators[filter_name](arg_filter[i])
                if i < arg_filter_len - 1:
                    validator = validator.next_validator
        return validator.next_validator
