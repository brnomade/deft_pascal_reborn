from lark import Tree, Token, UnexpectedToken, UnexpectedCharacters
from deft_pascal_parser_3 import DeftPascalParser
from symbol_table import SymbolTable, Constant, Variable

import logging
logging.basicConfig(level=logging.DEBUG)


class DeftPascalCompiler:

    def __init__(self):
        self._dp = DeftPascalParser()
        self._symbol_table = SymbolTable()
        self._context = 0
        self._stack_constants = []
        self._stack_variables = []
        self._stack_operands = []
        self._stack_scope = []


    def check_syntax(self, input_program):
        tree = None
        try:
            tree = self._dp.compile(input_program)
        except UnexpectedToken as error:
            print('ERROR 1 - {0}'.format(error))
        except UnexpectedCharacters as error:
            print('ERROR 2 - {0}'.format(error))
        return tree


    def compile(self, ast):
        for i in ast.children:
            if isinstance(i, Tree):
                if i.data.upper() == "PROGRAM_HEADING":
                    self.action_0(i.children)
                elif i.data.upper() == "CONSTANT_DEFINITION_PART":
                    self.action_1(i.children)
                else:
                    print('{0} - action not yet implemented'.format(i.data))
            elif isinstance(i, Token):
                if i.type == 'DOT':
                    print("DOT - not sure what to do")
                else:
                    print('{0} - action not yet implemented'.format(i.type))
            else:
                print('Error')


    def action_0(self, input_list):
        """
        process the PROGRAM statement
        :param input_tree:
        :return: tree
        """
        #print(input_list)
        if input_list[0].value.upper() == 'PROGRAM':
            identifier = input_list[1].value
            self._stack_scope.append((identifier, 0))
            context_label = self._stack_scope[-1][0]
            context_level = self._stack_scope[-1][1]
            self._symbol_table.append(Constant('True', context_label, context_level, True, 0))
            self._symbol_table.append(Constant('False', context_label, context_level, False, 0))
            print("[{0}] {1} : '{2}' - stack: {3} {4} {5}".format("1",
                                                                  "program declared",
                                                                  identifier,
                                                                  self._stack_constants,
                                                                  self._symbol_table,
                                                                  self._stack_scope))

        if len(input_list) > 2:
            print('Program variables detected - all will be ignored')

    def action_1(self, input_list):
        """
        process the CONSTANT_BLOCK statement
        :param input_tree:
        :return: tree
        """
        #print(input_list)
        if input_list[0].value.upper() == 'CONST':
            input_list = input_list[1:]
            for constant_definition in input_list:
                declaration = constant_definition.children
                identifier = declaration[0].value
                value = declaration[1].value
                pascal_type = declaration[1].type
                context_label = self._stack_scope[-1][0]
                context_level = self._stack_scope[-1][1]
                a_symbol = Constant(identifier, context_label, context_level, value, pascal_type)
                # scenarios:
                # - identifier not declared
                # - identifier already declared (as a constant or a variable)
                if self._symbol_table.has_equal(a_symbol, equal_type=False):
                    print('ERROR 6 - Identifier already declared in the current scope')
                else:
                    self._symbol_table.append(a_symbol)
                    print("[{0}] {1} : '{2}' - stack: {3} {4} {5}".format("1",
                                                                          "constant declared",
                                                                          identifier,
                                                                          self._stack_constants,
                                                                          self._symbol_table,
                                                                          self._stack_scope))

        else:
            print('action_{0} - incorrect constant declaration'.format('1'))
