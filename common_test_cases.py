
class TestSuit:

    @staticmethod
    def parser_tests_to_run():
        return TestSuit.tests_to_run()

    @staticmethod
    def compiler_tests_to_run():
        return [
    ["scenario_variable_assignment_with_single_value", LanguageTests().scenario_variable_assignment_with_single_value()],
    ["scenario_for_to_loop_with_constants", LanguageTests.scenario_for_to_loop_with_constants()],
                ]

    @staticmethod
    def tests_to_run():
        return [
    ["tdd_1", TDD().tdd_1()],
    ["tdd_2", TDD().tdd_2()],
    ["scenario_program_definition_with_variables", LanguageTests().scenario_program_definition_with_variables()],
    ["scenario_program_definition_without_variables", LanguageTests().scenario_program_definition_without_variables()],
    ["scenario_label_declaration", LanguageTests().scenario_label_declaration()],
    ["scenario_decimal_numbers", LanguageTests().scenario_decimal_numbers()],
    ["scenario_binary_numbers", LanguageTests().scenario_binary_numbers()],
    ["scenario_octal_numbers", LanguageTests().scenario_octal_numbers()],
    ["scenario_hexadecimal_numbers", LanguageTests().scenario_hexadecimal_numbers()],
    ["scenario_strings", LanguageTests().scenario_strings()],
    ["scenario_booleans", LanguageTests().scenario_booleans()],
    ["scenario_constant_declaration", LanguageTests().scenario_constant_declaration()],
    ["scenario_variable_declaration", LanguageTests().scenario_variable_declaration()],
    ["scenario_variable_assignment_with_nil", LanguageTests.scenario_variable_assignment_with_nil()],
    ["scenario_variable_assignment_with_single_value", LanguageTests().scenario_variable_assignment_with_single_value()],
    ["scenario_variable_assignment_with_expression", LanguageTests().scenario_variable_assignment_with_expression()],
    ["scenario_variable_assignment_with_same_variable", LanguageTests().scenario_variable_assignment_with_same_variable()],
    ["scenario_repeat_loop_with_boolean", LanguageTests().scenario_repeat_loop_with_boolean()],
    ["scenario_repeat_loop_with_variable", LanguageTests().scenario_repeat_loop_with_variable()],
    ["scenario_repeat_loop_with_expression", LanguageTests().scenario_repeat_loop_with_expression()],
    ["scenario_for_to_loop_with_constants", LanguageTests.scenario_for_to_loop_with_constants()],
    ["scenario_for_to_loop_with_expressions", LanguageTests.scenario_for_to_loop_with_expressions()],
                ]

#    ["scenario_for_downto_loop", LanguageTests.scenario_for_downto_loop()],
#    ["scenario_for_to_loop_with_begin_end", LanguageTests.scenario_for_to_loop_with_begin_end()],
#    ["scenario_for_downto_loop_with_begin_end", LanguageTests.scenario_for_downto_loop_with_begin_end()],


class LanguageTests(TestSuit):

    @staticmethod
    def scenario_program_definition_without_variables():
        code = \
            "PROGRAM my_scenario_program;        \n" \
            "BEGIN                               \n" \
            "END.                                \n"
        return code

    @staticmethod
    def scenario_program_definition_with_variables():
        code = \
            "PROGRAM my_scenario_program( A1, A2, A3); \n" \
            "BEGIN                                     \n" \
            "END.                                      \n"
        return code


    @staticmethod
    def scenario_label_declaration():
        code = \
            "PROGRAM my_scenario_program( A1, A2, A3); \n" \
            "LABEL 100, 200, 300, 400;             \n" \
            "BEGIN                                 \n" \
            "END.                                  \n"
        return code


    @staticmethod
    def scenario_decimal_numbers():
        code = \
            "PROGRAM my_scenario_program;              \n" \
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
        return code


    @staticmethod
    def scenario_binary_numbers():
        code = \
            "PROGRAM my_scenario_program;              \n" \
            "CONST                                 \n" \
            "C1 = &B00;                            \n" \
            "C2 = &b11;                            \n" \
            "C3 = &B101010101010;                  \n" \
            "C4 = &b101010101010;                  \n" \
            "BEGIN                                 \n" \
            "END.                                  \n"
        return code


    @staticmethod
    def scenario_octal_numbers():
        code = \
            "PROGRAM my_scenario_program;              \n" \
            "CONST                                 \n" \
            "C1 = &O00;                            \n" \
            "C2 = &o00;                            \n" \
            "C3 = &O01234567;                      \n" \
            "C4 = &O01234567;                      \n" \
            "BEGIN                                 \n" \
            "END.                                  \n"
        return code


    @staticmethod
    def scenario_hexadecimal_numbers():
        code = \
            "PROGRAM my_scenario_program;              \n" \
            "CONST                                 \n" \
            "C1 = &h00;                            \n" \
            "C2 = &H00;                            \n" \
            "C3 = &hABCDFE;                        \n" \
            "C4 = &HABCDFE;                        \n" \
            "C5 = &h0123456789;                    \n" \
            "C6 = &H0123456789;                    \n" \
            "C7 = &H0123456789ABCDEF;              \n" \
            "C8 = &h0123456789ABCDEF;              \n" \
            "BEGIN                                 \n" \
            "END.                                  \n"
        return code


    @staticmethod
    def scenario_strings():
        code = \
            "PROGRAM my_scenario_program;              \n" \
            "CONST                                 \n" \
            "C7 = 'C';                             \n" \
            "C8 = 'C8C8C8C8';                      \n" \
            "BEGIN                                 \n" \
            "END.                                  \n"
        return code


    @staticmethod
    def scenario_booleans():
        code = \
            "PROGRAM my_scenario_program;              \n" \
            "CONST                                 \n" \
            "C1 = True;                            \n" \
            "C2 = False;                          \n" \
            "C3 = TRUE;                            \n" \
            "C4 = FALSE;                          \n" \
            "C5 = true;                            \n" \
            "C6 = false;                          \n" \
            "C7 = TrUe;                            \n" \
            "C8 = fAlSe;                          \n" \
            "BEGIN                                 \n" \
            "END.                                  \n"
        return code


    @staticmethod
    def scenario_constant_declaration():
        code = \
            "PROGRAM my_scenario_program;             \n" \
            "CONST                                \n" \
            "C1 = 2;                               \n" \
            "C1a = -1;                              \n" \
            "C1b = +1;                              \n" \
            "C2 = 1.0;                             \n" \
            "C2a = -1.0;                            \n" \
            "C2b = +1.0;                            \n" \
            "C3 = 1.0e-12;                         \n" \
            "C3a = -1.0e+12;                         \n" \
            "C3b = 1.0e12;                         \n" \
            "C4 = &HFF;                            \n" \
            "C4a = &B10;                            \n" \
            "C4b = &O12;                            \n" \
            "C5 = 'C';                             \n" \
            "C6 = 'C8C8C8C8';                      \n" \
            "C7 = True;                            \n" \
            "C8 = False;                           \n" \
            "C9 = Nil;                           \n" \
            "BEGIN                                \n" \
            "END.                                 \n"
        return code


    @staticmethod
    def scenario_variable_declaration():
        code = \
            "PROGRAM my_scenario_program;              \n" \
            "VAR V1, V2 : INTEGER;                 \n" \
            "    _V3    : REAL;                    \n" \
            "    _V3_b  : BOOLEAN;                 \n" \
            "    _V3c   : BYTE;                    \n" \
            "    _V3_d  : CHAR;                    \n" \
            "    _V3_e   : STRING;                  \n" \
            "    _V3_f  : TEXT;                    \n" \
            "    _V3g   : WORD;                    \n" \
            "    _V3h   : SET;                     \n" \
            "BEGIN                                 \n" \
            "END.                                  \n"
        return code


    @staticmethod
    def scenario_variable_assignment_with_nil():
        code = \
            "PROGRAM my_scenario_program;              \n" \
            "VAR                                       \n" \
            "V1 : INTEGER;                             \n" \
            "BEGIN                                     \n" \
            "V1 := NIL                                 \n" \
            "END.                                      \n"
        return code


    @staticmethod
    def scenario_variable_assignment_with_single_value():
        code = \
            "PROGRAM my_scenario_program;              \n" \
            "VAR                                 \n" \
            " V1 : INTEGER;                             \n" \
            " V2 : BOOLEAN;                          \n" \
            " V3 : CHAR;                           \n" \
            " V4 : STRING;                      \n" \
            " V5 : STRING;                      \n" \
            " V6 : INTEGER;                            \n" \
            " V7 : REAL;                          \n" \
            " V8 : BYTE;                          \n" \
            " V9 : BYTE;                          \n" \
            " V10 : BYTE;                         \n" \
            " V11 : WORD;                          \n" \
            " V12 : REAL;                     \n" \
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
        return code


    @staticmethod
    def scenario_variable_assignment_with_expression():
        code = \
            "PROGRAM my_scenario_program;                  \n" \
            "VAR V1 : INTEGER;                         \n" \
            "    V2 : REAL;                         \n" \
            "BEGIN                                     \n" \
            " V1 := 2 + V1 * 3 + (&HFF / 2);              \n" \
            " V2 := -2.0 + V2 * 3.0 + (1.0 / -1.1E-23); \n" \
            "END.                                      \n"
        return code


    @staticmethod
    def scenario_variable_assignment_with_same_variable():
        code = \
            "PROGRAM my_scenario_program;                  \n" \
            "VAR V1 : INTEGER;                         \n" \
            "BEGIN                                     \n" \
            " V1 := V1 + 1;                        \n" \
            "END.                                      \n"
        return code


    @staticmethod
    def scenario_repeat_loop_with_boolean():
        code = \
            "PROGRAM my_scenario_program;              \n" \
            "VAR V1 : INTEGER;                         \n" \
            "BEGIN                                     \n" \
            "   REPEAT                                 \n" \
            "      V1 := 2 + V1 * 3 + (1 / 2);         \n" \
            "   UNTIL True                             \n" \
            "END.                                      \n"
        return code


    @staticmethod
    def scenario_repeat_loop_with_variable():
        code = \
            "PROGRAM my_scenario_program;                  \n" \
            "VAR V1 : INTEGER;                         \n" \
            "    V2 : REAL;                         \n" \
            "BEGIN                                     \n" \
            "   REPEAT                                 \n" \
            "      V1 := 2 + V1 * 3 + (1 / 2);         \n" \
            "   UNTIL V2;                               \n" \
            "END.                                      \n"
        return code


    @staticmethod
    def scenario_repeat_loop_with_expression():
        code = \
            "PROGRAM my_scenario_program;                  \n" \
            "VAR V1 : INTEGER;                         \n" \
            "    V2 : INTEGER;                         \n" \
            "BEGIN                                     \n" \
            "   REPEAT                                 \n" \
            "      V1 := 2 + V1 * 3 + (1 / 2);         \n" \
            "   UNTIL V2 + 1 > 2                       \n" \
            "END.                                      \n"
        return code

    @staticmethod
    def scenario_for_to_loop_with_constants():
        code = \
            "PROGRAM my_scenario_program;              \n" \
            "VAR X : INTEGER;                          \n" \
            "BEGIN                                     \n" \
            "   FOR X := 1 TO 10 DO                    \n" \
            "      V1 := X;                            \n" \
            "END.                                      \n"
        return code

    @staticmethod
    def scenario_for_to_loop_with_expressions():
        code = \
            "PROGRAM my_scenario_program;                \n" \
            "VAR V1 : INTEGER;                           \n" \
            "BEGIN                                       \n" \
            "   FOR X := (1 + 2 * 3) TO (10 + 1 * 2) DO  \n" \
            "      V1 := X;                              \n" \
            "END.                                        \n"
        return code


    @staticmethod
    def scenario_for_downto_loop():
        code = \
            "PROGRAM my_scenario_program;              \n" \
            "VAR V1 : INTEGER;                         \n" \
            "BEGIN                                     \n" \
            "   FOR X := 10 DOWNTO 1 DO                \n" \
            "      V1 := X;                            \n" \
            "END.                                      \n"
        return code

    @staticmethod
    def scenario_for_to_loop_with_begin_end():
        code = \
            "PROGRAM my_scenario_program;              \n" \
            "VAR V1 : INTEGER;                         \n" \
            "BEGIN                                     \n" \
            "   FOR X := 1 TO 10 DO                    \n" \
            "      BEGIN                               \n" \
            "         V1 := X;                         \n" \
            "      END;                                \n" \
            "END.                                      \n"
        return code

    @staticmethod
    def scenario_for_downto_loop_with_begin_end():
        code = \
            "PROGRAM my_scenario_program;              \n" \
            "VAR V1 : INTEGER;                         \n" \
            "BEGIN                                     \n" \
            "   FOR X := 10 DOWNTO 1 DO                \n" \
            "      BEGIN                               \n" \
            "         V1 := X;                         \n" \
            "      END;                                \n" \
            "END.                                      \n"
        return code

class TDD(TestSuit):

    @staticmethod
    def tdd_1():
        code = \
            "PROGRAM my_scenario_program;              \n" \
            "VAR                                   \n" \
            "V1 : INTEGER;                         \n" \
            "BEGIN                                 \n" \
            "V1 := NIL                                 \n" \
            "END.                                  \n"
        return code

    @staticmethod
    def tdd_2():
        code = \
            "PROGRAM my_test_program( A1, A2, A3); \n" \
            "LABEL 100, 200, 300, 400;             \n" \
            "CONST                                 \n" \
            "C1 = 0.5;  B = 1;                             \n" \
            "VAR V1, V3 : INTEGER;                     \n" \
            "V2 : BOOLEAN;                         \n" \
            "BEGIN                                 \n" \
            "   REPEAT                             \n" \
            "     V1 := V1 + 1                   \n" \
            "   UNTIL V1 + V3 > 10 + 1      \n" \
            "END.                                  \n"
        return code

    @staticmethod
    def scenario_program_definition_2():
        code = \
            "program test;                        \n"\
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
        return code

