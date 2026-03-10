from lib.arg import CLIParser, ArgChecker, WrongFileError
import tests.fixture as fixture
import unittest


class TestArgChecker(unittest.TestCase):
    """The tests here rely on real files and folders"""

    def setUp(self):
        self.parser = CLIParser()

    def check_args(self, command: str):
        args = fixture.get_args(self.parser, command)
        ArgChecker.check_args(args)

    def test_folder_exists(self):
        self.assertIsNone(self.check_args(f"{fixture.DUMMY_PATH}/"))

    def test_folder_or_file_not_exists(self):
        for command in ["tests/jrajj/", f"{fixture.DUMMY_PATH}/file.txt"]:
            with self.subTest(name=command):
                with self.assertRaises(FileNotFoundError):
                    self.check_args(command)

    def test_valid_file(self):
        self.assertIsNone(self.check_args(f"{fixture.DUMMY_PATH}/errors.txt"))

    def test_invalid_file(self):
        """Tests against an actual file in dummy folder called real.txt"""
        with self.assertRaises(WrongFileError):
            self.check_args(f"{fixture.DUMMY_PATH}/real.txt")
