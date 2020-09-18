"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from obsoletes.deft_pascal_lexer import DeftPascalLexer
from components.symbol_table import SymbolTable, Constant
import ply.yacc as yacc


class DeftPascalParser_2:

    tokens = DeftPascalLexer.tokens

    precedence = ()

    def p_file(self, p):
        """
        file : program
             | module
        """
        print('p_file {0} {1}'.format(p[0], p[1]))

    def p_program(self, p):
        """
        program : program_heading SEMICOLON block DOT
        """
        print('p_program {0} {1} {2} {3} {4}'.format(p[0], p[1], p[2], p[3], p[4]))


    def p_module(self, p):
        """
        module : IDENTIFIER
        """
        print('p_module {0}'.format(self._stack_scope))


    def p_program_heading(self, p):
        """
        program_heading : RESERVED_STRUCTURE_PROGRAM IDENTIFIER
                        | RESERVED_STRUCTURE_PROGRAM IDENTIFIER LEFT_PARENTHESES identifier_list RIGHT_PARENTHESES
        """
        self._stack_scope.append((p[2], 0))
        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]
        self._symbol_table.append(Constant('True', context_label, context_level, True, 0))
        self._symbol_table.append(Constant('False', context_label, context_level, False, 0))
        print("p_program_heading declared '{0}' stack: {1} {2} {3}".format(p[2], self._stack_constants, self._symbol_table, self._stack_scope))

    def p_identifier_list(self, p):
        """
        identifier_list : identifier_list COMMA IDENTIFIER
                        | IDENTIFIER
        """
        print('p_identifier_list {0}'.format(self._stack_scope))

    def p_block(self, p):
        """
        block : constant_definition_part statement_part
              |
        """
        print('p_block {0}'.format(self._stack_scope))

    def p_constant_definition_part(self, p):
        """
        constant_definition_part : RESERVED_DECLARATION_CONST constant_list
                                 |
        """
        # print('p_constant_definition_part {0}'.format(self._stack_scope))

    def p_constant_list(self, p):
        """
        constant_list : constant_list constant_definition
                      | constant_definition
        """
        # print('p_constant_list {0}'.format(self._stack_scope))

    def p_constant_definition(self, p):
        """
        constant_definition : IDENTIFIER OPERATOR_EQUAL_TO constant_expression SEMICOLON
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
            print("p_constant_definition - constant declared '{0}' stack: {1} {2}".format(p[1], self._stack_constants, self._symbol_table))

    def p_constant_expression(self, p):
        """
        constant_expression : NUMBER_REAL
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
        print("p_cexpression - constant valued : '{0}' stack: {1}".format(p[1], self._stack_constants))

    def p_statement_part(self, p):
        """
        statement_part : compound_statement
        """
        print('statement_part {0}'.format(self._stack_scope))

    def p_compound_statement(self, p):
        """
        compound_statement : RESERVED_STRUCTURE_BEGIN RESERVED_STRUCTURE_END
        """
        print('compound_statement {0}'.format(self._stack_scope))

    def p_error(self, p):
        print(p)
        print("Syntax error line {0} position {1}".format(p.lineno, p.lexpos))

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


