import re
from argparse import Namespace
from typing import final
from lib.validator import ObjectStrategy, IValidatorChain, IValidatorChainSolo, NullStrategy
from lib.file.filter import InvalidRenpyFilter, ValidRenpyFilter
from lib.custom_types import FilterTag
from lib.validator.rule import SpeakerRules, DialogueRules, QuoteRules, Rule


@final
class ArgAssembler:
    """Provides a class for converting parsed arguments into something more useful."""

    __narg_validators: dict[str, type[IValidatorChain]] = {
        FilterTag.NO_CUSTOM_TEXT_TAGS.value: IValidatorChainSolo,
        FilterTag.NO_CUSTOM_CHARS.value: IValidatorChainSolo,
        FilterTag.NO_CUSTOM_CHAR_VAR_OBJS.value: ObjectStrategy,
        FilterTag.NO_CUSTOM_CHAR_OBJS.value: ObjectStrategy,
    }
    __quote_validators: list[IValidatorChain] = [IValidatorChainSolo(QuoteRules.EXPRESSION_CUE_TILDA.value),
                                                 IValidatorChainSolo(QuoteRules.EXPRESSION_CUE_ASTERISK.value),
                                                 IValidatorChainSolo(QuoteRules.ITALIC.value),
                                                 IValidatorChainSolo(QuoteRules.ONLY_PUNCTUATION.value),
                                                 IValidatorChainSolo(QuoteRules.PARENTHESIS.value),
                                                 IValidatorChainSolo(QuoteRules.GUILLEMET_SINGLE.value),
                                                 IValidatorChainSolo(QuoteRules.GUILLEMET_DOUBLE.value)]

    @classmethod
    def assemble(cls, args: Namespace):
        """Convert parsed arguments to useful types.

        Args:
            args: Namespace class containing parsed arguments.
        """
        cls.__line_filters(args)
        cls.__quote_filters(args)
        cls.__file_filters(args)

    @classmethod
    def __line_filters(cls, args: Namespace):
        """Convert parsed argument for filters in validators.

        At the end, the results are placed in the arg.validator attribute.

        Args:
            args: Namespace class containing parsed arguments.
        """
        args.validator = NullStrategy()
        current_validator = args.validator
        if args.narr_types:
            for narr_type in args.narr_types:
                narr_filters = cls.__get_filters(narr_type)
                if type(narr_filters) == list:
                    for validator in narr_filters:
                        current_validator.next_validator = validator
                        current_validator = current_validator.next_validator
                else:
                    current_validator.next_validator = narr_filters
                    current_validator = current_validator.next_validator
        current_validator = cls.__narg_filter(
            current_validator, cls.__escape(args, args.no_custom_tags), FilterTag.NO_CUSTOM_TEXT_TAGS.value,
            DialogueRules.TEXT_TAG.value
        )
        current_validator = cls.__narg_filter(
            current_validator, cls.__escape(args, args.no_custom_chars), FilterTag.NO_CUSTOM_CHARS.value,
            SpeakerRules.CHARACTER.value
        )
        current_validator = cls.__narg_filter(
            current_validator, cls.__escape(args, args.no_custom_char_objs), FilterTag.NO_CUSTOM_CHAR_OBJS.value,
            SpeakerRules.OBJECT.value
        )
        current_validator = cls.__narg_filter(
            current_validator, cls.__escape(args, args.no_custom_char_var_objs),
            FilterTag.NO_CUSTOM_CHAR_VAR_OBJS.value, SpeakerRules.OBJECT_VAR.value
        )

    @staticmethod
    def __get_filters(option_name: str) -> list[IValidatorChain] | IValidatorChain:
        match option_name:
            case FilterTag.BASIC_CHAR_OBJ.value:
                return ObjectStrategy(SpeakerRules.OBJECT_BASIC.value)
            case FilterTag.ITALIC.value:
                return [IValidatorChainSolo(DialogueRules.ITALIC.value),
                        ObjectStrategy(SpeakerRules.OBJECT_ITALIC.value)]
            case FilterTag.PARENTHESIS.value:
                return IValidatorChainSolo(DialogueRules.PARENTHESIS.value)
            case FilterTag.BASIC_CHAR.value:
                return IValidatorChainSolo(SpeakerRules.CHARACTER_BASIC.value)
            case FilterTag.NONE_CHAR_OBJ.value:
                return ObjectStrategy(SpeakerRules.OBJECT_NONE.value)
            case FilterTag.EXPRESSION_CUES.value:
                return [IValidatorChainSolo(DialogueRules.EXPRESSION_CUE_TILDA.value),
                        IValidatorChainSolo(DialogueRules.EXPRESSION_CUE_ASTERISK.value)]
            case FilterTag.ONLY_PUNCTUATIONS.value:
                return IValidatorChainSolo(DialogueRules.ONLY_PUNCTUATION.value)
            case FilterTag.NONE_CHAR.value:
                return IValidatorChainSolo(SpeakerRules.CHARACTER_NONE.value)
            case FilterTag.GUILLEMETS.value:
                return [IValidatorChainSolo(DialogueRules.GUILLEMET_SINGLE.value),
                        IValidatorChainSolo(DialogueRules.GUILLEMET_DOUBLE.value)]
            case FilterTag.NVL.value:
                return ObjectStrategy(SpeakerRules.NVL_BASIC.value)
            case _:
                return IValidatorChainSolo(DialogueRules.BASIC.value)

    @staticmethod
    def __escape(args, arg_filter_val: list[str] | None) -> str | list[str] | None:
        """Convert filter value into a literal expression if '--regex' is enabled."""
        if not arg_filter_val:
            return arg_filter_val
        if not args.regex:
            for i in range(len(arg_filter_val)):
                arg_filter_val[i] = re.escape(arg_filter_val[i])
            return arg_filter_val
        else:
            return "|".join(arg_filter_val)

    @classmethod
    def __narg_filter(cls, validator, arg_filter: str | list[str] | None, filter_name: str, rule_type: type[Rule]):
        if not arg_filter:
            return validator
        if type(arg_filter) is str:
            # Regex is On
            rule = rule_type(arg_filter)
            validator.next_validator = cls.__narg_validators[filter_name](rule)
        else:
            # Regex is Off
            arg_filter_len = len(arg_filter)
            for i in range(arg_filter_len):
                rule = rule_type(arg_filter[i])
                validator.next_validator = cls.__narg_validators[filter_name](rule)
                if i < arg_filter_len - 1:
                    validator = validator.next_validator
        return validator.next_validator

    @classmethod
    def __quote_filters(cls, args: Namespace):
        current_validator: IValidatorChain | None = None
        for validator in cls.__quote_validators:
            if not current_validator:
                args.quote_validator = validator
                current_validator = args.quote_validator
            else:
                current_validator.next_validator = validator
                current_validator = current_validator.next_validator

        current_validator = cls.__quote_nargs(current_validator, cls.__escape(args, args.no_custom_tags),
                                              IValidatorChainSolo, QuoteRules.TEXT_TAG.value)

    @staticmethod
    def __quote_nargs(validator, arg_filter: str | list[str] | None, filter_type: type[IValidatorChain],
                      rule_type: type[Rule]):
        if not arg_filter:
            return validator
        if type(arg_filter) is str:
            # Regex is On
            rule = rule_type(arg_filter)
            validator.next_validator = filter_type(rule)
        else:
            # Regex is Off
            arg_filter_len = len(arg_filter)
            for i in range(arg_filter_len):
                rule = rule_type(arg_filter[i])
                validator.next_validator = filter_type(rule)
                if i < arg_filter_len - 1:
                    validator = validator.next_validator
        return validator.next_validator

    @staticmethod
    def __file_filters(args):
        """Convert parsed file filters into a FileFilter object.

        This has the side effect of placing the results in args.file_filter.

        Args:
            args: Namespace class containing parsed arguments.
        """
        if args.valid_dirs or args.valid_files or args.valid_globs:
            args.file_filter = ValidRenpyFilter(args.valid_dirs, args.valid_files, args.valid_globs)
        else:
            args.file_filter = InvalidRenpyFilter(args.invalid_dirs, args.invalid_files, args.invalid_globs)
