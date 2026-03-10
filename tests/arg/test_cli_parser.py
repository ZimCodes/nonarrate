import pathlib
import unittest
from lib.arg.cli_parser import CLIParser
import tests.fixture as fixture


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

    def test_custom_tag_arg(self):
        args = fixture.get_args(
            self.parser, ["game/", "--custom-tag", "t", "scan", "hem phk"]
        )
        self.assertEqual(args.custom_tag, ["t", "scan", "hem phk"])
