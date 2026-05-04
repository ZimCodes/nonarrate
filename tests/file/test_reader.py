import unittest
from lib.arg.arg_assembler import ArgAssembler
from lib.arg.cli_parser import CLIParser
from lib.file.reader import Reader
import tests.fixture as fixture


class TestReader(unittest.TestCase):
    def setUp(self) -> None:
        self._parser = CLIParser()
        self._reader = Reader()

    def _prepare_args(self, arg_opts: list[str]):
        args = fixture.get_args(self._parser, arg_opts)
        ArgAssembler.assemble(args)
        return args

    def test_all_files_valid(self):
        args = self._prepare_args([fixture.DUMMY_PATH])
        files = self._reader.walk_files(args.folder_or_file, args.file_filter)
        self.assertEqual(len(files), 2, "all .rpy files should not be seen by reader")

    def test_invalid_files(self):
        args = self._prepare_args([fixture.DUMMY_PATH, "--invalid-files", "ex_reader", "hello"])
        files = self._reader.walk_files(args.folder_or_file, args.file_filter)
        self.assertEqual(len(files), 0, "ex_reader.py and hello.rpy should not be seen by reader")

    def test_invalid_dirs(self):
        args = self._prepare_args([fixture.DUMMY_PATH, "--invalid-dirs", "child_dir"])
        files = self._reader.walk_files(args.folder_or_file, args.file_filter)
        self.assertEqual(len(files), 1, "hello.rpy should not be seen by reader")

    def test_invalid_file_globs(self):
        args = self._prepare_args([fixture.DUMMY_PATH, "--invalid-globs", "[hz]*"])
        files = self._reader.walk_files(args.folder_or_file, args.file_filter)
        self.assertEqual(len(files), 1, "Glob should not match any .rpy files!")
