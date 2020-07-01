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

def example_write():
    source = "WRITE(1); WRITELN(2);"

def main():
    deft_pascal_parser = DeftPascalParser()
    print("start ----")
    deft_pascal_parser.compile(example_program_1())
    print("start ----")
    deft_pascal_parser.compile(example_labels())


main()

