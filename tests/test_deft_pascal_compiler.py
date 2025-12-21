"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from logging import getLogger, DEBUG

from unittest import TestCase
from components.compiler.deft_pascal_compiler import DeftPascalCompiler
from parameterized import parameterized
from tests.declarations_test_suit import TestSuit
from tests.negative_test_cases import NegativeLanguageTests

GLB_LOGGER = getLogger(__name__)
GLB_LOGGER.level = DEBUG


class ConfigurationForTestDeftPascalCompiler:

    @classmethod
    def positive_tests_to_run(cls):
        return TestSuit.positive_tests_to_run()

    @classmethod
    def negative_tests_to_run(cls):
        return TestSuit.negative_tests_to_run()

    @classmethod
    def example_tests_to_run(cls):
        return TestSuit.example_tests_to_run()


class TestCompilerPositiveScenarios(TestCase):

    @classmethod
    def setUpClass(cls):
        available_tests = TestSuit.available_positive_tests()
        selected_tests = ConfigurationForTestDeftPascalCompiler.positive_tests_to_run()
        if not set(available_tests).issubset(set(selected_tests)):
            msg = "\n\nNot all positive test scenarios are being run. Review TestSuit class.\n\nDifferences:\n{0}\n\n"
            GLB_LOGGER.warning(msg.format(set(available_tests)-set(selected_tests)))


    @parameterized.expand(ConfigurationForTestDeftPascalCompiler.positive_tests_to_run())
    def test_positive(self, name, function_callable):
        source_code = function_callable()
        if "{{{0}}}" in source_code:
            source_code = source_code.replace("{{{0}}}", name)

        compiler = DeftPascalCompiler()
        log = compiler.check_syntax(source_code)
        if log["ERROR"]:
            print(log["ERROR"])
        self.assertEqual([], log["ERROR"])

        log = compiler.compile()
        if log["ERROR"]:
            print(log["ERROR"])
        self.assertEqual([], log["ERROR"])


class TestCompilerNegativeScenarios(TestCase):

    @classmethod
    def setUpClass(cls):
        available_tests = TestSuit.available_negative_tests()
        selected_tests = ConfigurationForTestDeftPascalCompiler.negative_tests_to_run()
        if not set(available_tests).issubset(set(selected_tests)):
            msg = "\n\nNot all negative test scenarios are being run. Review TestSuit class.\n\nDifferences:\n{0}\n\n"
            GLB_LOGGER.warning(msg.format(set(available_tests)-set(selected_tests)))


    @parameterized.expand(ConfigurationForTestDeftPascalCompiler.negative_tests_to_run())
    def test_negative(self, name, function_callable):
        i = function_callable()
        error_message = i[0]
        warning_message = i[1]
        source_code = i[2]
        if "{{{0}}}" in source_code:
            source_code = source_code.replace("{{{0}}}", name)

        compiler = DeftPascalCompiler()
        log = compiler.check_syntax(source_code)
        self.assertEqual([], log["ERROR"])

        log = compiler.compile()

        # if the compilation is expected to return an error message, the test confirms that.
        if error_message == "":
            self.assertEqual([], log["ERROR"])
        else:
            # log["ERROR"] is a list and could contain multiple messages. We are assuming the unit tests
            # are constructed to produce a single message and therefore the list will always be unary
            # if this is not the case than the unit test scenario needs to be revised.
            # self.assertEqual(1, len(log["ERROR"]))
            self.assertIn(error_message, log["ERROR"][0])

        # if the compilation is expected to return a warning message, the test confirms that.
        if warning_message == "":
            self.assertEqual([], log["WARNING"])
        else:
            # log["WARNING"] is a list and could contain multiple messages. We are assuming the unit tests
            # are constructed to produce a single message and therefore the list will always be unary
            # if this is not the case than the unit test scenario needs to be revised.
            # self.assertEqual(1, len(log["WARNING"]))
            self.assertIn(warning_message, log["WARNING"][0])


class TestCompilerExampleScenarios(TestCase):

    @classmethod
    def setUpClass(cls):
        available_tests = TestSuit.available_example_tests()
        selected_tests = ConfigurationForTestDeftPascalCompiler.example_tests_to_run()
        if not set(available_tests).issubset(set(selected_tests)):
            msg = "\n\nNot all example test scenarios are being run. Review TestSuit class.\n\nDifferences:\n{0}\n\n"
            GLB_LOGGER.warning(msg.format(set(available_tests)-set(selected_tests)))


    @parameterized.expand(ConfigurationForTestDeftPascalCompiler.example_tests_to_run())
    def test_examples(self, name, function_callable):
        source_code = function_callable()
        if "{{{0}}}" in source_code:
            source_code = source_code.replace("{{{0}}}", name)

        compiler = DeftPascalCompiler()
        log = compiler.check_syntax(source_code)
        if log["ERROR"]:
            print(log["ERROR"])
        self.assertEqual([], log["ERROR"])

        log = compiler.compile()
        if log["ERROR"]:
            print(log["ERROR"])
        self.assertEqual([], log["ERROR"])


class TestParser(TestCase):

    def test_parser_syntax_error_raises_parser_error_unexpected_token(self):
        source_code = NegativeLanguageTests.syntax_error_raises_parser_error_unexpected_token()
        if "{{{0}}}" in source_code:
            source_code = source_code.replace("{{{0}}}", "syntax_error_raises_parser_error_unexpected_token")
        #
        compiler = DeftPascalCompiler()
        error_log = compiler.check_syntax(source_code)
        if error_log:
            print(error_log)
        self.assertNotEqual([], error_log)

    def test_parser_syntax_error_raises_parser_error_unexpected_character(self):
        source_code = NegativeLanguageTests.syntax_error_raises_parser_error_unexpected_characters()
        if "{{{0}}}" in source_code:
            source_code = source_code.replace("{{{0}}}", "syntax_error_raises_parser_error_unexpected_characters")
        #
        compiler = DeftPascalCompiler()
        error_log = compiler.check_syntax(source_code)
        if error_log:
            print(error_log)
        self.assertNotEqual([], error_log)


class TestCompiler(TestCase):

    def test_compiler_compile_without_defined_ast(self):
        compiler = DeftPascalCompiler()
        self.assertRaises(ValueError, compiler.compile)

    def test_compiler_get_ast_without_defined_ast(self):
        compiler = DeftPascalCompiler()
        with self.assertRaises(ValueError) as cm:
            compiler.ast()
        self.assertIsInstance(cm.exception, ValueError)

