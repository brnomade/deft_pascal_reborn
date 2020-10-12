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
        return [(123,
                 "scenario_procedure_call_single_parameter_with_literal",
                 PositiveLanguageTests.scenario_procedure_call_single_parameter_with_literal)
                ]


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
                self._execute_negative_test(t[1], t[2]())
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


    def _execute_negative_test(self, name, inbound):
        print("Run negative test '{0}'".format(name))
        error_message = inbound[0]
        warning_message = inbound[1]
        source_code = inbound[2]
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


    def _execute_step_1_2(self, source_code):
        print("Run syntax check, semantic check and generating intermediate code")
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
        print("Run syntax check, semantic check, generating intermediate code, generating c code and compiling in gcc")
        compiler = DeftPascalCompiler()

        # test syntax check
        log = compiler.check_syntax(source_code)
        if log["ERROR"]:
            print(log["ERROR"])
        else:
            print(compiler.ast.pretty())
        self.assertEqual([], log["ERROR"])

        # test compilation
        try:
            log = compiler.compile()
        except:
            print("EXCEPTION RAISED")
            exit(1)

        if log["ERROR"]:
            print(log["ERROR"])
        print(compiler.intermediate_code)
        self.assertEqual([], log["ERROR"])

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


