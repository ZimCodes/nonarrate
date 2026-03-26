import unittest
import os

from lib.arg.cli_parser import CLIParser
from lib.custom_types import FileInfo
from lib.file import FileExecutor, RenpyReader, Writer
from .. import fixture


class TestExecutor(unittest.TestCase):
    def test_reader(self):
        parser = CLIParser()
        reader = RenpyReader()
        args = fixture.get_args(parser, fixture.DUMMY_PATH)
        file_infos = FileExecutor.file_lines(reader, args)
        self.assertEqual(len(file_infos), 2, "Total renpy files detected!")

    def test_writer(self):
        writer = Writer()
        file_loc = f"{fixture.DUMMY_PATH}/ex_writer.rpy"
        file_infos = [
            FileInfo(
                file_loc,
                [
                    "Have you ever heard of a spoon?\n",
                    "It is like THE best invention ever!",
                ],
            )
        ]
        FileExecutor.write_files(writer, file_infos)
        self.assertTrue(os.path.exists(file_loc), "Checks if writer file exists")
        lines = []
        with open(file_loc, "r", encoding="utf-8") as f:
            lines = f.readlines()
        self.assertGreater(len(lines), 1, "Checks if writer file has content")
        self.addCleanup(os.remove, file_loc)
