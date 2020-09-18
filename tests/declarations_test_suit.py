"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from tests.positive_test_cases import PositiveLanguageTests
from tests.negative_test_cases import NegativeLanguageTests
from tests.example_test_cases import PascalExamples
from tests.tdd_test_cases import TDD


class TestSuit:

    @classmethod
    def positive_tests_to_run(cls):
        return PositiveLanguageTests.available_tests()

    @classmethod
    def negative_tests_to_run(cls):
        return NegativeLanguageTests.available_tests()

    @classmethod
    def example_tests_to_run(cls):
        return PascalExamples.available_tests() + TDD.available_tests()

    @classmethod
    def tdd_tests_to_run(cls):
        return TDD.available_tests()

    @classmethod
    def available_positive_tests(cls):
        return PositiveLanguageTests.available_tests()

    @classmethod
    def available_negative_tests(cls):
        return NegativeLanguageTests.available_tests()

    @classmethod
    def available_example_tests(cls):
        return PascalExamples.available_tests() + TDD.available_tests()

    @classmethod
    def available_tdd_tests(cls):
        return TDD.available_tests()
