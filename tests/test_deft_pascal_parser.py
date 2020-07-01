from unittest import TestCase
from deft_pascal_parser import DeftPascalParser
from ply.lex import LexToken

_newline = "\n"
glb_input_filename = "in_add_line_numbers.txt"
glb_output_filename = "out_add_line_numbers.txt"
param_remove_file_after_test = True


def _run_parser(input_string):
    deft_pascal_parser = DeftPascalParser()
    result = deft_pascal_parser.compile(input_string)
    return result


def assert_yacc_equivalent(stream_1, stream_2):
    if stream_1 is None or stream_2 is None:
        pass
    else:
        assert len(stream_1) == len(stream_2)
    #for token_1, token_2 in zip(stream_1, stream_2):
    #    assert token_1.type == token_2.type
    #    assert token_1.value == token_2.value


class TestDeftPascalParser(TestCase):

    def test_program_definition(self):
        test_code = "PROGRAM my_test_program;            \n"\
                    "CONST                               \n"\
                    "X = 1;                              \n"\
                    "X = 1.0;                            \n"\
                    "X = &HFF;                           \n"\
                    "X = &B10;                           \n"\
                    "X = &O12;                           \n"\
                    "X = 'C';                            \n"\
                    "X = 'CCCCCCCC';                     \n"\
                    "VAR a : INTEGER;                    \n"\
                    "    b : STRING;                     \n"\
                    "BEGIN                               \n"\
                    " a:=b + 1 * 2 / 3 MOD 4;            \n"\
                    " WRITE(a);                          \n"\
                    "END.                                \n"
        result = _run_parser(test_code)
        print(result)
        assert_yacc_equivalent(result, [1])

    def test_program_definition_2(self):
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

