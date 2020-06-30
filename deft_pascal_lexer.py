import ply.lex as lex


class DeftPascalReservedSymbols:

    def __init__(self):
        self._reserved_keywords = {
            'break': 'RESERVED_BREAK',
            'call': 'RESERVED_CALL',
            'chr': 'RESERVED_CHR',
            'exit': 'RESERVED_EXIT',
            'external': 'RESERVED_EXTERNAL',
            'file': 'RESERVED_FILE',
            'forward': 'RESERVED_FORWARD',
            'in': 'RESERVED_IN',
            'new': 'RESERVED_NEW',
            'odd': 'RESERVED_ODD',
            'ord': 'RESERVED_ORD',
            'packed': 'RESERVED_PACKED',
            'pred': 'RESERVED_PRED',
            'public': 'RESERVED_PUBLIC',
            'record': 'RESERVED_RECORD',
            'reset': 'RESERVED_RESET',
            'rewrite': 'RESERVED_REWRITE',
            'sizeof': 'RESERVED_SIZEOF',
            'static': 'RESERVED_STATIC',
            'succ': 'RESERVED_SUCC',

            # structure
            'program': 'RESERVED_STRUCTURE_PROGRAM',
            'interface': 'RESERVED_STRUCTURE_INTERFACE',
            'module': 'RESERVED_STRUCTURE_MODULE',

            # declarations
            'const': 'RESERVED_DECLARATION_CONST',
            'label': 'RESERVED_DECLARATION_LABEL',
            'type': 'RESERVED_DECLARATION_TYPE',
            'var': 'RESERVED_DECLARATION_VAR',
            'procedure': 'RESERVED_DECLARATION_PROCEDURE',
            'function': 'RESERVED_DECLARATION_FUNCTION',

            # statements
            'begin': 'RESERVED_STATEMENT_BEGIN',
            'end': 'RESERVED_STATEMENT_END',
            'case': 'RESERVED_STATEMENT_CASE',
            'of': 'RESERVED_STATEMENT_OF',
            'else': 'RESERVED_STATEMENT_ELSE',
            'for': 'RESERVED_STATEMENT_FOR',
            'to': 'RESERVED_STATEMENT_TO',
            'do': 'RESERVED_STATEMENT_DO',
            'downto': 'RESERVED_STATEMENT_DOWNTO',
            'goto': 'RESERVED_STATEMENT_GOTO',
            'if': 'RESERVED_STATEMENT_IF',
            'then': 'RESERVED_STATEMENT_THEN',
            'read': 'RESERVED_STATEMENT_READ',
            'readln': 'RESERVED_STATEMENT_READLN',
            'repeat': 'RESERVED_STATEMENT_REPEAT',
            'until': 'RESERVED_STATEMENT_UNTIL',
            'while': 'RESERVED_STATEMENT_WHILE',
            'with': 'RESERVED_STATEMENT_WITH',
            'write': 'RESERVED_STATEMENT_WRITE',
            'writeln': 'RESERVED_STATEMENT_WRITELN',

            # operators
            'abs': 'RESERVED_OPERATOR_ABS',
            'and': 'RESERVED_OPERATOR_AND',
            'div': 'RESERVED_OPERATOR_DIV',
            'lsl': 'RESERVED_OPERATOR_LSL',
            'lsr': 'RESERVED_OPERATOR_LSR',
            'mod': 'RESERVED_OPERATOR_MOD',
            'not': 'RESERVED_OPERATOR_NOT',
            'or':  'RESERVED_OPERATOR_OR',
            'shl': 'RESERVED_OPERATOR_SHL',
            'shr': 'RESERVED_OPERATOR_SHR',
            'xor': 'RESERVED_OPERATOR_XOR',

            # types
            'array':   'RESERVED_TYPE_ARRAY',
            'boolean': 'RESERVED_TYPE_BOOLEAN',
            'byte':    'RESERVED_TYPE_BYTE',
            'char':    'RESERVED_TYPE_CHAR',
            'integer': 'RESERVED_TYPE_INTEGER',
            'real':    'RESERVED_TYPE_REAL',
            'string':  'RESERVED_TYPE_STRING',
            'text':    'RESERVED_TYPE_TEXT',
            'word':    'RESERVED_TYPE_WORD',
            'set':     'RESERVED_TYPE_SET',

        }

        self._reserved_literals = ['!', '"', '#', '$', '%', '^', '&', '(', ')',
                                   '*', '+', ',', '-', '.', '/', ':', ';', '<',
                                   '=', '>', '?', '@', '[', ']'
                                  ]

    def reserved_keywords(self):
        return list(self._reserved_keywords.values())

    def reserved_literals(self):
        return list(self._reserved_literals)

    def get_keyword(self, key, default):
        return self._reserved_keywords.get(key, default)


class DeftPascalLexer:
    tokens = [
                 # Symbols and operators
                 #'PLUS',
                 #'MINUS',
                 #'MULTIPLY',
                 #'DIVIDE',

                 #'LANGLE',  # LEFT ANGLE BRACKET '<'
                 #'RANGLE',
                 #'DOT',
                 # 'INVERTCOMMA',                                      # '\''
                 # 'INVERTDOUBLECOMMA',                                # '\"'
                 #'POWER',  # '^'
                 # 'ATRATE',                                           # '@'
                 # 'DOLLAR',                                          # will have to check whether to remove or keep these (DOLLAR and HASH)
                 # 'HASH',
                 # 'AMPERSAND',
                 # 'PERCENT',
                 #'DOUBLESTAR',  # used for calculating powers '**'
                 # 'CINPUT',                                          # '<<' used for input in C
                 # 'COUTPUT',                                         # '>>' probably this and the upper symbol are not to tbe used in pascal
                 # 'LRANGLE',                                         # '<>' again probably not used in our grammar
                 # 'DOUBLESLASH',                                      # '//'

                 # number
                 'NUMBER_REAL',
                 'NUMBER_DECIMAL',
                 'NUMBER_BINARY',
                 'NUMBER_OCTAL',
                 'NUMBER_HEXADECIMAL',

                 # strings
                 'CHARACTER',
                 'STRING',
                 'WHERE',

                 # identifiers
                 'IDENTIFIER',

                 # operators
                 'OPERATOR_EQUAL_TO',
                 'OPERATOR_NOT_EQUAL_TO',
                 'OPERATOR_GREATER_OR_EQUAL_TO',
                 'OPERATOR_LESS_OR_EQUAL_TO',
                 'OPERATOR_ASSIGNMENT',

                 # structures
                 'COMMENT',
                 'COLON',
                 'SEMICOLON',
                 'LEFT_PARENTHESES',
                 'RIGHT_PARENTHESES',
                 'COMMA',
                 'RANGE',
                 'LEFT_SQUARE_BRACKET',
                 'RIGHT_SQUARE_BRACKET',

                 # constants
                 'CONSTANT_TRUE',
                 'CONSTANT_FALSE'

             ] + DeftPascalReservedSymbols().reserved_keywords()

    #t_PLUS = r'\+'
    #t_MINUS = r'\-'
    #t_MULTIPLY = r'\*'
    #t_DIVIDE = r'\/'
    #t_POWER = r'\^'
    # t_ATRATE = r'\@'
    # t_LCURLY = r'\{'
    # t_RCURLY = r'\}'
    # t_AMPERSAND = r'\&'
    # t_PERCENT = r'\%'
    #t_DOUBLESTAR = r'\*\*'
    # t_DOUBLESLASH = r'\\\\'
    #t_LANGLE = r'\<'
    #t_RANGLE = r'\>'
    #t_DOT = r'\.'
    # t_INVERTCOMMA = r'\''
    # t_INVERTDOUBLECOMMA = r'\"'

    t_LEFT_PARENTHESES = r'\('
    t_RIGHT_PARENTHESES = r'\)'
    t_COLON = r'\:'
    t_SEMICOLON = r'\;'
    t_COMMA = r'\,'
    t_RANGE = r'\.{2}'
    t_LEFT_SQUARE_BRACKET = r'\['
    t_RIGHT_SQUARE_BRACKET = r'\]'

    t_OPERATOR_EQUAL_TO = r'\='
    t_OPERATOR_NOT_EQUAL_TO = r'\<\>'
    t_OPERATOR_GREATER_OR_EQUAL_TO = r'\>\='
    t_OPERATOR_LESS_OR_EQUAL_TO = r'\<\='
    t_OPERATOR_ASSIGNMENT = r'\:\='

    def t_IDENTIFIER(self, t):
        r'[_A-Za-z]+[A-Za-z0-9_]*'
        t.type = self._reserved.get_keyword(t.value.lower(), 'IDENTIFIER')
        if t.value == 'True':
            t.type = 'CONSTANT_TRUE'
        elif t.value == 'False':
            t.type = 'CONSTANT_FALSE'
        return t

    def t_NUMBER(self, t):
        # identifies decimal and real numbers classifying them accordingly
        r"[+-]?\d+([.]\d+(E[+-]?\d+)?)?"
        if '.' in t.value:
            t.type = 'NUMBER_REAL'
        else:
            t.type = 'NUMBER_DECIMAL'
        return t

    def t_NUMBER_HEXADECIMAL(self, t):
        r'\&[Hh][0-9A-F]+|\$[0-9A-F]+'
        return t

    def t_NUMBER_OCTAL(self, t):
        # Deft Pascal does not contain octal numbers, adding here for convenience
        r'\&[Oo][0-7]+'
        return t

    def t_NUMBER_BINARY(self, t):
        # Deft Pascal does not contain binary numbers, adding here for convenience
        r'\&[Bb][0-1]+'
        return t

    def t_CHARACTER(self, t):
        r"\'[\ A-Za-z0-9!\"#$%^&\'()*+,\-.\/:;<=>?@\[\]]\'"
        return t

    def t_STRING(self, t):
        # This implementation differs from Deft Pascal as it does not allow single quotes inside a string
        # In Deft Pascal this example is valid ['Sam & Joe''s Sub Shop'] but the expression below does not support it
        r"\'[\ A-Za-z0-9!\"#$%^&()*+,\-.\/:;<=>?@\[\]]{2,}\'"
        return t

    # define comment
    def t_COMMENT(self, t):
        r"\(\*[^\*\)]*\*\)"
        return t

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    # Error handling rule
    def t_error(self, t):
        print("Syntax error at {0},{1} - illegal character '{2}'".format(t.lineno, t.lexpos, t.value))
        t.lexer.skip(1)

    def __init__(self, debug_flag=False):
        self._reserved = DeftPascalReservedSymbols()
        self._lexer = lex.lex(module=self, debug=debug_flag)

    def set_input(self, input_string):
        self._lexer.input(input_string)

    def get_token(self):
        return self._lexer.token()

