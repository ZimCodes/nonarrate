import os
import pathlib
from lib.arg.cli_parser import CLIParser
from lib.file.backup import Backup
from lib.file.filter.backup_filter import BackupFilter
from lib.file.filter.renpy_filter import RenpyFilter
import tests.fixture as fixture
import unittest


class TestBackup(unittest.TestCase):
    def setUp(self) -> None:
        self._parser = CLIParser()
        self._path = fixture.get_dummy_path(self._parser)
        self.backup_folder = None

    def tearDown(self) -> None:
        if self.backup_folder and self.backup_folder.exists():
            os.remove(self.backup_folder)

    def test_backup(self):
        dummy_file = "ex_reader"
        backup_path = pathlib.Path(f"{self._path}/{dummy_file}{BackupFilter.FILE_EXT}")
        files_to_backup = [f"{self._path}/{dummy_file}{RenpyFilter.FILE_EXT}"]
        Backup.backup_files(files_to_backup)
        self.assertTrue(backup_path.exists(), f"Backup file doesn't exist at {backup_path.absolute()}")
        self.backup_folder = backup_path

    def test_restore(self):
        dummy_file = "ex_reader"
        original_file = pathlib.Path(f"{self._path}/{dummy_file}{RenpyFilter.FILE_EXT}")
        files_to_backup = [f"{self._path}/{dummy_file}{RenpyFilter.FILE_EXT}"]
        Backup.backup_files(files_to_backup)
        os.remove(original_file)
        Backup.restore_files([f"{self._path}/{dummy_file}{BackupFilter.FILE_EXT}"])
        self.assertTrue(original_file.exists(), f"Original file was not restored at {original_file.absolute()}")
        self.backup_folder = pathlib.Path(f"{self._path}/{dummy_file}{BackupFilter.FILE_EXT}")
