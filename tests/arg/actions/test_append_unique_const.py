# import unittest
# from lib.arg.cli_parser import CLIParser
# import tests.fixture as fixture

# NOTE: There are no options using this argparse action.
# When one uses this action, test it here!
#
# class TestAppendUniqueConst(unittest.TestCase):
#     def setUp(self):
#         self.parser = CLIParser()
#         self.option = '--basic-char'
#
#     def test_action(self):
#         args = fixture.get_args(self.parser,f'game/ { self.option }')
#         self.assertIn(self.option,args.narr_types)
#
#     def test_multiple_usage(self):
#         args = fixture.get_args(self.parser,f'game/ {self.option} {self.option}')
#         items = [ narr_type for narr_type in args.narr_types if narr_type == self.option ]
#         self.assertIn(self.option,args.narr_types)
#         self.assertEqual(len(items),1)
#
#     def test_none(self):
#         args = fixture.get_args(self.parser,'game/')
#         self.assertNotIn(self.option, args.narr_types)
