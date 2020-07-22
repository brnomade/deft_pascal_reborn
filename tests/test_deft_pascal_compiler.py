from unittest import TestCase
from deft_pascal_compiler import DeftPascalCompiler
from parameterized import parameterized
from common_test_cases import LanguageTests, TestSuit
import inspect
import logging

logger = logging.getLogger(__name__)


class TestDeftPascalCompiler(TestCase):

    def setUp(self):
        available_tests = [i[0] for i in inspect.getmembers(LanguageTests, predicate=inspect.isfunction) if
                           'scenario_' in i[0]]
        selected_tests = [i[0] for i in TestSuit().compiler_tests_to_run() if 'scenario_' in i[0]]
        if not set(available_tests).issubset(set(selected_tests)):
            msg = "\n\nWARNING!\nNot all test scenarios are being run. Review TestSuit class.\n\nDifferences:\n{0}\n\n\n"
            logger.warning(msg.format(set(available_tests)-set(selected_tests)))
            # print("\n\nWARNING!\nNot all test scenarios are being run. Review TestSuit class\n\n")


    @parameterized.expand(LanguageTests.compiler_tests_to_run())
    def test(self, name, source_code):
        compiler = DeftPascalCompiler()
        #
        ast = compiler.check_syntax(source_code)
        self.assertIsNotNone(ast)
        #
        error_log = compiler.compile(ast)
        self.assertEqual(error_log, [])



