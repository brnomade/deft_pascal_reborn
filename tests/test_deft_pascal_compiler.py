"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from logging import getLogger, DEBUG

from unittest import TestCase
from components.deft_pascal_compiler import DeftPascalCompiler
from parameterized import parameterized
from tests.declarations_test_suit import TestSuit
from tests.negative_test_cases import NegativeLanguageTests

GLB_LOGGER = getLogger(__name__)
GLB_LOGGER.level = DEBUG


class ConfigurationForTestDeftPascalCompiler:

    @classmethod
    def tests_to_run(cls):
        return TestSuit.tests_to_run()


class TestDeftPascalCompiler(TestCase):

    def setUp(self):
        available_tests = TestSuit.available_tests()
        selected_tests = ConfigurationForTestDeftPascalCompiler.tests_to_run()
        if not set(available_tests).issubset(set(selected_tests)):
            msg = "\n\nNot all test scenarios are being run. Review TestSuit class.\n\nDifferences:\n{0}\n\n"
            GLB_LOGGER.warning(msg.format(set(available_tests)-set(selected_tests)))


    @parameterized.expand(ConfigurationForTestDeftPascalCompiler.tests_to_run())
    def test_positive(self, name, function_callable):
        source_code = function_callable()
        if "{{{0}}}" in source_code:
            source_code = source_code.replace("{{{0}}}", name)
        #
        compiler = DeftPascalCompiler()
        error_log = compiler.check_syntax(source_code)
        if error_log:
            print(error_log)
        self.assertEqual([], error_log)
        #
        GLB_LOGGER.debug(compiler.ast.pretty())
        #
        error_log = compiler.compile()
        if error_log:
            print(error_log)
        self.assertEqual([], error_log)

    # def test_negative_scenario_syntax_error_detected_by_parser(self):
    #     source_code = NegativeLanguageTests.scenario_syntax_error_detected_by_parser()
    #     if "{{{0}}}" in source_code:
    #         source_code = source_code.replace("{{{0}}}", "scenario_syntax_error_detected_by_parser")
    #     #
    #     compiler = DeftPascalCompiler()
    #     error_log = compiler.check_syntax(source_code)
    #     if error_log:
    #         print(error_log)
    #     self.assertNotEqual([], error_log)

