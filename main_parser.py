from deft_pascal_parser_3 import DeftPascalParser


def _run_parser(input_string):
    deft_pascal_parser = DeftPascalParser()
    ast = deft_pascal_parser.parse(input_string)
    return ast


def test_code():
    source = "PROGRAM my_test_program( A1, A2, A3); \n" \
             "LABEL 100, 200, 300, 400;             \n" \
             "BEGIN                                 \n" \
             "END.                                  \n"
    return source


_run_parser(test_code())

