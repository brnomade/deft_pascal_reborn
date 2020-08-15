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
from tests.common_test_cases import LanguageTests, TestSuit
import inspect
import logging

GLB_LOGGER = logging.getLogger(__name__)


class TestDeftPascalParser(TestCase):

    def setUp(self):
        available_tests = [i[0] for i in inspect.getmembers(LanguageTests, predicate=inspect.isfunction) if
                           'scenario_' in i[0]]
        selected_tests = [i[0] for i in TestSuit().parser_tests_to_run() if 'scenario_' in i[0]]
        if not set(available_tests).issubset(set(selected_tests)):
            msg = "\n\nNot all test scenarios are being run. Review TestSuit class.\n\nDifferences:\n{0}\n\n"
            GLB_LOGGER.warning(msg.format(set(available_tests)-set(selected_tests)))


    @parameterized.expand(LanguageTests.parser_tests_to_run())
    def test_positive(self, name, source_code):
        if "{{{0}}}" in source_code:
            source_code = source_code.replace("{{{0}}}", name)

        deft_pascal_parser = DeftPascalParser()
        error_list = deft_pascal_parser.parse(source_code)
        self.assertIsNone(error_list)
        GLB_LOGGER.debug(deft_pascal_parser.ast.pretty())


