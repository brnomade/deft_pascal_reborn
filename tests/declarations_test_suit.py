"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

import logging

from tests.language_test_cases import PositiveLanguageTests
from tests.example_test_cases import PascalExamples
from tests.tdd_test_cases import TDD

GLB_LOGGER = logging.getLogger(__name__)


class TestSuit:

    @classmethod
    def tests_to_run(cls):
        return PascalExamples.available_tests() + TDD.available_tests() + PositiveLanguageTests.available_tests()

    @classmethod
    def available_tests(cls):
        return PascalExamples.available_tests() + TDD.available_tests() + PositiveLanguageTests.available_tests()
