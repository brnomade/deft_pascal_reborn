"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from unittest import TestCase
from components.parsers.deft_pascal_parser_3 import DeftPascalParser
from parameterized import parameterized
from tests.declarations_test_suit import TestSuit
from tests.negative_test_cases import NegativeLanguageTests


class ConfigurationForTestDeftPascalParser:

    @classmethod
    def tests_to_run(cls):
        return TestSuit.positive_tests_to_run() + TestSuit.example_tests_to_run()

    @classmethod
    def example_tests_to_run(cls):
        return TestSuit.example_tests_to_run()


class TestDeftPascalParser(TestCase):

    def setUp(self):
        available_tests = TestSuit.available_positive_tests()
        selected_tests = ConfigurationForTestDeftPascalParser.tests_to_run()
        if not set(available_tests).issubset(set(selected_tests)):
            msg = "\n\nNot all test scenarios are being run. Review TestSuit class.\n\nDifferences:\n{0}\n\n"
            print(msg.format(set(available_tests)-set(selected_tests)))

    @parameterized.expand(ConfigurationForTestDeftPascalParser.tests_to_run())
    def test_positive(self, name, function_callable):
        source_code = function_callable()
        if "{{{0}}}" in source_code:
            source_code = source_code.replace("{{{0}}}", name)
        #
        parser = DeftPascalParser()
        error_log = parser.parse(source_code)
        if error_log:
            print(error_log)
        self.assertEqual([], error_log)
        print(parser.ast.pretty())

    def test_parser_syntax_error_raises_parser_error_unexpected_token(self):
        source_code = NegativeLanguageTests.syntax_error_raises_parser_error_unexpected_token()
        if "{{{0}}}" in source_code:
            source_code = source_code.replace("{{{0}}}", "syntax_error_raises_parser_error_unexpected_token")
        #
        parser = DeftPascalParser()
        error_log = parser.parse(source_code)
        if error_log:
            print(error_log)
        self.assertNotEqual([], error_log)

    def test_parser_syntax_error_raises_parser_error_unexpected_character(self):
        source_code = NegativeLanguageTests.syntax_error_raises_parser_error_unexpected_characters()
        if "{{{0}}}" in source_code:
            source_code = source_code.replace("{{{0}}}", "syntax_error_raises_parser_error_unexpected_characters")
        #
        parser = DeftPascalParser()
        error_log = parser.parse(source_code)
        if error_log:
            print(error_log)
        self.assertNotEqual([], error_log)

    def test_negative_ast_not_defined_raises_exception(self):
        deft_pascal_parser = DeftPascalParser()
        with self.assertRaises(ValueError) as cm:
            deft_pascal_parser.ast()
        self.assertIsInstance(cm.exception, ValueError)
