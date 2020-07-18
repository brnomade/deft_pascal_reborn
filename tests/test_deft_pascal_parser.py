from unittest import TestCase
from deft_pascal_parser_3 import DeftPascalParser
from lark import Tree, Token, UnexpectedToken, UnexpectedCharacters

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
        test_code = "PROGRAM my_test_program;            \n"\
                    "BEGIN                               \n"\
                    "END.                                \n"
        self.assertIsNotNone(_run_parser(test_code))

    def test_program_definition_with_variables(self):
        test_code = "PROGRAM my_test_program( A1, A2, A3); \n"\
                    "BEGIN                                 \n"\
                    "END.                                  \n"
        self.assertIsNotNone(_run_parser(test_code))

    def test_label_declaration(self):
        test_code = "PROGRAM my_test_program( A1, A2, A3); \n" \
                    "LABEL 100, 200, 300, 400;             \n" \
                    "BEGIN                                 \n" \
                    "END.                                  \n"
        self.assertIsNotNone(_run_parser(test_code))

    def test_decimal_numbers(self):
        test_code = "PROGRAM my_test_program;              \n" \
                    "CONST                                 \n" \
                    "C1 = 0;                               \n" \
                    "C2 = +0;                              \n" \
                    "C3 = -1;                              \n" \
                    "C4 = +1;                              \n" \
                    "C5 = -0.5;                            \n" \
                    "C6 = +0.5;                            \n" \
                    "C7 = 0.5e1;                           \n" \
                    "C8 = 0.5E1;                           \n" \
                    "C9 = -0.5E+1;                         \n" \
                    "C10 = +0.5E-1;                        \n" \
                    "BEGIN                                 \n" \
                    "END.                                  \n"
        self.assertIsNotNone(_run_parser(test_code))

    def test_binary_numbers(self):
        test_code = "PROGRAM my_test_program;              \n" \
                    "CONST                                 \n" \
                    "C1 = &B00;                            \n" \
                    "C2 = &b11;                            \n" \
                    "C3 = &B101010101010;                  \n" \
                    "C4 = &b101010101010;                  \n" \
                    "BEGIN                                 \n" \
                    "END.                                  \n"
        self.assertIsNotNone(_run_parser(test_code))

    def test_octal_numbers(self):
        test_code = "PROGRAM my_test_program;              \n" \
                    "CONST                                 \n" \
                    "C1 = &O00;                            \n" \
                    "C2 = &o00;                            \n" \
                    "C3 = &O01234567;                      \n" \
                    "C4 = &O01234567;                      \n" \
                    "BEGIN                                 \n" \
                    "END.                                  \n"
        self.assertIsNotNone(_run_parser(test_code))

    def test_hexadecimal_numbers(self):
        test_code = "PROGRAM my_test_program;              \n" \
                    "CONST                                 \n" \
                    "C1 = &h00;                            \n" \
                    "C2 = &H00;                            \n" \
                    "C3 = &hABCDFE;                        \n" \
                    "C4 = &HABCDFE;                        \n" \
                    "C4 = &h0123456789;                    \n" \
                    "C5 = &H0123456789;                    \n" \
                    "C6 = &H0123456789ABCDEF;              \n" \
                    "C7 = &h0123456789ABCDEF;              \n" \
                    "BEGIN                                 \n" \
                    "END.                                  \n"
        self.assertIsNotNone(_run_parser(test_code))

    def test_strings(self):
        test_code = "PROGRAM my_test_program;              \n" \
                    "CONST                                 \n" \
                    "C7 = 'C';                             \n" \
                    "C8 = 'C8C8C8C8';                      \n" \
                    "BEGIN                                 \n" \
                    "END.                                  \n"
        self.assertIsNotNone(_run_parser(test_code))

    def test_booleans(self):
        test_code = "PROGRAM my_test_program;              \n" \
                    "CONST                                 \n" \
                    "C9 = True;                            \n" \
                    "C10 = False;                          \n" \
                    "C9 = TRUE;                            \n" \
                    "C10 = FALSE;                          \n" \
                    "C9 = true;                            \n" \
                    "C10 = false;                          \n" \
                    "C9 = TrUe;                            \n" \
                    "C10 = fAlSe;                          \n" \
                    "BEGIN                                 \n" \
                    "END.                                  \n"
        self.assertIsNotNone(_run_parser(test_code))

    def test_constant_declaration(self):
        test_code = "PROGRAM my_test_program;             \n" \
                    "CONST                                \n" \
                    "C = 2;                               \n" \
                    "C = -1;                              \n" \
                    "C = +1;                              \n" \
                    "C = 1.0;                             \n" \
                    "C = -1.0;                            \n" \
                    "C = +1.0;                            \n" \
                    "C = 1.0e-12;                         \n" \
                    "C = &HFF;                            \n" \
                    "C = &B10;                            \n" \
                    "C = &O12;                            \n" \
                    "C = 'C';                             \n" \
                    "C = 'C8C8C8C8';                      \n" \
                    "C = True;                            \n" \
                    "C = False;                           \n" \
                    "BEGIN                                \n" \
                    "END.                                 \n"
        self.assertIsNotNone(_run_parser(test_code))

    def test_variable_declaration(self):
        test_code = "PROGRAM my_test_program;              \n" \
                    "VAR V1, V2 : INTEGER;                 \n" \
                    "    _V3    : REAL;                    \n" \
                    "    _V3_b  : BOOLEAN;                 \n" \
                    "    _V3c   : BYTE;                    \n" \
                    "    _V3_b  : CHAR;                    \n" \
                    "    _V3c   : STRING;                  \n" \
                    "    _V3_b  : TEXT;                    \n" \
                    "    _V3c   : WORD;                    \n" \
                    "    _V3c   : SET;                     \n" \
                    "BEGIN                                 \n" \
                    "END.                                  \n"
        self.assertIsNotNone(_run_parser(test_code))

    def test_variable_assignment_with_single_value(self):
        test_code = "PROGRAM my_test_program;              \n" \
                    "BEGIN                                 \n" \
                    " V1 := 2;                             \n" \
                    " V2 := True;                          \n" \
                    " V3 := 'C';                           \n" \
                    " V4 := 'STRING';                      \n" \
                    " V5 := V4;                            \n" \
                    " V6 := -1;                            \n" \
                    " V7 := -1.0;                          \n" \
                    " V8 := &HFF;                          \n" \
                    " V9 := &B10;                          \n" \
                    " V10 := &O11;                         \n" \
                    " V11 := NIL;                          \n" \
                    " V12 := -1.1E-23;                     \n" \
                    "END.                                  \n"
        self.assertIsNotNone(_run_parser(test_code))

    def test_variable_assignment_with_expression(self):
        test_code = "PROGRAM my_test_program;                  \n" \
                    "BEGIN                                     \n" \
                    " V1 := 2 + V1 * 3 + (1 / 2);              \n" \
                    " V1 := -2 + V1 * 3.0 + (&HFF / -1.1E-23); \n" \
                    "END.                                      \n"
        self.assertIsNotNone(_run_parser(test_code))

    def test_variable_assignment_with_same_variable(self):
        test_code = "PROGRAM my_test_program;                  \n" \
                    "BEGIN                                     \n" \
                        " V1 := V1 + 1;                        \n" \
                    "END.                                      \n"
        self.assertIsNotNone(_run_parser(test_code))

    def test_repeat_loop_with_boolean(self):
        test_code = "PROGRAM my_test_program;                  \n" \
                    "BEGIN                                     \n" \
                    "   REPEAT                                 \n" \
                    "      V1 := 2 + V1 * 3 + (1 / 2);         \n" \
                    "   UNTIL True                             \n" \
                    "END.                                      \n"

    def test_repeat_loop_with_variable(self):
        test_code = "PROGRAM my_test_program;                  \n" \
                    "BEGIN                                     \n" \
                    "   REPEAT                                 \n" \
                    "      V1 := 2 + V1 * 3 + (1 / 2);         \n" \
                    "   UNTIL V2                               \n" \
                    "END.                                      \n"

    def test_repeat_loop_with_expression(self):
        test_code = "PROGRAM my_test_program;                  \n" \
                    "BEGIN                                     \n" \
                    "   REPEAT                                 \n" \
                    "      V1 := 2 + V1 * 3 + (1 / 2);         \n" \
                    "   UNTIL V2 + 1 > 2                       \n" \
                    "END.                                      \n"

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

