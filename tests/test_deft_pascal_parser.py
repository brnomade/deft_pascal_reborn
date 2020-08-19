"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
VERSION.......: 0.1
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from unittest import TestCase
from components.deft_pascal_parser_3 import DeftPascalParser
from parameterized import parameterized
from tests.declarations_test_suit import TestSuit

# from tests.language_test_cases import PositiveLanguageTests


class ConfigurationForTestDeftPascalParser:

    @classmethod
    def tests_to_run(cls):
        return TestSuit.tests_to_run()


class TestDeftPascalParser(TestCase):

    def setUp(self):
        available_tests = TestSuit.available_tests()
        selected_tests = ConfigurationForTestDeftPascalParser.tests_to_run()
        if not set(available_tests).issubset(set(selected_tests)):
            msg = "\n\nNot all test scenarios are being run. Review TestSuit class.\n\nDifferences:\n{0}\n\n"
            GLB_LOGGER.warning(msg.format(set(available_tests)-set(selected_tests)))

    @parameterized.expand(ConfigurationForTestDeftPascalParser.tests_to_run())
    def test_positive(self, name, function_callable):
        source_code = function_callable()
        if "{{{0}}}" in source_code:
            source_code = source_code.replace("{{{0}}}", name)

        deft_pascal_parser = DeftPascalParser()
        error_list = deft_pascal_parser.parse(source_code)
        self.assertIsNone(error_list)
        print(deft_pascal_parser.ast.pretty())

    def test_extra_ast(self):
        deft_pascal_parser = DeftPascalParser()
        with self.assertRaises(ValueError) as cm:
            deft_pascal_parser.ast()
        self.assertIsInstance(cm.exception, ValueError)
