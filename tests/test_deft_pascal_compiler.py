from unittest import TestCase
from deft_pascal_compiler import DeftPascalCompiler
from common_test_cases import CommonTestCases


def _run_syntax_check(source_code):
    compiler = DeftPascalCompiler()
    ast = compiler.check_syntax(source_code)
    return ast


def _run_compiler(ast):
    compiler = DeftPascalCompiler()
    log = compiler.compile(ast)
    return log


class TestDeftPascalCompiler(TestCase):

    def run_test(self, source_code):
        ast = _run_syntax_check(source_code)
        self.assertIsNotNone(ast)
        error_log = _run_compiler(ast)
        self.assertEqual(error_log, [])

    def test_scenario_program_definition_with_variables(self):
        test_code = CommonTestCases().scenario_program_definition_with_variables()
        self.run_test(test_code)

    def test_scenario_program_definition_without_variables(self):
        test_code = CommonTestCases().scenario_program_definition_without_variables()
        self.run_test(test_code)

    def test_scenario_label_declaration( self ):
        test_code = CommonTestCases().scenario_label_declaration()
        self.run_test(test_code)

    def test_scenario_booleans(self):
        test_code = CommonTestCases().scenario_booleans()
        self.run_test(test_code)

    def test_scenario_strings(self):
        test_code = CommonTestCases().scenario_strings()
        self.run_test(test_code)

    def test_scenario_decimal_numbers(self):
        test_code = CommonTestCases().scenario_decimal_numbers()
        self.run_test(test_code)

    def test_scenario_hexadecimal_numbers(self):
        test_code = CommonTestCases().scenario_hexadecimal_numbers()
        self.run_test(test_code)

    def test_scenario_binary_numbers(self):
        test_code = CommonTestCases().scenario_binary_numbers()
        self.run_test(test_code)

    def test_scenario_octal_numbers(self):
        test_code = CommonTestCases().scenario_octal_numbers()
        self.run_test(test_code)

    def test_scenario_constant_declaration(self):
        test_code = CommonTestCases().scenario_constant_declaration()
        self.run_test(test_code)

    def test_scenario_variable_declaration(self):
        test_code = CommonTestCases().scenario_variable_declaration()
        self.run_test(test_code)

    def test_scenario_variable_assignment_with_nil(self):
        test_code = CommonTestCases.scenario_variable_assignment_with_nil()
        self.run_test(test_code)

    def test_scenario_variable_assignment_with_expression(self):
        test_code = CommonTestCases().scenario_variable_assignment_with_expression()
        self.run_test(test_code)

    def test_scenario_variable_assignment_with_same_variable(self):
        test_code = CommonTestCases().scenario_variable_assignment_with_same_variable()
        self.run_test(test_code)

    def test_scenario_variable_assignment_with_single_value(self):
        test_code = CommonTestCases().scenario_variable_assignment_with_single_value()
        self.run_test(test_code)

    def test_scenario_repeat_loop_with_boolean(self):
        test_code = CommonTestCases().scenario_repeat_loop_with_boolean()
        self.run_test(test_code)

    def test_scenario_repeat_loop_with_expression(self):
        test_code = CommonTestCases().scenario_repeat_loop_with_expression()
        self.run_test(test_code)

    def test_scenario_repeat_loop_with_variable(self):
        test_code = CommonTestCases().scenario_repeat_loop_with_variable()
        self.run_test(test_code)

