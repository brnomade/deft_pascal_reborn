from lark import Tree, Token, UnexpectedToken, UnexpectedCharacters
from deft_pascal_parser_3 import DeftPascalParser
from symbol_table import SymbolTable, Constant, Variable
from abstract_emiter import CEmitter

import logging
logging.basicConfig(level=logging.DEBUG)


class DeftPascalCompiler:

    def __init__(self):
        self._parser = DeftPascalParser()
        self._symbol_table = SymbolTable()

        self._context = 0

        self._stack_constants = []
        self._stack_variables = []
        self._stack_operands = []
        self._stack_scope = []

        self._actions = {"PROGRAM_HEADING": self._action_0,
                         "RESERVED_STRUCTURE_BEGIN": self._action_1,
                         "CONSTANT_DEFINITION_PART": self._action_2,
                         "VARIABLE_DECLARATION_PART": self._action_3,
                         "LABEL_DECLARATION_PART": self._action_4,
                         "RESERVED_STRUCTURE_END": self._action_5,
                         "ASSIGNMENT_STATEMENT": self._action_6
                         }

        self._emitter = None

    @staticmethod
    def exception_raiser(exception):
        raise exception

    def check_syntax(self, input_program):
        tree = None
        try:
            tree = self._parser.parse(input_program)
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
                    action_number = action_to_call.__name__.split("_")[-1]
                except KeyError:
                    print("action '{0}' not yet implemented".format(i.data.upper()))
                else:
                    action_to_call(action_number, i.children)
            elif isinstance(i, Token):
                try:
                    action_name = i.type.upper()
                    action_to_call = self._actions[action_name]
                    action_number = action_to_call.__name__.split("_")[-1]
                except KeyError:
                    print("action '{0}' not yet implemented".format(i.type.upper()))
                else:
                    action_to_call(action_number, i)
            else:
                print('Error')
        self._emitter.write_file()

    def _action_0(self, my_number, input_list):
        """
        process PROGRAM
        """
        # print(input_list)
        if input_list[0].value.upper() == 'PROGRAM':
            identifier = input_list[1].value
            self._stack_scope.append((identifier, 0))
            context_label = self._stack_scope[-1][0]
            context_level = self._stack_scope[-1][1]
            self._symbol_table.append(Constant('TRUE', context_label, context_level, 'true', 'CONSTANT_TRUE'))
            self._symbol_table.append(Constant('FALSE', context_label, context_level, 'false', 'CONSTANT_FALSE'))
            self._emitter = CEmitter(identifier)
            self._emitter.emit_action_0()
            print("[{0}] {1} : '{2}' - stack: {3} {4} {5}".format(my_number,
                                                                  "program declared",
                                                                  identifier,
                                                                  self._stack_constants,
                                                                  self._symbol_table,
                                                                  self._stack_scope))
        if len(input_list) > 2:
            print("[{0}] {1} : variables detected - all will be ignored".format(my_number, "program declared"))

    def _action_1(self, my_number, input_token):
        """
        process RESERVED_STRUCTURE_BEGIN
        """
        # print(input_list)
        if input_token.value.upper() == "BEGIN":
            self._emitter.emit_action_1()
            print("[{0}] {1} : stack: {2} {3} {4}".format(my_number,
                                                          input_token.value.upper(),
                                                          self._stack_constants,
                                                          self._symbol_table,
                                                          self._stack_scope))
        else:
            print("[{0}] - incorrect declaration".format(my_number))

    def _action_2(self, my_number, input_list):
        """
        process CONSTANT_DEFINITION_PART
        """
        # print(input_list)
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
                    self._emitter.emit_action_2(a_symbol)
                    print("[{0}] {1} : '{2}' - stack: {3} {4} {5}".format(my_number,
                                                                          "constant declared",
                                                                          identifier,
                                                                          self._stack_constants,
                                                                          self._symbol_table,
                                                                          self._stack_scope))

        else:
            print("[{0}] - incorrect declaration".format(my_number))

    def _action_3(self, my_number, input_list):
        """
        process VARIABLE_DECLARATION_PART
        """
        # print(input_list)
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
                        self._emitter.emit_action_3(a_symbol)
                        print("[{0}] {1} : '{2}' - {3}".format(my_number,
                                                               "variable declared",
                                                               identifier,
                                                               a_symbol))
        else:
            print("[{0}] - incorrect declaration".format(my_number))

    def _action_4(self, my_number, input_list):
        """
        process LABEL_DECLARATION_PART
        """
        # print(input_list)
        if input_list[0].value.upper() == "LABEL":
            print("[{0}] {1} : all will be ignored".format(my_number, "labels declared"))
        else:
            print("[{0}] - incorrect declaration".format(my_number))

    def _action_5(self, my_number, input_token):
        """
        process END
        """
        # print(input_list)
        if input_token.value.upper() == 'END':
            self._emitter.emit_action_5()
            print("[{0}] {1} : stack: {2} {3} {4}".format(my_number,
                                                          input_token.value.upper(),
                                                          self._stack_constants,
                                                          self._symbol_table,
                                                          self._stack_scope))
        else:
            print("[{0}] - incorrect declaration".format(my_number))

    def _action_6(self, my_number, token_list):
        # print(token_list)
        if len(token_list) == 3 and token_list[1].type.upper() == 'OPERATOR_ASSIGNMENT':
            # check variable exists
            token = token_list[0]
            identifier = token.value if token.type == "IDENTIFIER" else self.exception_raiser(UnexpectedToken)
            context_label = self._stack_scope[-1][0]
            context_level = self._stack_scope[-1][1]
            a_variable = Variable(identifier, context_label, context_level, None, None)
            # scenarios:
            # - identifier not declared
            # - identifier declared on same scope
            # - identifier declared on a lower scope
            if self._symbol_table.has_equal(a_variable, equal_type=True, equal_level=True, equal_name=True):
                a_variable = self._symbol_table.get(a_variable)
            elif self._symbol_table.has_equal(a_variable, equal_type=True, equal_level=False, equal_name=True):
                a_variable = self._symbol_table.get_from_lower_scope(a_variable)
            else:
                msg = "[{0}] {1} : Error - assignment to undeclared variable : stack: {2} {3} {4}"
                print(msg.format(my_number,
                      token.value.upper(),
                      self._stack_constants,
                      self._symbol_table,
                      self._stack_scope))
            # check what is being assigned is of acceptable type
            token = token_list[2]
            context_label = self._stack_scope[-1][0]
            context_level = self._stack_scope[-1][1]
            a_constant = Constant(token.value, context_label, context_level, token.value, token.type)
            valid_types = ["NUMBER_DECIMAL", "NUMBER_BINARY", "NUMBER_OCTAL", "NUMBER_HEXADECIMAL",
                           "CHARACTER", "STRING", "CONSTANT_TRUE", "CONSTANT_FALSE", "NUMBER_REAL"
                           ]
            if a_constant.type not in valid_types:
                msg = "[{0}] {1} : Error - unexpected variable type : stack: {2} {3} {4}"
                print(msg.format(my_number,
                                 a_constant.type.upper(),
                                 self._stack_constants,
                                 self._symbol_table,
                                 self._stack_scope))
            # check variable and constant are of compatible types
            if a_variable.type == "REAL" and a_constant.type.upper() == "NUMBER_REAL":
                self._emitter.emit_action_6(a_variable, a_constant)
                print("[{0}] {1} : stack: {2} {3} {4}".format(my_number,
                                                              token_list[0].value.upper(),
                                                              self._stack_constants,
                                                              self._symbol_table,
                                                              self._stack_scope))
            elif a_variable.type in ["INTEGER", "WORD", "BYTE"] and a_constant.type.upper() in ["NUMBER_DECIMAL", "NUMBER_BINARY", "NUMBER_OCTAL", "NUMBER_HEXADECIMAL"]:
                self._emitter.emit_action_6(a_variable, a_constant)
                print("[{0}] {1} : stack: {2} {3} {4}".format(my_number,
                                                              token_list[1].value.upper(),
                                                              self._stack_constants,
                                                              self._symbol_table,
                                                              self._stack_scope))
            elif a_variable.type == "BOOLEAN" and a_constant.type.upper() in ["CONSTANT_TRUE", "CONSTANT_FALSE"]:
                if self._symbol_table.has_equal(a_constant, equal_type=True, equal_level=True, equal_name=True):
                    a_constant = self._symbol_table.get(a_constant)
                elif self._symbol_table.has_equal(a_constant, equal_type=True, equal_level=False, equal_name=True):
                    a_constant = self._symbol_table.get_from_lower_scope(a_constant)
                else:
                    msg = "[{0}] {1} : Error - use of undeclared boolean constant : stack: {2} {3} {4}"
                    print(msg.format(my_number,
                          a_constant.value.upper(),
                          self._stack_constants,
                          self._symbol_table,
                          self._stack_scope))
                self._emitter.emit_action_6(a_variable, a_constant)
                print("[{0}] {1} : stack: {2} {3} {4}".format(my_number,
                                                              token_list[1].value.upper(),
                                                              self._stack_constants,
                                                              self._symbol_table,
                                                              self._stack_scope))
            elif a_variable.type in ["STRING", "TEXT"] and a_constant.type.upper() in ["CHARACTER", "STRING"]:
                self._emitter.emit_action_6(a_variable, a_constant)
                print("[{0}] {1} : stack: {2} {3} {4}".format(my_number,
                                                              token_list[1].value.upper(),
                                                              self._stack_constants,
                                                              self._symbol_table,
                                                              self._stack_scope))
            elif a_variable.type == "CHAR" and a_constant.type.upper() == "CHARACTER":
                self._emitter.emit_action_6(a_variable, a_constant)
                print("[{0}] {1} : stack: {2} {3} {4}".format(my_number,
                                                              token_list[1].value.upper(),
                                                              self._stack_constants,
                                                              self._symbol_table,
                                                              self._stack_scope))
            else:
                msg = "[{0}] {1} <- {2} : Error - assignment of incorrect data type : stack: {3} {4} {5}"
                print(msg.format(my_number,
                                 a_variable.type,
                                 token.type.upper(),
                                 self._stack_constants,
                                 self._symbol_table,
                                 self._stack_scope))
        else:
           print("[{0}] - incorrect declaration".format(my_number))
