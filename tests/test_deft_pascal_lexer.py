from unittest import TestCase
from obsoletes.deft_pascal_lexer import DeftPascalLexer
from ply.lex import LexToken

_newline = "\n"
glb_input_filename = "in_add_line_numbers.txt"
glb_output_filename = "out_add_line_numbers.txt"
param_remove_file_after_test = True


def _run_lexer(input_string):
    deft_pascal_lexer = DeftPascalLexer()
    deft_pascal_lexer.set_input(input_string)
    result = []
    while True:
        t = deft_pascal_lexer.get_token()
        if not t:
            break  # No more input
        else:
            result.append(t)
    return result


def _token(a_type, value):
    t = LexToken()
    if a_type is None:
        t.type = value
    else:
        t.type = a_type
    t.value = value
    t.lineno = -1
    t.lexpos = -1
    return t


def assert_lex_equivalent(stream_1, stream_2):
    assert len(stream_1) == len(stream_2)
    for token_1, token_2 in zip(stream_1, stream_2):
        assert token_1.type == token_2.type
        assert token_1.value == token_2.value


class TestDeftPascalLexer(TestCase):

    def test_program_declaration(self):
        test_code = "PROGRAM my_test_program \n BEGIN \n \n END."
        result = _run_lexer(test_code)
        print(result)
        assert_lex_equivalent(result, [
            _token('RESERVED_STRUCTURE_PROGRAM', 'PROGRAM'),
            _token('IDENTIFIER', 'my_test_program'),
            _token('RESERVED_STRUCTURE_BEGIN', 'BEGIN'),
            _token('RESERVED_STRUCTURE_END', 'END'),
            _token('DOT', '.'),
        ])

    def test_assignment_set(self):
        test_code = "BriteColors := [Yellow, Red] \n NoColors := []"
        result = _run_lexer(test_code)
        print(result)
        assert_lex_equivalent(result, [
            _token('IDENTIFIER', 'BriteColors'),
            _token('OPERATOR_ASSIGNMENT', ':='),
            _token('LEFT_SQUARE_BRACKET', '['),
            _token('IDENTIFIER', 'Yellow'),
            _token('COMMA', ','),
            _token('IDENTIFIER', 'Red'),
            _token('RIGHT_SQUARE_BRACKET', ']'),
            _token('IDENTIFIER', 'NoColors'),
            _token('OPERATOR_ASSIGNMENT', ':='),
            _token('LEFT_SQUARE_BRACKET', '['),
            _token('RIGHT_SQUARE_BRACKET', ']')
        ])

    def test_type_declaration_record(self):
        test_code = "TYPE Employee = RECORD\nName : String(20) \n Street,City : String(20); \n State : String(2)" \
                    "ZipCode : String(5); \n Number: Integer; \n Female: Boolean; \n END"
        result = _run_lexer(test_code)
        print(result)
        assert_lex_equivalent(result, [
            _token('RESERVED_DECLARATION_TYPE', 'TYPE'),
            _token('IDENTIFIER', 'Employee'),
            _token('OPERATOR_EQUAL_TO', '='),
            _token('RESERVED_RECORD', 'RECORD'),
            _token('IDENTIFIER', 'Name'),
            _token('COLON', ':'),
            _token('RESERVED_TYPE_STRING', 'String'),
            _token('LEFT_PARENTHESES', '('),
            _token('NUMBER_DECIMAL', '20'),
            _token('RIGHT_PARENTHESES', ')'),
            _token('IDENTIFIER', 'Street'),
            _token('COMMA', ','),
            _token('IDENTIFIER', 'City'),
            _token('COLON', ':'),
            _token('RESERVED_TYPE_STRING', 'String'),
            _token('LEFT_PARENTHESES', '('),
            _token('NUMBER_DECIMAL', '20'),
            _token('RIGHT_PARENTHESES', ')'),
            _token('SEMICOLON', ';'),
            _token('IDENTIFIER', 'State'),
            _token('COLON', ':'),
            _token('RESERVED_TYPE_STRING', 'String'),
            _token('LEFT_PARENTHESES', '('),
            _token('NUMBER_DECIMAL', '2'),
            _token('RIGHT_PARENTHESES', ')'),
            _token('IDENTIFIER', 'ZipCode'),
            _token('COLON', ':'),
            _token('RESERVED_TYPE_STRING', 'String'),
            _token('LEFT_PARENTHESES', '('),
            _token('NUMBER_DECIMAL', '5'),
            _token('RIGHT_PARENTHESES', ')'),
            _token('SEMICOLON', ';'),
            _token('IDENTIFIER', 'Number'),
            _token('COLON', ':'),
            _token('RESERVED_TYPE_INTEGER', 'Integer'),
            _token('SEMICOLON', ';'),
            _token('IDENTIFIER', 'Female'),
            _token('COLON', ':'),
            _token('RESERVED_TYPE_BOOLEAN', 'Boolean'),
            _token('SEMICOLON', ';'),
            _token('RESERVED_STRUCTURE_END', 'END')
        ])

    def test_type_declaration_array_multi_dimension(self):
        test_code = "TYPE ColorPlane = ARRAY[0..200] OF ARRAY[1..6] OF Color \n" \
                    "ColorPlane_2 = ARRAY[0..200, 1..6] OF Color"
        result = _run_lexer(test_code)
        print(result)
        assert_lex_equivalent(result, [
            _token('RESERVED_DECLARATION_TYPE', 'TYPE'),
            _token('IDENTIFIER', 'ColorPlane'),
            _token('OPERATOR_EQUAL_TO', '='),
            _token('RESERVED_TYPE_ARRAY', 'ARRAY'),
            _token('LEFT_SQUARE_BRACKET', '['),
            _token('NUMBER_DECIMAL', '0'),
            _token('RANGE', '..'),
            _token('NUMBER_DECIMAL', '200'),
            _token('RIGHT_SQUARE_BRACKET', ']'),
            _token('RESERVED_STATEMENT_OF', 'OF'),
            _token('RESERVED_TYPE_ARRAY', 'ARRAY'),
            _token('LEFT_SQUARE_BRACKET', '['),
            _token('NUMBER_DECIMAL', '1'),
            _token('RANGE', '..'),
            _token('NUMBER_DECIMAL', '6'),
            _token('RIGHT_SQUARE_BRACKET', ']'),
            _token('RESERVED_STATEMENT_OF', 'OF'),
            _token('IDENTIFIER', 'Color'),
            _token('IDENTIFIER', 'ColorPlane_2'),
            _token('OPERATOR_EQUAL_TO', '='),
            _token('RESERVED_TYPE_ARRAY', 'ARRAY'),
            _token('LEFT_SQUARE_BRACKET', '['),
            _token('NUMBER_DECIMAL', '0'),
            _token('RANGE', '..'),
            _token('NUMBER_DECIMAL', '200'),
            _token('COMMA', ','),
            _token('NUMBER_DECIMAL', '1'),
            _token('RANGE', '..'),
            _token('NUMBER_DECIMAL', '6'),
            _token('RIGHT_SQUARE_BRACKET', ']'),
            _token('RESERVED_STATEMENT_OF', 'OF'),
            _token('IDENTIFIER', 'Color')
        ])

    def test_type_declaration_array_single_dimension(self):
        test_code = "TYPE ColorList = ARRAY[1..6] OF Color \n Numbers = ARRAY[Green..Orange] OF Integer \n" \
                    "Flags = ARRAY[Color] OF Boolean ColorPlane = ARRAY[0 .. 200] OF ColorList"
        result = _run_lexer(test_code)
        print(result)
        assert_lex_equivalent(result, [
             _token('RESERVED_DECLARATION_TYPE', 'TYPE'),
             _token('IDENTIFIER', 'ColorList'),
             _token('OPERATOR_EQUAL_TO', '='),
             _token('RESERVED_TYPE_ARRAY', 'ARRAY'),
             _token('LEFT_SQUARE_BRACKET', '['),
             _token('NUMBER_DECIMAL', '1'),
             _token('RANGE', '..'),
             _token('NUMBER_DECIMAL', '6'),
             _token('RIGHT_SQUARE_BRACKET', ']'),
             _token('RESERVED_STATEMENT_OF', 'OF'),
             _token('IDENTIFIER', 'Color'),
             _token('IDENTIFIER', 'Numbers'),
             _token('OPERATOR_EQUAL_TO', '='),
             _token('RESERVED_TYPE_ARRAY', 'ARRAY'),
             _token('LEFT_SQUARE_BRACKET', '['),
             _token('IDENTIFIER', 'Green'),
             _token('RANGE', '..'),
             _token('IDENTIFIER', 'Orange'),
             _token('RIGHT_SQUARE_BRACKET', ']'),
             _token('RESERVED_STATEMENT_OF', 'OF'),
             _token('RESERVED_TYPE_INTEGER', 'Integer'),
             _token('IDENTIFIER', 'Flags'),
             _token('OPERATOR_EQUAL_TO', '='),
             _token('RESERVED_TYPE_ARRAY', 'ARRAY'),
             _token('LEFT_SQUARE_BRACKET', '['),
             _token('IDENTIFIER', 'Color'),
             _token('RIGHT_SQUARE_BRACKET', ']'),
             _token('RESERVED_STATEMENT_OF', 'OF'),
             _token('RESERVED_TYPE_BOOLEAN', 'Boolean'),
             _token('IDENTIFIER', 'ColorPlane'),
             _token('OPERATOR_EQUAL_TO', '='),
             _token('RESERVED_TYPE_ARRAY', 'ARRAY'),
             _token('LEFT_SQUARE_BRACKET', '['),
             _token('NUMBER_DECIMAL', '0'),
             _token('RANGE', '..'),
             _token('NUMBER_DECIMAL', '200'),
             _token('RIGHT_SQUARE_BRACKET', ']'),
             _token('RESERVED_STATEMENT_OF', 'OF'),
             _token('IDENTIFIER', 'ColorList')
        ])

    def test_type_declaration_set(self):
        test_code = "TYPE SomeColors = SET OF SmallColor"
        result = _run_lexer(test_code)
        print(result)
        assert_lex_equivalent(result, [
            _token('RESERVED_DECLARATION_TYPE', 'TYPE'),
            _token('IDENTIFIER', 'SomeColors'),
            _token('OPERATOR_EQUAL_TO', '='),
            _token('RESERVED_TYPE_SET', 'SET'),
            _token('RESERVED_STATEMENT_OF', 'OF'),
            _token('IDENTIFIER', 'SmallColor')
        ])

    def test_type_declaration_subrange(self):
        test_code = "TYPE SmallColor = Green..Blue \n SmallInt = -128..127 \n This = 1 .. 20"
        result = _run_lexer(test_code)
        print(result)
        assert_lex_equivalent(result, [
            _token('RESERVED_DECLARATION_TYPE', 'TYPE'),
            _token('IDENTIFIER', 'SmallColor'),
            _token('OPERATOR_EQUAL_TO', '='),
            _token('IDENTIFIER', 'Green'),
            _token('RANGE', '..'),
            _token('IDENTIFIER', 'Blue'),
            _token('IDENTIFIER', 'SmallInt'),
            _token('OPERATOR_EQUAL_TO', '='),
            _token('NUMBER_DECIMAL', '-128'),
            _token('RANGE', '..'),
            _token('NUMBER_DECIMAL', '127'),
            _token('IDENTIFIER', 'This'),
            _token('OPERATOR_EQUAL_TO', '='),
            _token('NUMBER_DECIMAL', '1'),
            _token('RANGE', '..'),
            _token('NUMBER_DECIMAL', '20'),
        ])

    def test_type_declaration_enumerated(self):
        test_code = "TYPE Color = (Red, Green, Yellow, Blue, Orange, Brown)"
        result = _run_lexer(test_code)
        print(result)
        assert_lex_equivalent(result, [
            _token('RESERVED_DECLARATION_TYPE', 'TYPE'),
            _token('IDENTIFIER', 'Color'),
            _token('OPERATOR_EQUAL_TO', '='),
            _token('LEFT_PARENTHESES', '('),
            _token('IDENTIFIER', 'Red'),
            _token('COMMA', ','),
            _token('IDENTIFIER', 'Green'),
            _token('COMMA', ','),
            _token('IDENTIFIER', 'Yellow'),
            _token('COMMA', ','),
            _token('IDENTIFIER', 'Blue'),
            _token('COMMA', ','),
            _token('IDENTIFIER', 'Orange'),
            _token('COMMA', ','),
            _token('IDENTIFIER', 'Brown'),
            _token('RIGHT_PARENTHESES', ')')
        ])

    def test_type_declaration_simple(self):
        test_code = "TYPE Number = Integer Float = Real Letter = Char Option = Boolean Paragraph = String Book = Text"
        result = _run_lexer(test_code)
        print(result)
        assert_lex_equivalent(result, [
            _token('RESERVED_DECLARATION_TYPE', 'TYPE'),
            _token('IDENTIFIER', 'Number'),
            _token('OPERATOR_EQUAL_TO', '='),
            _token('RESERVED_TYPE_INTEGER', 'Integer'),
            _token('IDENTIFIER', 'Float'),
            _token('OPERATOR_EQUAL_TO', '='),
            _token('RESERVED_TYPE_REAL', 'Real'),
            _token('IDENTIFIER', 'Letter'),
            _token('OPERATOR_EQUAL_TO', '='),
            _token('RESERVED_TYPE_CHAR', 'Char'),
            _token('IDENTIFIER', 'Option'),
            _token('OPERATOR_EQUAL_TO', '='),
            _token('RESERVED_TYPE_BOOLEAN', 'Boolean'),
            _token('IDENTIFIER', 'Paragraph'),
            _token('OPERATOR_EQUAL_TO', '='),
            _token('RESERVED_TYPE_STRING', 'String'),
            _token('IDENTIFIER', 'Book'),
            _token('OPERATOR_EQUAL_TO', '='),
            _token('RESERVED_TYPE_TEXT', 'Text')
        ])

    def test_const_declaration(self):
        test_code = "CONST MinSize = -3 \nMaxSize=3451 \nCharLit='G' \n" \
                    "StringLit='This is a STRING constant' \nExtraSize=MaxSize Yes=True \n No=False \n"
        result = _run_lexer(test_code)
        print(result)
        assert_lex_equivalent(result, [
            _token('RESERVED_DECLARATION_CONST', 'CONST'),
            _token('IDENTIFIER', 'MinSize'),
            _token('OPERATOR_EQUAL_TO', '='),
            _token('NUMBER_DECIMAL', '-3'),
            _token('IDENTIFIER', 'MaxSize'),
            _token('OPERATOR_EQUAL_TO', '='),
            _token('NUMBER_DECIMAL', '3451'),
            _token('IDENTIFIER', 'CharLit'),
            _token('OPERATOR_EQUAL_TO', '='),
            _token('CHARACTER', "'G'"),
            _token('IDENTIFIER', 'StringLit'),
            _token('OPERATOR_EQUAL_TO', '='),
            _token('STRING', "'This is a STRING constant'"),
            _token('IDENTIFIER', 'ExtraSize'),
            _token('OPERATOR_EQUAL_TO', '='),
            _token('IDENTIFIER', 'MaxSize'),
            _token('IDENTIFIER', 'Yes'),
            _token('OPERATOR_EQUAL_TO', '='),
            _token('CONSTANT_TRUE', 'True'),
            _token('IDENTIFIER', 'No'),
            _token('OPERATOR_EQUAL_TO', '='),
            _token('CONSTANT_FALSE', 'False')
        ])

    def test_operators(self):
        test_code = "<> >= <= := = + - * / ABS MOD DIV LSL LSR SHL SHR AND NOT OR XOR"
        result = _run_lexer(test_code)
        print(result)
        assert_lex_equivalent(result, [
            _token('OPERATOR_NOT_EQUAL_TO', '<>'),
            _token('OPERATOR_GREATER_OR_EQUAL_TO', '>='),
            _token('OPERATOR_LESS_OR_EQUAL_TO', '<='),
            _token('OPERATOR_ASSIGNMENT', ':='),
            _token('OPERATOR_EQUAL_TO', '='),
            _token('OPERATOR_PLUS', '+'),
            _token('OPERATOR_MINUS', '-'),
            _token('OPERATOR_MULTIPLY', '*'),
            _token('OPERATOR_DIVIDE', '/'),
            _token('RESERVED_OPERATOR_ABS', 'ABS'),
            _token('RESERVED_OPERATOR_MOD', 'MOD'),
            _token('RESERVED_OPERATOR_DIV', 'DIV'),
            _token('RESERVED_OPERATOR_LSL', 'LSL'),
            _token('RESERVED_OPERATOR_LSR', 'LSR'),
            _token('RESERVED_OPERATOR_SHL', 'SHL'),
            _token('RESERVED_OPERATOR_SHR', 'SHR'),
            _token('RESERVED_OPERATOR_AND', 'AND'),
            _token('RESERVED_OPERATOR_NOT', 'NOT'),
            _token('RESERVED_OPERATOR_OR', 'OR'),
            _token('RESERVED_OPERATOR_XOR', 'XOR')
        ])

    def test_labels(self):
        test_code = "100: I" + _newline + \
                    "LABEL 100;"
        result = _run_lexer(test_code)
        print(result)
        assert_lex_equivalent(result, [
            _token('NUMBER_DECIMAL', '100'),
            _token('COLON', ':'),
            _token('IDENTIFIER', 'I'),
            _token('RESERVED_DECLARATION_LABEL', 'LABEL'),
            _token('NUMBER_DECIMAL', '100'),
            _token('SEMICOLON', ';')
        ])

    def test_number_decimals(self):
        test_code = "-32768 -0 0 +0 +32768 1 -1-1 -1+1 +1-1 +1+1"
        result = _run_lexer(test_code)
        print(result)
        assert_lex_equivalent(result, [
            _token('NUMBER_DECIMAL', '-32768'),
            _token('NUMBER_DECIMAL', '-0'),
            _token('NUMBER_DECIMAL', '0'),
            _token('NUMBER_DECIMAL', '+0'),
            _token('NUMBER_DECIMAL', '+32768'),
            _token('NUMBER_DECIMAL', '1'),
            _token('NUMBER_DECIMAL', '-1'),
            _token('NUMBER_DECIMAL', '-1'),
            _token('NUMBER_DECIMAL', '-1'),
            _token('NUMBER_DECIMAL', '+1'),
            _token('NUMBER_DECIMAL', '+1'),
            _token('NUMBER_DECIMAL', '-1'),
            _token('NUMBER_DECIMAL', '+1'),
            _token('NUMBER_DECIMAL', '+1'),

        ])

    def test_number_hexadecimals(self):
        test_code = "$0 $00 $0000 $A $B $C $D $E $F $ABC $12A5 $5 $FFFF " \
                    "&H0 &H00 &H0000 &HA &HB &HC &HD &HE &HF &HABC &H12A5 &H5 &HFFFF"
        result = _run_lexer(test_code)
        print(result)
        assert_lex_equivalent(result, [
            _token('NUMBER_HEXADECIMAL', '$0'),
            _token('NUMBER_HEXADECIMAL', '$00'),
            _token('NUMBER_HEXADECIMAL', '$0000'),
            _token('NUMBER_HEXADECIMAL', '$A'),
            _token('NUMBER_HEXADECIMAL', '$B'),
            _token('NUMBER_HEXADECIMAL', '$C'),
            _token('NUMBER_HEXADECIMAL', '$D'),
            _token('NUMBER_HEXADECIMAL', '$E'),
            _token('NUMBER_HEXADECIMAL', '$F'),
            _token('NUMBER_HEXADECIMAL', '$ABC'),
            _token('NUMBER_HEXADECIMAL', '$12A5'),
            _token('NUMBER_HEXADECIMAL', '$5'),
            _token('NUMBER_HEXADECIMAL', '$FFFF'),
            _token('NUMBER_HEXADECIMAL', '&H0'),
            _token('NUMBER_HEXADECIMAL', '&H00'),
            _token('NUMBER_HEXADECIMAL', '&H0000'),
            _token('NUMBER_HEXADECIMAL', '&HA'),
            _token('NUMBER_HEXADECIMAL', '&HB'),
            _token('NUMBER_HEXADECIMAL', '&HC'),
            _token('NUMBER_HEXADECIMAL', '&HD'),
            _token('NUMBER_HEXADECIMAL', '&HE'),
            _token('NUMBER_HEXADECIMAL', '&HF'),
            _token('NUMBER_HEXADECIMAL', '&HABC'),
            _token('NUMBER_HEXADECIMAL', '&H12A5'),
            _token('NUMBER_HEXADECIMAL', '&H5'),
            _token('NUMBER_HEXADECIMAL', '&HFFFF')
        ])

    def test_number_octal(self):
        test_code = "&O0 &O347 &O177777 &o0 &o347 &o177777"
        result = _run_lexer(test_code)
        print(result)
        assert_lex_equivalent(result, [
            _token('NUMBER_OCTAL', '&O0'),
            _token('NUMBER_OCTAL', '&O347'),
            _token('NUMBER_OCTAL', '&O177777'),
            _token('NUMBER_OCTAL', '&o0'),
            _token('NUMBER_OCTAL', '&o347'),
            _token('NUMBER_OCTAL', '&o177777')
        ])

    def test_number_binary(self):
        test_code = "&B0 &B1 &B01110110 &B11100111 &b0 &b1 &b01110110 &b11100111"
        result = _run_lexer(test_code)
        print(result)
        assert_lex_equivalent(result, [
            _token('NUMBER_BINARY', '&B0'),
            _token('NUMBER_BINARY', '&B1'),
            _token('NUMBER_BINARY', '&B01110110'),
            _token('NUMBER_BINARY', '&B11100111'),
            _token('NUMBER_BINARY', '&b0'),
            _token('NUMBER_BINARY', '&b1'),
            _token('NUMBER_BINARY', '&b01110110'),
            _token('NUMBER_BINARY', '&b11100111'),
        ])

    def test_number_real(self):
        test_code = "-1.0 1.0 +1.0 -6.74 6.74 +6.74 -56.3E6 56.3E6 +56.3E6 1.2E-3 1.2E3 1.2E+3 -10.2E-3 10.2E3 +10.2E+3"
        result = _run_lexer(test_code)
        print(result)
        assert_lex_equivalent(result, [
            _token('NUMBER_REAL', "-1.0"),
            _token('NUMBER_REAL', "1.0"),
            _token('NUMBER_REAL', "+1.0"),
            _token('NUMBER_REAL', "-6.74"),
            _token('NUMBER_REAL', "6.74"),
            _token('NUMBER_REAL', "+6.74"),
            _token('NUMBER_REAL', "-56.3E6"),
            _token('NUMBER_REAL', "56.3E6"),
            _token('NUMBER_REAL', "+56.3E6"),
            _token('NUMBER_REAL', "1.2E-3"),
            _token('NUMBER_REAL', "1.2E3"),
            _token('NUMBER_REAL', "1.2E+3"),
            _token('NUMBER_REAL', "-10.2E-3"),
            _token('NUMBER_REAL', "10.2E3"),
            _token('NUMBER_REAL', "+10.2E+3")
        ])

    def test_strings_character(self):
        test_code = "'A' 'a' 'Z' 'z' '0' '9' '!' '#' '$' '%' '^' '&' '(' ')' '*' '+' ',' '-' '.' '/' ':' ';' " + \
                    "'<' '=' '>' '?' '@' '[' ']' ' ' " + "'''" + "'\"'"
        result = _run_lexer(test_code)
        print(result)
        assert_lex_equivalent(result, [
            _token('CHARACTER', "'A'"),
            _token('CHARACTER', "'a'"),
            _token('CHARACTER', "'Z'"),
            _token('CHARACTER', "'z'"),
            _token('CHARACTER', "'0'"),
            _token('CHARACTER', "'9'"),
            _token('CHARACTER', "'!'"),
            _token('CHARACTER', "'#'"),
            _token('CHARACTER', "'$'"),
            _token('CHARACTER', "'%'"),
            _token('CHARACTER', "'^'"),
            _token('CHARACTER', "'&'"),
            _token('CHARACTER', "'('"),
            _token('CHARACTER', "')'"),
            _token('CHARACTER', "'*'"),
            _token('CHARACTER', "'+'"),
            _token('CHARACTER', "','"),
            _token('CHARACTER', "'-'"),
            _token('CHARACTER', "'.'"),
            _token('CHARACTER', "'/'"),
            _token('CHARACTER', "':'"),
            _token('CHARACTER', "';'"),
            _token('CHARACTER', "'<'"),
            _token('CHARACTER', "'='"),
            _token('CHARACTER', "'>'"),
            _token('CHARACTER', "'?'"),
            _token('CHARACTER', "'@'"),
            _token('CHARACTER', "'['"),
            _token('CHARACTER', "']'"),
            _token('CHARACTER', "' '"),
            _token('CHARACTER', "'''"),
            _token('CHARACTER', "'\"'"),
        ])

    def test_strings_string(self):
        test_code = "'PAGE HEADING TITLE' 'sam & joe' 'AaZz09!#$%^&()*+,-./:;<=>?@[]' '0123456789' 'THIS IS A \"QUOTE\" OF ANOTHER BOOK'"
        result = _run_lexer(test_code)
        print(result)
        assert_lex_equivalent(result, [
            _token('STRING', "'PAGE HEADING TITLE'"),
            _token('STRING', "'sam & joe'"),
            _token('STRING', "'AaZz09!#$%^&()*+,-./:;<=>?@[]'"),
            _token('STRING', "'0123456789'"),
            _token('STRING', "'THIS IS A \"QUOTE\" OF ANOTHER BOOK'")
        ])

    def test_comments(self):
        test_code = "(* a single line comment *) \n  (* multiple \n lines \n comment *)"
        result = _run_lexer(test_code)
        print(result)
        assert_lex_equivalent(result, [
            _token('COMMENT', "(* a single line comment *)"),
            _token('COMMENT', "(* multiple \n lines \n comment *)")
        ])

    def test_lower_case(self):
        test_code = "program test;                        \n" \
                    " const                               \n" \
                    "   PI = 3.1415;                      \n" \
                    "                                     \n" \
                    " var                                 \n" \
                    "   a, b: real;                       \n" \
                    "                                     \n" \
                    " procedure hello(s: string; n: real);\n" \
                    " begin                               \n" \
                    "   writeln(s);                       \n" \
                    " end;                                \n" \
                    "                                     \n" \
                    " begin                               \n" \
                    "   a := PI;                          \n" \
                    "   b := a * 10;                      \n" \
                    "   hello('Hello World!', b);         \n" \
                    " end.                                \n"
        result = _run_lexer(test_code)
        print(result)
        assert_lex_equivalent(result, [
            _token('RESERVED_STRUCTURE_PROGRAM', 'program'),
            _token('IDENTIFIER', 'test'),
            _token('SEMICOLON', ';'),
            _token('RESERVED_DECLARATION_CONST', 'const'),
            _token('IDENTIFIER', 'PI'),
            _token('OPERATOR_EQUAL_TO', '='),
            _token('NUMBER_REAL', '3.1415'),
            _token('SEMICOLON', ';'),
            _token('RESERVED_DECLARATION_VAR', 'var'),
            _token('IDENTIFIER', 'a'),
            _token('COMMA', ','),
            _token('IDENTIFIER', 'b'),
            _token('COLON', ':'),
            _token('RESERVED_TYPE_REAL', 'real'),
            _token('SEMICOLON', ';'),
            _token('RESERVED_DECLARATION_PROCEDURE', 'procedure'),
            _token('IDENTIFIER', 'hello'),
            _token('LEFT_PARENTHESES', '('),
            _token('IDENTIFIER', 's'),
            _token('COLON', ':'),
            _token('RESERVED_TYPE_STRING', 'string'),
            _token('SEMICOLON', ';'),
            _token('IDENTIFIER', 'n'),
            _token('COLON', ':'),
            _token('RESERVED_TYPE_REAL', 'real'),
            _token('RIGHT_PARENTHESES', ')'),
            _token('SEMICOLON', ';'),
            _token('RESERVED_STRUCTURE_BEGIN', 'begin'),
            _token('RESERVED_STATEMENT_WRITELN', 'writeln'),
            _token('LEFT_PARENTHESES', '('),
            _token('IDENTIFIER', 's'),
            _token('RIGHT_PARENTHESES', ')'),
            _token('SEMICOLON', ';'),
            _token('RESERVED_STRUCTURE_END', 'end'),
            _token('SEMICOLON', ';'),
            _token('RESERVED_STRUCTURE_BEGIN', 'begin'),
            _token('IDENTIFIER', 'a'),
            _token('OPERATOR_ASSIGNMENT', ':='),
            _token('IDENTIFIER', 'PI'),
            _token('SEMICOLON', ';'),
            _token('IDENTIFIER', 'b'),
            _token('OPERATOR_ASSIGNMENT', ':='),
            _token('IDENTIFIER', 'a'),
            _token('OPERATOR_MULTIPLY', '*'),
            _token('NUMBER_DECIMAL', '10'),
            _token('SEMICOLON', ';'),
            _token('IDENTIFIER', 'hello'),
            _token('LEFT_PARENTHESES', '('),
            _token('STRING', "'Hello World!'"),
            _token('COMMA', ','),
            _token('IDENTIFIER', 'b'),
            _token('RIGHT_PARENTHESES', ')'),
            _token('SEMICOLON', ';'),
            _token('RESERVED_STRUCTURE_END', 'end'),
            _token('DOT', '.')
        ])
