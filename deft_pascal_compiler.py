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

        self._actions = {"PROGRAM_HEADING": self._action_0,
                         "CONSTANT_DEFINITION_PART": self._action_1,
                         "VARIABLE_DECLARATION_PART": self._action_2,
                         "LABEL_DECLARATION_PART": self._action_3,
                         "assignment_statement": self._action_4
                         }


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
                try:
                    action_name = i.data.upper()
                    action_to_call = self._actions[action_name]
                except KeyError:
                    print("action '{0}' not yet implemented".format(i.data.upper()))
                else:
                    action_to_call(i.children)
            elif isinstance(i, Token):
                if i.type == 'DOT':
                    print("DOT - not sure what to do")
                else:
                    print('{0} - action not yet implemented'.format(i.type))
            else:
                print('Error')

    def _action_0(self, input_list):
        """
        process PROGRAM
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
            print("[{0}] {1} : '{2}' - stack: {3} {4} {5}".format("0",
                                                                  "program declared",
                                                                  identifier,
                                                                  self._stack_constants,
                                                                  self._symbol_table,
                                                                  self._stack_scope))

        if len(input_list) > 2:
            print("[{0}] {1} : variables detected - all will be ignored".format("0", "program declared"))

    def _action_1(self, input_list):
        """
        process CONSTANT_DEFINITION_PART
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
                data_type = declaration[1].type
                # TODO: the data_type needs to be adjusted to a real data_type
                context_label = self._stack_scope[-1][0]
                context_level = self._stack_scope[-1][1]
                a_symbol = Constant(identifier, context_label, context_level, value, data_type)
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
            print("[{0}] - incorrect constant declaration".format('1'))

    def _action_2(self, input_list):
        """
        process VARIABLE_DECLARATION_PART
        :param input_tree:
        :return: tree
        """
        #print(input_list)
        if input_list[0].value.upper() == 'VAR':
            input_list = input_list[1:]
            for variable_declaration in input_list:
                data_type = variable_declaration.children.pop().value
                for token in variable_declaration.children:
                    identifier = token.value
                    context_label = self._stack_scope[-1][0]
                    context_level = self._stack_scope[-1][1]
                    a_symbol = Variable(identifier, context_label, context_level, data_type, None)
                    # scenarios:
                    # - identifier not declared
                    # - identifier already declared (as a constant or a variable)
                    if self._symbol_table.has_equal(a_symbol, equal_type=False):
                        print('ERROR 2 - Identifier already declared in the current scope')
                    else:
                        self._symbol_table.append(a_symbol)
                        self._stack_variables.append(a_symbol)
                        print("[{0}] {1} : '{2}' - stack: {3} {4} {5}".format("2",
                                                                              "variable declared",
                                                                              identifier,
                                                                              self._stack_constants,
                                                                              self._symbol_table,
                                                                              self._stack_scope))
        else:
            print("[{0}] - incorrect variable declaration".format('2'))

    def _action_3(self, input_list):
        """
        process LABEL_DECLARATION_PART
        :param
        :return:
        """
        #print(input_list)
        if input_list[0].value.upper() == "LABEL":
            print("[{0}] {1} : all will be ignored".format("3", "labels declared"))
        else:
            print("[{0}] - incorrect label declaration".format('3'))

    def _action_4(self, input_list):
        """
        process
        :param
        :return:
        """
        print(input_list)

