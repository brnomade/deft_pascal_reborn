from deft_pascal_parser import DeftPascalParser

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


def example_labels():
    source = "100: I" + glb_new_line_symbol + \
                    "LABEL 100; 1 := 1 + 1"
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

def example_program_3():
    test_code = "PROGRAM my_test_program; \n" \
                "BEGIN END.               \n"
    return test_code

def example_write():
    source = "WRITE(1); WRITELN(2);"


def main():
    deft_pascal_parser = DeftPascalParser()
    #print("start ----")
    #deft_pascal_parser.compile(example_program_1())
    #print("start ----")
    #deft_pascal_parser.compile(example_labels())
    result = deft_pascal_parser.compile(example_program_2())
    print("Compilation result : \n {0}".format(result))

main()

