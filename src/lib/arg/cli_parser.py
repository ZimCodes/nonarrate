"""Provides a 'CLIParser' class for parsing arguments from the command line.

This module defines a class, 'CLIParser', which encapsulate methods and attributes for
extracting command line arguments from the command line interface.
"""

import argparse
import pathlib
import os
from typing import Any

from lib.arg.actions import *
from lib.custom_types import FilterTag


class CLIParser:
    """Represents a class for parsing arguments from the command line.

    CLIParser parses arguments from the command line and provides the results.
    """

    def __init__(self):
        self.__version_num = "2.2.2"
        self.__setup()

    def __setup(self):
        self.__init_parser()
        self.__init_parser_groups()
        self.__configure_opts()

    def __init_parser(self):
        self.__parser = argparse.ArgumentParser(
            prog="nonarrate",
            description="Remove narration & thoughts from Ren'Py visual novel games.",
        )

    def __init_parser_groups(self):
        self.__search_group = self.__parser.add_argument_group("File Search", "Limits the search for .rpy files.")
        self.__filter_group = self.__parser.add_argument_group("Filters", "Types of narration to remove.")

    def __configure_opts(self):
        self.__add_arg(
            "folder_or_file",
            metavar="Folder of *.rpy files OR errors.txt",
            type=pathlib.Path,
            help="Removes narration from .rpy files OR fix errors from errors.txt file",
        )
        self.__add_arg(
            "-p",
            "--pauses",
            action="store_true",
            help="Show removed narrated scenes by pausing.",
        )
        self.__add_arg(
            "-v",
            "--version",
            action="version",
            version="%(prog)s " + self.__version_num,
        )
        self.__add_arg(
            "-b",
            "--backup",
            metavar="BACKUP_DIR_PATH",
            type=pathlib.Path,
            help="Backup .rpy files to a specified location.",
        )
        self.__add_arg(
            "-e",
            "--regex",
            action="store_true",
            help="Enable regular expressions when specifying filter values.",
        )
        self.__add_arg(
            "-j",
            "--jobs",
            metavar="NUMBER_OF_WORKERS",
            type=int,
            default=min(32, (os.cpu_count() or 1) * 4),
            help="Maximum number of workers to use for I/O tasks.",
        )
        self.__add_search_arg(
            "--invalid-dirs",
            action=AppendUnique,
            default={
                "tl",
                "menu",
                "gui",
                "saves",
                "images",
                "cache",
                "fonts",
                "voices",
                "functions",
                "music",
                "audio",
                "gallery"
            },
            metavar="IGNORE_FOLDERS",
            help="Ignore specified [folders] when looking for .rpy files",
        )
        self.__add_search_arg(
            "--invalid-files",
            action=AppendUnique,
            default={"gui",
                     "options",
                     "screens",
                     "images",
                     "gallery",
                     "camera",
                     "credits",
                     "Credits",
                     "splashscreen",
                     "transitions",
                     "transforms",
                     "achievement"
                     "achievements"
                     },
            metavar="IGNORE_FILES",
            help="Ignore specified [files] when looking for .rpy files.",
        )
        self.__add_search_arg(
            "--invalid-globs",
            action=AppendUnique,
            metavar="IGNORE_FILE_GLOBS",
            help="Ignore specified [files] using glob syntax."
        )
        no_filters: dict[str, str] = {
            FilterTag.BASIC_NARR.value: "Keep dialogues that don't have a speaker",
            FilterTag.BASIC_CHAR_OBJ.value: "Keep [default narrators] that are saved to a Character object",
            FilterTag.ITALIC_NARR.value: "Keep fully italic dialogues",
            FilterTag.PARENTHESIS_NARR.value: "Keep dialogue fully wrapped in a parenthesis",
            FilterTag.BASIC_CHAR.value: "Keep [default narrators] not saved to a Character object",
            FilterTag.NONE_CHAR_OBJ.value: "Keep empty Character objects.",
            FilterTag.EXPRESSION_CUES.value: "Keep expression cues. Ex: *smiles*, ~raises eyebrows~.",
        }
        self.__add_no_filters(no_filters)
        self.__add_filter_arg(
            FilterTag.NO_CUSTOM_TEXT_TAGS.value,
            "--nct",
            metavar="TAG_NAMES",
            nargs="*",
            help="Removes dialogue wrapped entirely in a custom text tag. Ex:{t}..{/t}",
        )
        self.__add_filter_arg(
            FilterTag.NO_CUSTOM_CHARS.value,
            "--ncc",
            metavar="SPEAKER_NAMES",
            nargs="*",
            help="Removes speaker(s) surrounded by quotes.",
        )
        self.__add_filter_arg(
            FilterTag.NO_CUSTOM_CHAR_OBJS.value,
            "--ncco",
            metavar="SPEAKER_OBJECT_NAMES",
            nargs="*",
            help="Removes speaker(s) saved to a Character object",
        )

    def __add_no_filters(self, optnames: dict[str, str]):
        has_default = False
        initial_default = set(optnames)
        for optname, helpMsg in optnames.items():
            if not has_default:
                self.__add_filter_arg(
                    optname,
                    dest="narr_types",
                    action=RemoveUniqueConst,
                    const=optname,
                    default=initial_default,
                    help=helpMsg,
                )
                has_default = True
            else:
                self.__add_filter_arg(
                    optname,
                    dest="narr_types",
                    action=RemoveUniqueConst,
                    const=optname,
                    help=helpMsg,
                )

    def __add_arg(self, *args, **kwargs: Any):
        self.__parser.add_argument(*args, **kwargs)

    def __add_filter_arg(self, *args, **kwargs: Any):
        self.__filter_group.add_argument(*args, **kwargs)

    def __add_search_arg(self, *args, **kwargs: Any):
        self.__search_group.add_argument(*args, **kwargs)

    def parse_args(self, *args):
        """Parses a set of command arguments.

        Parses a list of commands. If *args isn't provided, user input from the
        command line is parsed instead.

        Args:
            *args: a collection of command arguments

        Returns:
            A Namespace object containing all parsed commands and their values.
        """
        return self.__parser.parse_args(*args)
