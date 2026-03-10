import unittest
import os

from lib.file import FileExecutor, RenpyReader, Writer
from .. import fixture


class TestExecutor(unittest.TestCase):
    def test_reader(self):
        reader = RenpyReader()
        file_infos = FileExecutor.file_lines(reader, fixture.DUMMY_PATH)
        self.assertEqual(len(file_infos), 1, "Total renpy files detected!")

    def test_writer(self):
        writer = Writer()
        file_loc = f"{fixture.DUMMY_PATH}/ex_writer.rpy"
        file_info = {
            file_loc: [
                "Have you ever heard of a spoon?\n",
                "It is like THE best invention ever!",
            ]
        }
        FileExecutor.write_files(writer, file_info)
        self.assertTrue(os.path.exists(file_loc), "Checks if writer file exists")
        lines = []
        with open(file_loc, "r", encoding="utf-8") as f:
            lines = f.readlines()
        self.assertGreater(len(lines), 1, "Checks if writer file has content")
        self.addCleanup(os.remove, file_loc)
