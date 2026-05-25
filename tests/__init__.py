import unittest
from tests.validator import *
from tests.arg.actions import *
from tests.arg import *
from tests.file import *
def load(test_case: type[unittest.TestCase]) -> unittest.TestSuite:
    return unittest.TestLoader().loadTestsFromTestCase(test_case)

def suite() -> unittest.TestSuite:
    test_suite = unittest.TestSuite()
    test_suite.addTests(load(TestArgAssembler))
    test_suite.addTests(load(TestCharacter))
    test_suite.addTests(load(TestCLIParser))
    test_suite.addTests(load(TestAppendUniqueLower))
    test_suite.addTests(load(TestDialogue))
    test_suite.addTests(load(TestRemoveUniqueConst))
    test_suite.addTests(load(TestQuote))
    test_suite.addTests(load(TestAppendUnique))
    test_suite.addTests(load(TestArgChecker))
    test_suite.addTests(load(TestWriter))
    test_suite.addTests(load(TestReader))
    test_suite.addTests(load(TestExecutor))
    return test_suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())