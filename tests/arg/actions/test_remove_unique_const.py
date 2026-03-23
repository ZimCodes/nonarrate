import unittest
from lib.arg.cli_parser import CLIParser
import tests.fixture as fixture
from lib.custom_types import FilterTag


class TestRemoveUniqueConst(unittest.TestCase):
    def setUp(self):
        self.parser = CLIParser()

    def test_action(self):
        option = FilterTag.BASIC_NARR.value
        args = fixture.get_args(self.parser, f"game/ {option}")
        self.assertNotIn(option, args.narr_types)

    def test_multiple(self):
        options = [FilterTag.BASIC_NARR.value, FilterTag.ITALIC_NARR.value]
        args = fixture.get_args(self.parser, f"game/ {options[0]} {options[1]}")
        for i in range(len(options)):
            with self.subTest(name=options[i]):
                self.assertNotIn(options[i], args.narr_types)
        self.assertIn(FilterTag.BASIC_CHAR_OBJ.value, args.narr_types)
