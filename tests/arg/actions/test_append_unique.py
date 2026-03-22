import unittest
from lib.arg.cli_parser import CLIParser
import tests.fixture as fixture


class TestAppendUnique(unittest.TestCase):
    def setUp(self) -> None:
        self._parser = CLIParser()

    def test_action(self):
        args = fixture.get_args(self._parser, ["game/", "--invalid-dirs", "backend", "waterfall"])
        self.assertIs(type(args.invalid_dirs), set)
        self.assertIn("backend", args.invalid_dirs)
        self.assertIn("waterfall", args.invalid_dirs)
        self.assertNotEqual(len(args.invalid_dirs), 2)

    def test_multiple(self):
        args = fixture.get_args(
            self._parser,
            ["game/", "--invalid-dirs", "backend", "waterfall", "--invalid-files", "gui", "anims", "images"],
        )
        self.assertIn("waterfall", args.invalid_dirs)
        self.assertIn("images", args.invalid_files)
        self.assertNotEqual(len(args.invalid_dirs), 2)
        self.assertNotEqual(len(args.invalid_files), 3)
