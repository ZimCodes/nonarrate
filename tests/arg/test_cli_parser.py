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
            FilterTag.TEXT_TAGS.value,
            FilterTag.QUOTED_CHARS.value,
            FilterTag.OBJ_CHARS.value,
        ]
        for option in options:
            with self.subTest(i=option):
                args[1] = option
                arg_namespace = fixture.get_args(self.parser, args)
                self.assertEqual(getattr(arg_namespace, option[2:].replace("-", "_")), ["t", "scan", "hem phk"])

    def test_no_args(self):
        args = ["game/", ""]
        options = [
            FilterTag.KEEP_PARENTHESIS.value,
            FilterTag.KEEP_COMMON_QUOTED_CHARS.value,
            FilterTag.KEEP_ITALIC.value,
            FilterTag.KEEP_COMMON_OBJ_CHARS.value,
            FilterTag.KEEP_NARRATION.value,
        ]
        for option in options:
            with self.subTest(i=option):
                args[1] = option
                arg_namespace = fixture.get_args(self.parser, args)
                self.assertNotIn(option, arg_namespace.narr_types)
