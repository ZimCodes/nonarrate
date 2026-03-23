import pathlib
import unittest
from lib.arg.cli_parser import CLIParser
import tests.fixture as fixture
from lib.custom_types import FilterTag


class TestCLIParser(unittest.TestCase):
    def setUp(self):
        self.parser = CLIParser()

    def test_positional(self):
        positional = fixture.get_args(self.parser, "game/")
        self.assertEqual(
            positional.folder_or_file,
            pathlib.Path("game/"),
            msg="Failed accepting a folder",
        )
        positional = fixture.get_args(self.parser, "errors.txt")
        self.assertEqual(
            positional.folder_or_file,
            pathlib.Path("errors.txt"),
            msg="Failed accepting errors.txt file",
        )

    def test_narg_args(self):
        """Test options with variable arguments."""
        args = ["game/", "", "t", "scan", "hem phk"]
        options = [
            FilterTag.NO_CUSTOM_TEXT_TAGS.value,
            FilterTag.NO_CUSTOM_CHARS.value,
            FilterTag.NO_CUSTOM_CHAR_OBJS.value,
        ]
        for option in options:
            with self.subTest(i=option):
                args[1] = option
                arg_namespace = fixture.get_args(self.parser, args)
                self.assertEqual(getattr(arg_namespace, option[2:].replace("-", "_")), ["t", "scan", "hem phk"])

    def test_no_args(self):
        args = ["game/", ""]
        options = [
            FilterTag.PARENTHESIS_NARR.value,
            FilterTag.BASIC_CHAR.value,
            FilterTag.ITALIC_NARR.value,
            FilterTag.BASIC_CHAR_OBJ.value,
            FilterTag.BASIC_NARR.value,
        ]
        for option in options:
            with self.subTest(i=option):
                args[1] = option
                arg_namespace = fixture.get_args(self.parser, args)
                self.assertNotIn(option, arg_namespace.narr_types)
