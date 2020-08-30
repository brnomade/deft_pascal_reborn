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
from tests.positive_test_cases import PositiveLanguageTests

GLB_LOGGER = getLogger(__name__)
GLB_LOGGER.level = DEBUG


class ConfigurationForTestDeftPascalCompiler:

    @classmethod
    def positive_tests_to_run(cls):
        # return [("scenario_variable_assignment_with_pointer", PositiveLanguageTests.scenario_variable_assignment_with_pointer)]
        return TestSuit.positive_tests_to_run()

    @classmethod
    def negative_tests_to_run(cls):
        #return [("scenario_incompatible_types_assignment_raises_compiler_error_basic_type_case", NegativeLanguageTests.scenario_incompatible_types_assignment_raises_compiler_error_basic_type_case)
        #        ]
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
        message = i[0]
        source_code = i[1]
        if "{{{0}}}" in source_code:
            source_code = source_code.replace("{{{0}}}", name)
        #
        compiler = DeftPascalCompiler()
        error_log = compiler.check_syntax(source_code)
        if error_log:
            print(error_log)
        self.assertEqual([], error_log)
        error_log = compiler.compile()
        if error_log:
            print(error_log)
        if message:
            self.assertIn(message, error_log[0])
        else:
            self.assertNotEqual([], error_log)


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

