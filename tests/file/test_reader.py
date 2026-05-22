import unittest
from lib.arg.arg_assembler import ArgAssembler
from lib.arg.cli_parser import CLIParser
from lib.file.reader import Reader
import tests.fixture as fixture


class TestReader(unittest.TestCase):
    def setUp(self) -> None:
        self._parser = CLIParser()
        self._path = fixture.get_dummy_path(self._parser)
        self._reader = Reader()

    def _prepare_args(self, arg_opts: list[str]):
        args = fixture.get_args(self._parser, arg_opts)
        ArgAssembler.assemble(args)
        return args

    def test_all_files_valid(self):
        args = self._prepare_args([self._path])
        files = self._reader.walk_files(args.folder_or_file, args.file_filter)
        self.assertEqual(len(files), 3, "all .rpy files should be seen by reader")

    def test_invalid_files(self):
        args = self._prepare_args([self._path, "--invalid-files", "oracle","ex_reader", "hello"])
        files = self._reader.walk_files(args.folder_or_file, args.file_filter)
        self.assertEqual(len(files), 0, "ex_reader.py, oracle.rpy and hello.rpy should not be seen by reader")

    def test_invalid_dirs(self):
        args = self._prepare_args([self._path, "--invalid-dirs", "child_dir"])
        files = self._reader.walk_files(args.folder_or_file, args.file_filter)
        self.assertEqual(len(files), 1, "hello.rpy should not be seen by reader")

    def test_invalid_file_globs(self):
        args = self._prepare_args([self._path, "--invalid-globs", "[hz]*"])
        files = self._reader.walk_files(args.folder_or_file, args.file_filter)
        self.assertEqual(len(files), 2, "Glob should not match any .rpy files starting with h or z!")

    def test_valid_files(self):
        args = self._prepare_args([self._path, "--valid-files", "ex_reader"])
        files = self._reader.walk_files(args.folder_or_file, args.file_filter)
        self.assertEqual(len(files), 1, "ex_reader.rpy should be the only valid file")

    def test_valid_dirs(self):
        args = self._prepare_args([self._path, "--valid-dirs", "child_dir"])
        files = self._reader.walk_files(args.folder_or_file, args.file_filter)
        self.assertEqual(len(files), 2, "child_dir is the only valid folder to look for rpy files.")

    def test_valid_file_globs(self):
        args = self._prepare_args([self._path, "--valid-globs", "o*"])
        files = self._reader.walk_files(args.folder_or_file, args.file_filter)
        self.assertEqual(len(files), 1, "Glob should match any .rpy files starting with o!")