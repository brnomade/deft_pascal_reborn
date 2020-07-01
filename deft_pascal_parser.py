from deft_pascal_lexer import DeftPascalLexer
import ply.yacc as yacc


class DeftPascalParser:

    tokens = DeftPascalLexer.tokens

    def p_pascal_program(self, p):
        """
        program : program_header declarations compound_statement DOT
        """
        print('p_pascal_program')

    def p_program_header(self, p):
        """
        program_header : RESERVED_STRUCTURE_PROGRAM IDENTIFIER SEMICOLON
                       | RESERVED_STRUCTURE_PROGRAM IDENTIFIER LEFT_PARENTHESES id_list RIGHT_PARENTHESES SEMICOLON
        """
        print('p_program_header')

    def p_id_list(self, p):
        """
        id_list : IDENTIFIER
                | IDENTIFIER COMMA id_list
        """
        print('p_id_list')

    def p_declarations(self, p):
        """
        declarations : constant_definitions variable_declarations
        """
        print('p_declarations')

    def p_variable_declarations(self, p):
        """
        variable_declarations : RESERVED_DECLARATION_VAR variable_declaration_list
                              |
        """
        print('p_variable_declarations')

    def p_variable_declaration_list(self, p):
        """
        variable_declaration_list : variable_dec
                                  | variable_dec variable_declaration_list
        """
        print('p_variable_declaration_list')

    def p_variable_dec(self, p):
        """
        variable_dec : id_list COLON type_specifier SEMICOLON
        """
        print('p_variable_dec')

    def p_type_specifier(self, p):
        """
        type_specifier : IDENTIFIER
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
        print('p_type_specifier')

    def p_constant_definitions(self, p):
        """
        constant_definitions : RESERVED_DECLARATION_CONST constant_definition_list
                             |
        """
        print('p_constant_definitions')

    def p_constant_definition_list(self, p):
        """
        constant_definition_list : constant_def
                                 | constant_def constant_definition_list
        """
        print('p_constant_definition_list')

    def p_constant_def(self, p):
        """
        constant_def : IDENTIFIER OPERATOR_EQUAL_TO constant SEMICOLON
        """
        print(p.slice[0].type, p[1])

    def p_compound_statement(self, p):
        """
        compound_statement : RESERVED_STRUCTURE_BEGIN statement_list RESERVED_STRUCTURE_END
        """
        print('p_compound_statement')

    def p_statement_list(self, p):
        """
        statement_list : statement
                       | statement SEMICOLON statement_list
        """
        print(p.slice[0].type, p[1])

    def p_statement(self, p):
        """
        statement : compound_statement
                  | assignment_statement
                  | procedure_call
                  | write_call
                  | writeln_call
                  |
        """
        #print(p.slice[0].type, p[1])
        print('p_statement')

    def p_write_call(self, p):
        """
        write_call : RESERVED_STATEMENT_WRITE actuals
        """
        print('p_write_call')

    def p_writeln_call(self, p):
        """
        writeln_call : RESERVED_STATEMENT_WRITELN actuals
        """
        print('p_writeln_call')

    def p_procedure_call(self, p):
        """
        procedure_call : IDENTIFIER actuals
        """
        print('p_procedure_call')

    def p_actuals(self, p):
        """
        actuals : LEFT_PARENTHESES expression_list RIGHT_PARENTHESES
                |
        """
        print('p_actuals')

    def p_expression_list(self, p):
        """
        expression_list : expression
                        | expression COMMA expression_list
        """
        print('p_expression_list')

    def p_assignment_statement(self, p):
        """
        assignment_statement : variable OPERATOR_ASSIGNMENT expression
        """
        print('p_assignment_statement')

    def p_variable(self, p):
        """
        variable : IDENTIFIER
        """
        print('p_variable')

    def p_expression(self, p):
        """
        expression : simple_expression
                   | simple_expression OPERATOR_EQUAL_TO simple_expression
                   | simple_expression OPERATOR_NOT_EQUAL_TO simple_expression
                   | simple_expression OPERATOR_LESS_THEN simple_expression
                   | simple_expression OPERATOR_LESS_OR_EQUAL_TO simple_expression
                   | simple_expression OPERATOR_GREATER_THEN simple_expression
                   | simple_expression OPERATOR_GREATER_OR_EQUAL_TO simple_expression
        """
        print('p_expression')

    def p_simple_expression(self, p):
        """
        simple_expression ::= term
                    | simple_expression OPERATOR_PLUS term
                    | simple_expression OPERATOR_MINUS term
                    | simple_expression RESERVED_OPERATOR_OR term
        """
        print('p_simple_expression')

    def p_term(self, p):
        """
        term ::= factor
         | term OPERATOR_MULTIPLY factor
         | term OPERATOR_DIVIDE factor
         | term RESERVED_OPERATOR_DIV factor
         | term RESERVED_OPERATOR_MOD factor
         | term RESERVED_OPERATOR_AND factor
        """
        print('p_term')

    def p_factor(self, p):
        """
        factor : LEFT_PARENTHESES expression RIGHT_PARENTHESES
               | OPERATOR_PLUS factor
               | OPERATOR_MINUS factor
               | RESERVED_OPERATOR_NOT factor
               | constant
               | variable
        """
        print('p_factor')

    def p_constant(self, p):
        """
        constant : NUMBER_REAL
                 | NUMBER_DECIMAL
                 | NUMBER_BINARY
                 | NUMBER_OCTAL
                 | NUMBER_HEXADECIMAL
                 | CHARACTER
                 | STRING
        """
        print(p.slice[0].type, p[1])



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

    def compile(self, input_string):
        return self._parser.parse(input_string, lexer=self._lexer.get_lexer())


