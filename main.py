from deft_pascal_parser_3 import DeftPascalParser
from deft_pascal_compiler import DeftPascalCompiler

glb_new_line_symbol = "\n"


def example_program_1():
    source = "PROGRAM Example;" \
             "TYPE SmallColor = Green..Blue;"\
             "VAR A:ARRAY[1..6] OF SmallColor;"\
             "VAR I,J : Integer;" \
             "  PROCEDURE Proc1;" \
             "  VAR I : Integer;" \
             "      PROCEDURE Proc2;" \
             "      VAR J : Integer;" \
             "      BEGIN    (* Proc2 BEGIN *)" \
             "        I:=J" \
             "      END;" \
             "  BEGIN (*Proc1 BEGIN*)" \
             "     Proc2;" \
             "     I:=J" \
             "  END;" \
             "BEGIN (* PROGRAM Example BEGIN*)" \
             "   Proc1;" \
             "I := J;" \
             "This.that();"\
             "END." \
             ""
    return source


def example_program_2():
    test_code = "PROGRAM my_test_program;            \n" \
                "CONST C1 = 2;                       \n" \
                "C2 = 1;                             \n" \
                "C3 = 1.0;                           \n" \
                "C4 = &HFF;                          \n" \
                "C5 = &B10;                          \n" \
                "C6 = &O12;                          \n" \
                "C7 = 'C';                           \n" \
                "C8 = 'C8C8C8C8';                    \n" \
                "C9 = True;                          \n" \
                "C10 = False;                        \n" \
                "VAR V1, V2 : INTEGER;               \n" \
                "    V3 : REAL;                      \n" \
                "    V4 : BOOLEAN;                   \n" \
                "    V5 : BYTE;                      \n" \
                "BEGIN BEGIN BEGIN BEGIN             \n" \
                " V1 := 1 >= 2;                      \n" \
                " V2 := (1 + 2)                      \n" \
                "END END END END.                    \n"
    return test_code





def example_program_4():
    test_code = "PROGRAM my_test_program( A1, A2, A3); \n" \
                "LABEL 100, 200, 300, 400;             \n" \
                "CONST C1 = -2;                        \n" \
                "C2 = +1;                              \n" \
                "C3 = 1.0;                             \n" \
                "C4 = &HFF;                            \n" \
                "C5 = &B10;                            \n" \
                "C6 = &O12;                            \n" \
                "C7 = 'C';                             \n" \
                "C8 = 'C8C8C8C8';                      \n" \
                "C9 = True;                            \n" \
                "C10 = False;                          \n" \
                "C11 = 1;                              \n" \
                "_C11 = 1;                             \n" \
                "VAR V1, V2 : INTEGER;                 \n" \
                "    V3 : REAL;                        \n" \
                "    V4 : BOOLEAN;                     \n" \
                "    V5 : BYTE;                        \n" \
                "    V6 : CHAR;                        \n" \
                "BEGIN                                 \n" \
                " V2 := 2 + V1 * (2 / 3);               \n" \
                " V4 := TRUE;                          \n" \
                " V1 := 1;                             \n" \
                " V6 := 'C';                           \n" \
                "END.                                  \n"
    return test_code


def main():
    compiler = DeftPascalCompiler()
    ast = compiler.check_syntax(example_program_4())
    if ast:
        print("Compilation result : \n {0}".format(ast.pretty()))
        compiler.compile(ast)
    else:
        print("Compilation failed!")


main()

