from unittest import TestCase
from deft_pascal_parser_3 import DeftPascalParser
from common_test_cases import CommonTestCases

_newline = "\n"
glb_input_filename = "in_add_line_numbers.txt"
glb_output_filename = "out_add_line_numbers.txt"
param_remove_file_after_test = True


def _run_parser(input_string):
    deft_pascal_parser = DeftPascalParser()
    ast = deft_pascal_parser.parse(input_string)
    return ast


class TestDeftPascalParser(TestCase):

    def test_program_definition_without_variables(self):
        test_code = CommonTestCases().scenario_program_definition_with_variables()
        self.assertIsNotNone(_run_parser(test_code))

    def test_program_definition_with_variables(self):
        test_code = CommonTestCases().scenario_program_definition_without_variables()
        self.assertIsNotNone(_run_parser(test_code))

    def test_label_declaration(self):
        test_code = CommonTestCases().scenario_label_declaration()
        self.assertIsNotNone(_run_parser(test_code))

    def test_decimal_numbers(self):
        test_code = CommonTestCases().scenario_decimal_numbers()
        self.assertIsNotNone(_run_parser(test_code))

    def test_binary_numbers(self):
        test_code = CommonTestCases().scenario_binary_numbers()
        self.assertIsNotNone(_run_parser(test_code))

    def test_octal_numbers(self):
        test_code = CommonTestCases().scenario_octal_numbers()
        self.assertIsNotNone(_run_parser(test_code))

    def test_hexadecimal_numbers(self):
        test_code = CommonTestCases().scenario_hexadecimal_numbers()
        self.assertIsNotNone(_run_parser(test_code))

    def test_strings(self):
        test_code = CommonTestCases().scenario_strings()
        self.assertIsNotNone(_run_parser(test_code))

    def test_booleans(self):
        test_code = CommonTestCases().scenario_booleans()
        self.assertIsNotNone(_run_parser(test_code))

    def test_constant_declaration(self):
        test_code = CommonTestCases().scenario_constant_declaration()
        self.assertIsNotNone(_run_parser(test_code))

    def test_variable_declaration(self):
        test_code = CommonTestCases().scenario_variable_declaration()
        self.assertIsNotNone(_run_parser(test_code))

    def test_scenario_variable_assignment_with_nil(self):
        test_code = CommonTestCases.scenario_variable_assignment_with_nil()
        self.assertIsNotNone(_run_parser(test_code))

    def test_variable_assignment_with_single_value(self):
        test_code = CommonTestCases().scenario_variable_assignment_with_single_value()
        self.assertIsNotNone(_run_parser(test_code))

    def test_variable_assignment_with_expression(self):
        test_code = CommonTestCases().scenario_variable_assignment_with_expression()
        self.assertIsNotNone(_run_parser(test_code))

    def test_variable_assignment_with_same_variable(self):
        test_code = CommonTestCases().scenario_variable_assignment_with_same_variable()
        self.assertIsNotNone(_run_parser(test_code))

    def test_repeat_loop_with_boolean(self):
        test_code = CommonTestCases().scenario_repeat_loop_with_boolean()
        self.assertIsNotNone(_run_parser(test_code))

    def test_repeat_loop_with_variable(self):
        test_code = CommonTestCases().scenario_repeat_loop_with_variable()
        self.assertIsNotNone(_run_parser(test_code))

    def test_repeat_loop_with_expression(self):
        test_code = CommonTestCases().scenario_repeat_loop_with_expression()
        self.assertIsNotNone(_run_parser(test_code))

    def xtest_program_definition_2(self):
        test_code = "program test;                        \n"\
                    " const                               \n"\
                    "   PI = 3.1415;                      \n"\
                    "                                     \n"\
                    " var                                 \n"\
                    "   a, b: real;                       \n"\
                    "   c : MEUTIPO;                      \n"\
                    " procedure hello(s: string; n: real);\n"\
                    " begin                               \n"\
                    "   writeln(s);                       \n"\
                    " end;                                \n"\
                    "                                     \n"\
                    " begin                               \n"\
                    "   a := PI;                          \n"\
                    "   b := a * 10;                      \n"\
                    "   hello('Hello World!', b);         \n"\
                    " end.                                \n"
        result = _run_parser(test_code)
        print(result)
        assert_yacc_equivalent(result, [1])

