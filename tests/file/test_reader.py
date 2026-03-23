import unittest
from lib.arg.cli_parser import CLIParser
from lib.file import RenpyReader
import tests.fixture as fixture


class TestReader(unittest.TestCase):
    def setUp(self) -> None:
        self._parser = CLIParser()
        self._reader = RenpyReader()

    def test_invalid_files(self):
        args = fixture.get_args(self._parser, [fixture.DUMMY_PATH, "--invalid-files", "ex_reader", "hello"])
        files = self._reader.walk_files(args.folder_or_file, invalid_files=args.invalid_files)
        self.assertEqual(len(files), 0, "ex_reader.py and hello.rpy should not be seen by reader")

    def test_invalid_dirs(self):
        args = fixture.get_args(self._parser, [fixture.DUMMY_PATH, "--invalid-dirs", "child_dir"])
        files = self._reader.walk_files(args.folder_or_file, invalid_folders=args.invalid_dirs)
        self.assertEqual(len(files), 1, "hello.rpy should not be seen by reader")
