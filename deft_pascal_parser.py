from deft_pascal_lexer import DeftPascalLexer
from symbol_table import SymbolTable, Constant, Variable
import ply.yacc as yacc



class DeftPascalParser:

    tokens = DeftPascalLexer.tokens

    #start = 'pascal_program'

    precedence = (
        ('nonassoc', 'OPERATOR_LESS_THEN', 'OPERATOR_GREATER_THEN'),
        ('left', 'OPERATOR_PLUS', 'OPERATOR_MINUS'),
        ('left', 'OPERATOR_MULTIPLY', 'OPERATOR_DIVIDE'),
    )

    #precedence = (
    #    ('left', 'COLON'),
    #    ('left', 'COMMA'),
    #    ('left', 'AND', 'OR'),
    #    ('left', 'EQUALS', 'NOT_EQUAL', 'GREATER_THAN', 'LESS_THAN', 'EQUAL_GREATER_THAN', 'EQUAL_LESS_THAN'),
    #    ('left', 'AS'),
    #    ('left', 'PLUS', 'MINUS'),
    #    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    #    ('left', 'EXP'),
    #    ('right', 'UMINUS', 'NOT'),
    #    ('left', 'DOT'),
    #)

    #precedence = (
    #    ('nonassoc', 'ID', 'ARRAY_ID'),
    #    ('left', 'OR'),
    #    ('left', 'AND'),
    #    ('left', 'XOR'),
    #    ('right', 'NOT'),
    #    ('left', 'LT', 'GT', 'EQ', 'LE', 'GE', 'NE'),
    #    ('left', 'BOR'),
    #    ('left', 'BAND', 'BXOR', 'SHR', 'SHL'),
    #    ('left', 'BNOT', 'PLUS', 'MINUS'),
    #    ('left', 'MOD'),
    #    ('left', 'MUL', 'DIV'),
    #    ('right', 'UMINUS'),
    #    ('right', 'POW'),
    #    ('left', 'RP'),
    #    ('right', 'LP'),
    #    ('right', 'ELSE'),
    #    ('left', 'CO'),
    #    ('left', 'LABEL'),
    #    ('left', 'NEWLINE'),
    #)

    def p_pascal_program(self, p):
        """
        pascal_program : program_header declarations compound_statement DOT
        """
        print('p_pascal_program')

    def p_program_header(self, p):
        """
        program_header : RESERVED_STRUCTURE_PROGRAM IDENTIFIER SEMICOLON
                       | RESERVED_STRUCTURE_PROGRAM IDENTIFIER LEFT_PARENTHESES prgid_list RIGHT_PARENTHESES SEMICOLON
        """
        self._stack_scope.append((p[2], 0))
        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]
        self._symbol_table.append(Constant('True', context_label, context_level, True, 0))
        self._symbol_table.append(Constant('False', context_label, context_level, False, 0))
        print('p_program_header {0}'.format(self._stack_scope))

    def p_program_header_id_list(self, p):
        """
        prgid_list : IDENTIFIER
                   | IDENTIFIER COMMA prgid_list
        """
        print('p_program_header_id_list [{0}]'.format(p.slice))

    def p_declarations(self, p):
        """
        declarations : constant_definitions variable_declarations
        """
        print('p_declarations [{0}]'.format(p.slice))

    def p_variable_declarations(self, p):
        """
        variable_declarations : RESERVED_DECLARATION_VAR variable_declaration_list
                              |
        """
        # print('p_variable_declarations', '@@', p.slice, '@@')
        print('.')

    def p_variable_declaration_list(self, p):
        """
        variable_declaration_list : variable_declaration
                                  | variable_declaration variable_declaration_list
        """
        # print('p_variable_declaration_list', '@@', p.slice, '@@')
        print('.')

    def p_variable_declaration(self, p):
        """
        variable_declaration : variable_declaration_id_list COLON variable_declaration_type_specifier SEMICOLON
        """
        # print('p_variable_dec [{0}]'.format(p.slice))
        print('.')

    def p_variable_declaration_id_list(self, p):
        """
        variable_declaration_id_list : IDENTIFIER
                                     | IDENTIFIER COMMA variable_declaration_id_list
        """
        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]
        a_symbol = Variable(p[1], context_label, context_level, None, None)
        # scenarios:
        # - identifier not declared
        # - identifier already declared (as a constant or a variable)
        if self._symbol_table.has_equal(a_symbol, equal_type=False):
            print('ERROR 2 - Identifier already declared in the current scope')
        else:
            self._symbol_table.append(a_symbol)
            self._stack_variables.append(a_symbol)
            print("variable declared : '{0}' stack: {1} {2}".format(p[1], self._stack_variables, self._symbol_table))

    def p_variable_declaration_type_specifier(self, p):
        """
        variable_declaration_type_specifier : IDENTIFIER
                                            | RESERVED_TYPE_REAL
                                            | RESERVED_TYPE_BOOLEAN
                                            | RESERVED_TYPE_BYTE
                                            | RESERVED_TYPE_CHAR
                                            | RESERVED_TYPE_INTEGER
                                            | RESERVED_TYPE_STRING
                                            | RESERVED_TYPE_TEXT
                                            | RESERVED_TYPE_WORD
                                            | RESERVED_TYPE_SET
        """
        for a_symbol in self._stack_variables:
            a_symbol.first_attribute = p[1]
        self._stack_variables = []
        print("variable typed : '{0}' stack: {1} {2}".format(p[1], self._stack_variables, self._symbol_table))


    def p_constant_definitions(self, p):
        """
        constant_definitions : RESERVED_DECLARATION_CONST constant_definition_list
                             |
        """
        # print('p_constant_definitions', '@@', p.slice, '@@')
        print('.')

    def p_constant_definition_list(self, p):
        """
        constant_definition_list : constant_definition
                                 | constant_definition constant_definition_list
        """
        # print('p_constant_definition_list', '@@', p.slice, '@@')
        print('.')

    def p_constant_definition(self, p):
        """
        constant_definition : IDENTIFIER OPERATOR_EQUAL_TO constant_definition_value SEMICOLON
        """
        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]
        a_value = self._stack_constants.pop()
        a_symbol = Constant(str(p[1]), context_label, context_level, a_value, None)
        # scenarios:
        # - identifier not declared
        # - identifier already declared (as a constant or a variable)
        if self._symbol_table.has_equal(a_symbol, equal_type=False):
            print('ERROR 6 - Identifier already declared in the current scope')
        else:
            self._symbol_table.append(a_symbol)
            print("constant declared '{0}' stack: {1} {2}".format(p[1], self._stack_constants, self._symbol_table))

    def p_constant_definition_value(self, p):
        """
        constant_definition_value : NUMBER_REAL
                                  | NUMBER_DECIMAL
                                  | NUMBER_BINARY
                                  | NUMBER_OCTAL
                                  | NUMBER_HEXADECIMAL
                                  | CHARACTER
                                  | STRING
                                  | CONSTANT_TRUE
                                  | CONSTANT_FALSE
        """
        self._stack_constants.append(p[1])
        print("constant valued : '{0}' stack: {1}".format(p[1], self._stack_constants))

    def p_compound_statement(self, p):
        """
        compound_statement : RESERVED_STRUCTURE_BEGIN statement_list RESERVED_STRUCTURE_END
        """
        # print('p_compound_statement', '@@', p.slice, '@@')
        print('.')

    def p_statement_list(self, p):
        """
        statement_list : statement
                       | statement SEMICOLON statement_list
        """
        # print(p.slice[0].type, p[1], '@@', p.slice, '@@')
        print('.')

    def p_statement(self, p):
        """
        statement : compound_statement
                  | assignment_statement
                  | procedure_call
                  | write_call
                  | writeln_call
                  |
        """
        # print(p.slice[0].type, p[1])
        print('p_statement ->', p.slice)
        # print('.')

    def p_write_call(self, p):
        """
        write_call : RESERVED_STATEMENT_WRITE actuals
        """
        # print('p_write_call', '@@', p.slice, '@@')
        print('WRITE')

    def p_writeln_call(self, p):
        """
        writeln_call : RESERVED_STATEMENT_WRITELN actuals
        """
        # print('p_writeln_call', '@@', p.slice, '@@')
        print('WRITE')

    def p_procedure_call(self, p):
        """
        procedure_call : IDENTIFIER actuals
        """
        # print('p_procedure_call', '@@', p.slice, '@@')
        print('.')

    def p_actuals(self, p):
        """
        actuals : LEFT_PARENTHESES expression_list RIGHT_PARENTHESES
                |
        """
        # print('p_actuals', '@@', p.slice, '@@')
        print('.')

    def p_expression_list(self, p):
        """
        expression_list : expression
                        | expression COMMA expression_list
        """
        # print('p_expression_list', '@@', p.slice, '@@')
        print('.')

    def p_assignment_statement(self, p):
        """
        assignment_statement : variable_in_assigment OPERATOR_ASSIGNMENT expression
        """
        print('p_assignment_statement ->', p.slice)
        # print('.')

    def p_variable_in_assigment(self, p):
        """
        variable_in_assigment : IDENTIFIER
        """
        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]
        # scenarios:
        a_symbol = Constant(p[1], context_label, context_level, None, None)
        if self._symbol_table.has_equal(a_symbol) or self._symbol_table.has_equal_at_lower_scope(a_symbol):
            # assignment to a declared constant in the current or lower scope
            print('ERROR 13 - Invalid assignment to a constant')
        else:
            a_symbol = Variable(p[1], context_label, context_level, None, None)
            if not self._symbol_table.has_equal(a_symbol):
                if not self._symbol_table.has_equal_at_lower_scope(a_symbol):
                    # assignment to an undeclared variable
                    print('ERROR 12 - Invalid assignment to an undeclared variable')
                else:
                    # assignment to a declared variable in a lower scope
                    a_symbol = self._symbol_table.get_from_lower_scope(a_symbol)
                    print("assignment to : {0}".format(a_symbol))
            else:
                # assignment to a declared variable in the same scope
                a_symbol = self._symbol_table.get(a_symbol)
                print("assignment to : {0}".format(a_symbol))

    def p_expression(self, p):
        """
        expression : simple_expression
                   | simple_expression relational_operator simple_expression
        """
        # print('p_expression ->', p.slice)
        print('.')

    def p_simple_expression(self, p):
        """
        simple_expression : term addition_operator term
                          | term
        """
        # print('p_simple_expression ->', p.slice)
        print('.')

    def p_relational_operator(self, p):
        """
        relational_operator : OPERATOR_EQUAL_TO
                            | OPERATOR_NOT_EQUAL_TO
                            | OPERATOR_LESS_THEN
                            | OPERATOR_LESS_OR_EQUAL_TO
                            | OPERATOR_GREATER_OR_EQUAL_TO
                            | OPERATOR_GREATER_THEN
        """
        print('p_relational_operator', p[1])

    def p_addition_operator(self, p):
        """
        addition_operator : OPERATOR_PLUS
                          | OPERATOR_MINUS
                          | RESERVED_OPERATOR_OR
        """
        print('p_addition_operator', p.slice)

    def p_term(self, p):
        """
        term : factor
             | term OPERATOR_MULTIPLY factor
             | term OPERATOR_DIVIDE factor
             | term RESERVED_OPERATOR_DIV factor
             | term RESERVED_OPERATOR_MOD factor
             | term RESERVED_OPERATOR_AND factor
        """
        # print('p_term ->', p.slice)
        print('BinaryOperator({0}, {1}, {2})'.format(p[0], p[1], p[1]))

    def p_factor(self, p):
        """
        factor : LEFT_PARENTHESES expression RIGHT_PARENTHESES
               | RESERVED_OPERATOR_NOT factor
               | constant_in_expression
               | variable_in_assigment
        """
        print('.')
        # print('p_factor ->', p.slice)

    def p_constant_in_expression(self, p):
        """
        constant_in_expression : NUMBER_REAL
                               | NUMBER_DECIMAL
                               | NUMBER_BINARY
                               | NUMBER_OCTAL
                               | NUMBER_HEXADECIMAL
                               | CHARACTER
                               | STRING
                               | CONSTANT_TRUE
                               | CONSTANT_FALSE
        """
        self._stack_operands.append(p[1])
        print("constant in expression : '{0}' stack: {1}".format(p[1], self._stack_operands))

    #def p_command_write(self, p):
    #    '''command : RESERVED_STATEMENT_WRITE LEFT_PARENTHESES NUMBER_DECIMAL RIGHT_PARENTHESES SEMICOLON'''
    #    #p[0] = ('WRITE', p[1], p[2], p[3], p[4], p[5])
    #    p[0] = 'print({0})'.format(p[3])

        # Error rule for syntax errors

    def p_error(self, p):
        print("Syntax error line {0} position {1}".format(p.lineno, p.lexpos))

    # def p_command_writeln(p):
    #     '''command : WRITELN plist optend'''
    #     p[0] = ('WRITELN', p[2], p[3])
    #
    # def p_command_write_bad(p):
    #     '''command : WRITE error'''
    #     p[0] = "MALFORMED WRITE STATEMENT"
    #
    # def p_command_writlne_bad(p):
    #     '''command : WRITELN error'''
    #     p[0] = "MALFORMED WRITELN STATEMENT"
    #
    # def p_expr_binary(p):
    #     '''expr : expr PLUS expr
    #             | expr MINUS expr
    #             | expr TIMES expr
    #             | expr DIVIDE expr
    #             | expr POWER expr'''
    #
    #     p[0] = ('BINOP', p[2], p[1], p[3])

    def __init__(self):
        self._lexer = DeftPascalLexer()
        self._parser = yacc.yacc(module=self)
        self._symbol_table = SymbolTable()
        self._context = 0
        self._stack_constants = []
        self._stack_variables = []
        self._stack_operands = []
        self._stack_scope =[]

    def compile(self, input_string):
        return self._parser.parse(input_string, lexer=self._lexer.get_lexer())


