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

GLB_LOGGER = getLogger(__name__)
GLB_LOGGER.level = DEBUG


class ConfigurationForTestDeftPascalCompiler:

    @classmethod
    def tests_to_run(cls):
        return TestSuit.tests_to_run()


class TestDeftPascalCompiler(TestCase):

    def setUp(self):
        available_tests = TestSuit.available_tests()
        selected_tests = ConfigurationForTestDeftPascalCompiler.tests_to_run()
        if not set(available_tests).issubset(set(selected_tests)):
            msg = "\n\nNot all test scenarios are being run. Review TestSuit class.\n\nDifferences:\n{0}\n\n"
            GLB_LOGGER.warning(msg.format(set(available_tests)-set(selected_tests)))


    @parameterized.expand(ConfigurationForTestDeftPascalCompiler.tests_to_run())
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

    def test_negative_scenario_any_syntax_error_raises_parser_error(self):
        source_code = NegativeLanguageTests.scenario_any_syntax_error_raises_parser_error()
        if "{{{0}}}" in source_code:
            source_code = source_code.replace("{{{0}}}", "scenario_any_syntax_error_raises_parser_error")
        #
        compiler = DeftPascalCompiler()
        error_log = compiler.check_syntax(source_code)
        if error_log:
            print(error_log)
        self.assertNotEqual([], error_log)

    def test_negative_compile_without_defined_ast(self):
        compiler = DeftPascalCompiler()
        self.assertRaises(ValueError, compiler.compile)

    def test_negative_get_ast_without_defined_ast(self):
        compiler = DeftPascalCompiler()
        with self.assertRaises(ValueError) as cm:
            compiler.ast()
        self.assertIsInstance(cm.exception, ValueError)

    def test_negative_scenario_incompatible_types_assignment(self):
        source_code = NegativeLanguageTests.scenario_incompatible_types_assignment_raises_compiler_error()
        if "{{{0}}}" in source_code:
            source_code = source_code.replace("{{{0}}}", "scenario_incompatible_types_in_expression")
        #
        compiler = DeftPascalCompiler()
        error_log = compiler.check_syntax(source_code)
        if error_log:
            print(error_log)
        self.assertEqual([], error_log)
        error_log = compiler.compile()
        if error_log:
            print(error_log)
        self.assertIn("incompatible types in expression", error_log[0])

    def test_negative_scenario_constant_identifier_already_declared(self):
        source_code = NegativeLanguageTests.scenario_constant_identifier_already_declared_raises_compiler_error()
        if "{{{0}}}" in source_code:
            source_code = source_code.replace("{{{0}}}", "scenario_constant_identifier_already_declared")
        #
        compiler = DeftPascalCompiler()
        error_log = compiler.check_syntax(source_code)
        if error_log:
            print(error_log)
        self.assertEqual([], error_log)
        error_log = compiler.compile()
        if error_log:
            print(error_log)
        self.assertIn("already declared", error_log[0])


    def test_negative_scenario_variable_identifier_already_declared(self):
        source_code = NegativeLanguageTests.scenario_variable_identifier_already_declared_raises_compiler_error()
        if "{{{0}}}" in source_code:
            source_code = source_code.replace("{{{0}}}", "scenario_variable_identifier_already_declared_raises_compiler_error")
        #
        compiler = DeftPascalCompiler()
        error_log = compiler.check_syntax(source_code)
        if error_log:
            print(error_log)
        self.assertEqual([], error_log)
        error_log = compiler.compile()
        if error_log:
            print(error_log)
        self.assertIn("already declared", error_log[0])

    def test_negative_scenario_assignment_to_undeclared_variable_identifier_raises_compiler_error(self):
        source_code = NegativeLanguageTests.scenario_assignment_to_undeclared_variable_identifier_raises_compiler_error()
        if "{{{0}}}" in source_code:
            source_code = source_code.replace("{{{0}}}", "scenario_assignment_to_undeclared_variable_identifier_raises_compiler_error")
        #
        compiler = DeftPascalCompiler()
        error_log = compiler.check_syntax(source_code)
        if error_log:
            print(error_log)
        self.assertEqual([], error_log)
        error_log = compiler.compile()
        if error_log:
            print(error_log)
        self.assertIn("Reference to undeclared", error_log[0])

    def test_negative_scenario_reference_to_undeclared_variable_identifier_raises_compiler_error(self):
        source_code = NegativeLanguageTests.scenario_reference_to_undeclared_variable_identifier_raises_compiler_error()
        if "{{{0}}}" in source_code:
            source_code = source_code.replace("{{{0}}}", "scenario_reference_to_undeclared_variable_identifier_raises_compiler_error")
        #
        compiler = DeftPascalCompiler()
        error_log = compiler.check_syntax(source_code)
        if error_log:
            print(error_log)
        self.assertEqual([], error_log)
        error_log = compiler.compile()
        if error_log:
            print(error_log)
        self.assertIn("Reference to undeclared", error_log[0])

    def test_negative_scenario_variable_identifier_declared_with_undeclared_type_raises_compiler_error(self):
        source_code = NegativeLanguageTests.scenario_variable_identifier_declared_with_undeclared_type_raises_compiler_error()
        if "{{{0}}}" in source_code:
            source_code = source_code.replace("{{{0}}}", "scenario_variable_identifier_declared_with_undeclared_type_raises_compiler_error")
        #
        compiler = DeftPascalCompiler()
        error_log = compiler.check_syntax(source_code)
        if error_log:
            print(error_log)
        self.assertEqual([], error_log)
        error_log = compiler.compile()
        if error_log:
            print(error_log)
        self.assertIn("unknown type", error_log[0])

    def test_negative_scenario_assignment_to_constant_raises_compiler_error(self):
        source_code = NegativeLanguageTests.scenario_assignment_to_constant_raises_compiler_error()
        if "{{{0}}}" in source_code:
            source_code = source_code.replace("{{{0}}}", "scenario_assignment_to_constant_raises_compiler_error")
        #
        compiler = DeftPascalCompiler()
        error_log = compiler.check_syntax(source_code)
        if error_log:
            print(error_log)
        self.assertEqual([], error_log)
        error_log = compiler.compile()
        if error_log:
            print(error_log)
        self.assertIn("Invalid assignment to constant", error_log[0])

    def test_negative_scenario_not_boolean_repeat_until_condition_raises_compiler_error(self):
        source_code = NegativeLanguageTests.scenario_not_boolean_repeat_until_condition_raises_compiler_error()
        if "{{{0}}}" in source_code:
            source_code = source_code.replace("{{{0}}}", "scenario_not_boolean_repeat_until_condition_raises_compiler_error")
        #
        compiler = DeftPascalCompiler()
        error_log = compiler.check_syntax(source_code)
        if error_log:
            print(error_log)
        self.assertEqual([], error_log)
        error_log = compiler.compile()
        if error_log:
            print(error_log)
        self.assertIn("expected boolean expression", error_log[0])

    def test_negative_scenario_not_boolean_while_do_condition_raises_compiler_error (self):
        source_code = NegativeLanguageTests.scenario_not_boolean_while_do_condition_raises_compiler_error()
        if "{{{0}}}" in source_code:
            source_code = source_code.replace("{{{0}}}", "scenario_not_boolean_while_do_condition_raises_compiler_error")
        #
        compiler = DeftPascalCompiler()
        error_log = compiler.check_syntax(source_code)
        if error_log:
            print(error_log)
        self.assertEqual([], error_log)
        error_log = compiler.compile()
        if error_log:
            print(error_log)
        self.assertIn("expected boolean expression", error_log[0])

    def test_negative_scenario_not_boolean_if_else_condition_raises_compiler_error(self):
        source_code = NegativeLanguageTests.scenario_not_boolean_if_else_condition_raises_compiler_error()
        if "{{{0}}}" in source_code:
            source_code = source_code.replace("{{{0}}}", "scenario_not_boolean_if_else_condition_raises_compiler_error")
        #
        compiler = DeftPascalCompiler()
        error_log = compiler.check_syntax(source_code)
        if error_log:
            print(error_log)
        self.assertEqual([], error_log)
        error_log = compiler.compile()
        if error_log:
            print(error_log)
        self.assertIn("expected boolean expression", error_log[0])

    def test_negative_scenario_reference_to_unknown_procedure_raises_compiler_error(self):
        source_code = NegativeLanguageTests.scenario_reference_to_unknown_procedure_raises_compiler_error()
        if "{{{0}}}" in source_code:
            source_code = source_code.replace("{{{0}}}", "scenario_reference_to_unknown_procedure_raises_compiler_error")
        #
        compiler = DeftPascalCompiler()
        error_log = compiler.check_syntax(source_code)
        if error_log:
            print(error_log)
        self.assertEqual([], error_log)
        error_log = compiler.compile()
        if error_log:
            print(error_log)
        self.assertIn("Unknown procedure", error_log[0])

    def test_negative_scenario_type_identifier_already_declared_raises_compiler_error(self):
        source_code = NegativeLanguageTests.scenario_type_identifier_already_declared_raises_compiler_error()
        if "{{{0}}}" in source_code:
            source_code = source_code.replace("{{{0}}}", "scenario_type_identifier_already_declared_raises_compiler_error")
        #
        compiler = DeftPascalCompiler()
        error_log = compiler.check_syntax(source_code)
        if error_log:
            print(error_log)
        self.assertEqual([], error_log)
        error_log = compiler.compile()
        if error_log:
            print(error_log)
        self.assertIn("already declared", error_log[0])

    def test_negative_scenario_reference_to_unknown_type_identifier_raises_compiler_error(self):
        source_code = NegativeLanguageTests.scenario_reference_to_unknown_type_identifier_raises_compiler_error()
        if "{{{0}}}" in source_code:
            source_code = source_code.replace("{{{0}}}", "scenario_reference_to_unknown_type_identifier_raises_compiler_error")
        #
        compiler = DeftPascalCompiler()
        error_log = compiler.check_syntax(source_code)
        if error_log:
            print(error_log)
        self.assertEqual([], error_log)
        error_log = compiler.compile()
        if error_log:
            print(error_log)
        self.assertIn("reference to unknown type", error_log[0])
