"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from unittest import TestCase
from components.deft_pascal_compiler import DeftPascalCompiler
from utils.compiler_utils import compile_in_gcc
from tests.negative_test_cases import NegativeLanguageTests
from tests.positive_test_cases import PositiveLanguageTests
from tests.example_test_cases import PascalExamples
from tests.tdd_test_cases import TDD
import os


class ConfigurationForTestTDD:

    @classmethod
    def tdd_tests_to_run(cls):
        return [(123, "scenario_procedure_declaration_without_parameters_without_directive_nested", PositiveLanguageTests.scenario_procedure_declaration_without_parameters_without_directive_nested)]


class TestTDD(TestCase):

    def test_run(self):
        for t in ConfigurationForTestTDD.tdd_tests_to_run():
            print("\nTesting: '{0}'".format(t[1]))
            if t[0] == 1:
                source_code = t[2]()
                if "{{{0}}}" in source_code:
                    source_code = source_code.replace("{{{0}}}", t[1])
                self._execute_step_1(source_code)
            elif t[0] == -1:
                i = t[2]()
                message = i[0]
                source_code = i[1]
                if "{{{0}}}" in source_code:
                    source_code = source_code.replace("{{{0}}}", t[1])
                self._execute_negative_test(message, source_code)
            elif t[0] == 12:
                source_code = t[2]()
                if "{{{0}}}" in source_code:
                    source_code = source_code.replace("{{{0}}}", t[1])
                self._execute_step_1_2(source_code)
            elif t[0] == 123:
                source_code = t[2]()
                if "{{{0}}}" in source_code:
                    source_code = source_code.replace("{{{0}}}", t[1])
                self._execute_step_1_2_3(source_code)
            else:
                raise ModuleNotFoundError("Unknown Test Class")


    def _execute_step_1(self, source_code):
        print("Running syntax and semantic check")
        compiler = DeftPascalCompiler()
        error_log = compiler.check_syntax(source_code)
        if error_log:
            print(error_log)
        self.assertEqual([], error_log)
        print(compiler.ast.pretty())
        #
        error_log = compiler.compile()
        if error_log:
            print(error_log)
        self.assertEqual([], error_log)


    def _execute_negative_test(self, message, source_code):
        print("Running negative test cases")
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

    def _execute_step_1_2(self, source_code):
        print("Running syntax check, semantic check and generating intermediate code")
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
        print(compiler.intermediate_code)

    def _execute_step_1_2_3(self, source_code):
        print("Running syntax check, semantic check, generating intermediate code, generating c code and compiling in gcc")
        compiler = DeftPascalCompiler()

        # test syntax check
        error_log = compiler.check_syntax(source_code)
        if error_log:
            print(error_log)
        else:
            print(compiler.ast.pretty())
        self.assertEqual([], error_log)

        # test compilation
        try:
            error_log = compiler.compile()
        except:
            error_log = "EXCEPTION RAISED"

        if error_log:
            print(error_log)
        print(compiler.intermediate_code)
        self.assertEqual([], error_log)

        # test code generation
        output_code = compiler.generate()
        home_dir = os.getcwd()
        filepath = os.path.join(home_dir, "output", "sources")

        if not os.path.isdir(filepath):
            filepath = home_dir
        filename = os.path.join(filepath, "{0}.c".format("test_tdd"))

        if output_code:
            print(output_code)
            print(filename)
            file = open(filename, "w")
            file.write(output_code)
            file.close()
        #
        output = compile_in_gcc(filename, False)
        self.assertNotIn("error", output)
        self.assertNotIn("warning", output)


