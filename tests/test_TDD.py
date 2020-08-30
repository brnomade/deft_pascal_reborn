"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from unittest import TestCase
from components.deft_pascal_compiler import DeftPascalCompiler
from tests.negative_test_cases import NegativeLanguageTests
from tests.positive_test_cases import PositiveLanguageTests
from tests.example_test_cases import PascalExamples
from tests.tdd_test_cases import TDD


class ConfigurationForTestTDD:

    @classmethod
    def tdd_tests_to_run(cls):
        return [(TDD, "tdd_2", TDD.tdd_2)]


class TestTDD(TestCase):

    def test_run(self):
        for t in ConfigurationForTestTDD.tdd_tests_to_run():
            if t[0] == PositiveLanguageTests:
                print("running Positive Test")
                source_code = t[2]()
                if "{{{0}}}" in source_code:
                    source_code = source_code.replace("{{{0}}}", t[1])
                self._execute_positive_test(source_code)
            elif t[0] == NegativeLanguageTests:
                print("running Negative Test")
                i = t[2]()
                message = i[0]
                source_code = i[1]
                if "{{{0}}}" in source_code:
                    source_code = source_code.replace("{{{0}}}", t[1])
                self._execute_negative_test(message, source_code)
            elif t[0] == PascalExamples:
                print("running Example Test")
                source_code = t[2]()
                if "{{{0}}}" in source_code:
                    source_code = source_code.replace("{{{0}}}", t[1])
                self._execute_examples_test(source_code)
            elif t[0] == TDD:
                print("running TDD Test")
                source_code = t[2]()
                if "{{{0}}}" in source_code:
                    source_code = source_code.replace("{{{0}}}", t[1])
                self._execute_tdd_test(source_code)
            else:
                raise ModuleNotFoundError("Unknown Test Class")

    def _execute_positive_test(self, source_code):
        compiler = DeftPascalCompiler()
        error_log = compiler.check_syntax(source_code)
        if error_log:
            print(error_log)
        self.assertEqual([], error_log)
        #
        error_log = compiler.compile()
        if error_log:
            print(error_log)
        self.assertEqual([], error_log)


    def _execute_negative_test(self, message, source_code):
        compiler = DeftPascalCompiler()
        error_log = compiler.check_syntax(source_code)
        if error_log:
            print(error_log)
        self.assertEqual([], error_log)
        #
        error_log = compiler.compile()
        if error_log:
            print(error_log)
        if message:
            self.assertIn(message, error_log[0])
        else:
            self.assertNotEqual([], error_log)


    def _execute_examples_test(self, source_code):
        compiler = DeftPascalCompiler()
        error_log = compiler.check_syntax(source_code)
        if error_log:
            print(error_log)
        self.assertEqual([], error_log)
        #
        error_log = compiler.compile()
        if error_log:
            print(error_log)
        self.assertEqual([], error_log)


    def _execute_tdd_test(self, source_code):
        compiler = DeftPascalCompiler()
        error_log = compiler.check_syntax(source_code)
        if error_log:
            print(error_log)
        else:
            print(compiler.ast.pretty())
        self.assertEqual([], error_log)
        #
        error_log = compiler.compile()
        if error_log:
            print(error_log)
        else:
            print(compiler.intermediate_code)
        self.assertEqual([], error_log)
