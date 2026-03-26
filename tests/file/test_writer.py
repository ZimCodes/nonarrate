import shutil
import pathlib
from lib.arg.cli_parser import CLIParser
import tests.fixture as fixture
import unittest
from lib.file import Writer


class TestWriter(unittest.TestCase):
    def setUp(self) -> None:
        self._parser = CLIParser()
        self.backup_folder = None

    def tearDown(self) -> None:
        if self.backup_folder and self.backup_folder.exists():
            shutil.rmtree(self.backup_folder, ignore_errors=True)

    def count_files(self, dir_path):
        total = 0
        for _ in dir_path.iterdir():
            total += 1
        return total

    def test_backup(self):
        backup_loc = pathlib.Path(f"{fixture.DUMMY_PATH}/_BACKUP")
        files_to_backup = [f"{fixture.DUMMY_PATH}/ex_reader.rpy"]
        writer = Writer()
        correct_total = len(files_to_backup)
        writer.backup_dir(files_to_backup, backup_loc)
        self.assertTrue(backup_loc.exists(), f"Backup folder doesn't exist at {backup_loc.absolute()}")
        self.backup_folder = backup_loc
        backup_total = self.count_files(backup_loc)
        self.assertEqual(
            backup_total,
            correct_total,
            "The contents of backup folder does not equal the total number of items in folder",
        )
