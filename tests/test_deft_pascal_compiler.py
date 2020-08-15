"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
VERSION.......: 0.1
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from unittest import TestCase
from components.deft_pascal_compiler import DeftPascalCompiler
from parameterized import parameterized
from tests.common_test_cases import LanguageTests, TestSuit
import inspect
from logging import getLogger

GLB_LOGGER = getLogger(__name__)


class TestDeftPascalCompiler(TestCase):

    def setUp(self):
        available_tests = [i[0] for i in inspect.getmembers(LanguageTests, predicate=inspect.isfunction) if
                           'scenario_' in i[0]]
        selected_tests = [i[0] for i in TestSuit().compiler_tests_to_run() if 'scenario_' in i[0]]
        if not set(available_tests).issubset(set(selected_tests)):
            msg = "\n\nNot all test scenarios are being run. Review TestSuit class.\n\nDifferences:\n{0}\n\n"
            GLB_LOGGER.warning(msg.format(set(available_tests)-set(selected_tests)))


    @parameterized.expand(LanguageTests.compiler_tests_to_run())
    def test_positive(self, name, source_code):
        compiler = DeftPascalCompiler()
        #
        if "{{{0}}}" in source_code:
            source_code = source_code.replace("{{{0}}}", name)
        #
        error_log = compiler.check_syntax(source_code)
        if error_log:
            GLB_LOGGER.debug(error_log)
        self.assertIsNone(error_log)
        #
        GLB_LOGGER.debug(compiler.ast.pretty())
        #
        error_log = compiler.compile()
        if error_log:
            GLB_LOGGER.debug(error_log)
        self.assertIsNone(error_log)
