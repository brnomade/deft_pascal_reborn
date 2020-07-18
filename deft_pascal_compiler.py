from lark import Tree, Token, UnexpectedToken, UnexpectedCharacters
from deft_pascal_parser_3 import DeftPascalParser
from symbol_table import SymbolTable, BaseSymbol, Constant, Variable, Operator
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
                         "ASSIGNMENT_STATEMENT": self._action_6,
                         "REPEAT_STATEMENT": self._action_7,
                         "BOOLEAN_EXPRESSION": self._action_8
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

    def _compile_tree(self, a_tree):
        try:
            action_name = a_tree.data.upper()
            action_to_call = self._actions[action_name]
            action_number = action_to_call.__name__.split("_")[-1]
        except KeyError:
            print("action '{0}' not yet implemented".format(a_tree.data.upper()))
        else:
            action_to_call(action_number, a_tree.children)

    def _compile_token(self, a_token):
        try:
            action_name = a_token.type.upper()
            action_to_call = self._actions[action_name]
            action_number = action_to_call.__name__.split("_")[-1]
        except KeyError:
            print("action '{0}' not yet implemented".format(a_token.type.upper()))
        else:
            action_to_call(action_number, a_token)

    def _internal_compile(self, ast):
        if isinstance(ast, Tree):
            if len(ast.children) > 0:
                self._compile_tree(ast)
        elif isinstance(ast, Token):
            self._compile_token(ast)
        else:
            raise TypeError('Error - unknown AST object {0}'.format(ast))

    def compile(self, ast):
        for i in ast.children:
            self._internal_compile(i)
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
            self._symbol_table.append(Constant('TRUE', context_label, context_level, 'CONSTANT_TRUE', 'true'))
            self._symbol_table.append(Constant('FALSE', context_label, context_level, 'CONSTANT_FALSE', 'false'))
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
                a_symbol = Constant(identifier, context_label, context_level, data_type,  value)
                # scenarios:
                # - identifier not declared
                # - identifier already declared (as a constant or a variable)
                if self._symbol_table.has_equal(a_symbol, equal_type=False):
                    print('ERROR 6 - Identifier already declared in the current scope')
                else:
                    self._symbol_table.append(a_symbol)
                    self._emitter.emit_action_2(a_symbol)
                    print("[{0}] {1} : {2}".format(my_number, "constant declared", a_symbol))

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
                    a_symbol = Variable(identifier, context_label, context_level, data_type, identifier)
                    # scenarios:
                    # - identifier not declared
                    # - identifier already declared (as a constant or a variable)
                    if self._symbol_table.has_equal(a_symbol, equal_type=False):
                        print('ERROR 2 - Identifier already declared in the current scope')
                    else:
                        self._symbol_table.append(a_symbol)
                        self._stack_variables.append(a_symbol)
                        self._emitter.emit_action_3(a_symbol)
                        print("[{0}] {1} : {2}".format(my_number, "variable declared", a_symbol))
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

    def _check_variable_exists( self, my_number, a_variable ):
        # check variable exists
        # scenarios:
        # - identifier not declared
        # - identifier declared on same scope
        # - identifier declared on a lower scope

        if self._symbol_table.has_equal(a_variable, equal_class=True, equal_type=False, equal_level=True, equal_name=True):
            a_variable = self._symbol_table.get(a_variable)
        elif self._symbol_table.has_equal(a_variable, equal_class=True, equal_type=False, equal_level=False, equal_name=True):
            a_variable = self._symbol_table.get_from_lower_scope(a_variable)
        else:
            msg = "[{0}] {1} : Error - assignment to undeclared variable"
            print(msg.format(my_number, a_variable))
        return a_variable


    def _check_type_compatibility( self, my_number, a_variable, a_symbol ):
        # check variable and symbol are of compatible types
        type_a = a_variable.type.upper()
        type_b = a_symbol.type.upper()
        compatible = False
        #
        if a_symbol.is_equal(a_variable):
            compatible = True
        elif type_a == "REAL":
            compatible = type_b in ["SIGNED_REAL", "UNSIGNED_REAL"]
        elif type_a in ["INTEGER", "WORD", "BYTE"]:
            compatible = type_b in ["SIGNED_DECIMAL", "UNSIGNED_DECIMAL", "NUMBER_BINARY", "NUMBER_OCTAL",
                                    "NUMBER_HEXADECIMAL"]
        elif type_a == "BOOLEAN":
            compatible = type_b in ["CONSTANT_TRUE", "CONSTANT_FALSE"]
        elif type_a in ["STRING", "TEXT"]:
            compatible = type_b in ["CHARACTER", "STRING"]
        elif type_a == "CHAR":
            compatible = type_b == "CHARACTER"
        #
        if not compatible:
            msg = "[{0}] Error - type violation in assignment: {1} {2} "
            print(msg.format(my_number, a_variable, a_symbol))
        #
        return compatible


    def _action_6(self, my_number, token_list):
        # print(token_list)
        if token_list[1].type.upper() == 'OPERATOR_ASSIGNMENT':

            context_label = self._stack_scope[-1][0]
            context_level = self._stack_scope[-1][1]

            # check variable exists

            token = token_list[0]
            identifier = token.value if token.type == "IDENTIFIER" else self.exception_raiser(UnexpectedToken)
            a_variable = Variable(identifier, context_label, context_level)
            a_variable = self._check_variable_exists(my_number, a_variable)

            self._emitter.emit_action_6(a_variable)

            # iterate over assignment list and check type compatibility

            #token_list = token_list[1:]

            for token in token_list[1:]:
                #print(token.type, token.value)

                if token.type in ["CONSTANT_TRUE", "CONSTANT_FALSE"]:

                    a_symbol = Constant(token.value, context_label, context_level, token.type, token.value)
                    if self._symbol_table.has_equal(a_symbol, equal_type=True, equal_level=True, equal_name=True):
                        a_symbol = self._symbol_table.get(a_symbol)
                    elif self._symbol_table.has_equal(a_symbol, equal_type=True, equal_level=False, equal_name=True):
                        a_symbol = self._symbol_table.get_from_lower_scope(a_symbol)
                    else:
                        msg = "[{0}] : Error - undeclared boolean system constant {1}"
                        print(msg.format(my_number, a_symbol))

                    self._check_type_compatibility(my_number, a_variable, a_symbol)

                elif token.type == "IDENTIFIER":

                    a_symbol = Variable(token.value, context_label, context_level)
                    a_symbol = self._check_variable_exists(my_number, a_symbol)
                    self._check_type_compatibility(my_number, a_variable, a_symbol)
                    #print("variable -> {0}".format(a_symbol))

                elif token.type in ["UNSIGNED_DECIMAL", "SIGNED_DECIMAL", "NUMBER_BINARY", "NUMBER_OCTAL",
                                     "NUMBER_HEXADECIMAL", "CHARACTER", "STRING", "CONSTANT_TRUE", "CONSTANT_FALSE",
                                     "UNSIGNED_REAL", "SIGNED_REAL"
                                     ]:

                    a_symbol = Constant(token.value, context_label, context_level, token.type, token.value)
                    self._check_type_compatibility(my_number, a_variable, a_symbol)

                else:

                    a_symbol = BaseSymbol(token.value, context_label, context_level, token.type, token.value)
                #
                #if token.type not in ["OPERATOR_ASSIGNMENT"]:

                #    self._action_6_check_type_compatibility(my_number, a_variable, a_symbol)
                #
                self._emitter.emit_action_6(a_symbol)
            self._emitter.emit_action_6_finish()
            print("[{0}] assignment : {1}".format(my_number, a_variable))
        else:
            print("[{0} incorrect declaration {1}] ".format(my_number, token_list))

    def _action_7(self, my_number, token_list):
        if token_list[0].type.upper() == 'RESERVED_STATEMENT_REPEAT':

            context_label = self._stack_scope[-1][0]
            context_level = self._stack_scope[-1][1]

            self._emitter.emit_action_7(1)
            print("[{0}] repeat".format(my_number))

            self._internal_compile(token_list[1])

            self._emitter.emit_action_7(2)
            print("[{0}] until".format(my_number))

            self._internal_compile(token_list[3])

            self._emitter.emit_action_7(3)
        else:
            print("[{0} incorrect declaration {1}] ".format(my_number, token_list))

    def _action_8(self, my_number, token_list):
        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]

        for token in token_list:
            print(token.type, token.value)

            if token.type in ["CONSTANT_TRUE", "CONSTANT_FALSE"]:

                a_symbol = Constant(token.value, context_label, context_level, token.type, token.value)
                if self._symbol_table.has_equal(a_symbol, equal_type=True, equal_level=True, equal_name=True):
                    a_symbol = self._symbol_table.get(a_symbol)
                elif self._symbol_table.has_equal(a_symbol, equal_type=True, equal_level=False, equal_name=True):
                    a_symbol = self._symbol_table.get_from_lower_scope(a_symbol)
                else:
                    msg = "[{0}] : Error - undeclared boolean system constant {1}"
                    print(msg.format(my_number, a_symbol))

            elif token.type == "IDENTIFIER":

                a_symbol = Variable(token.value, context_label, context_level)
                a_symbol = self._check_variable_exists(my_number, a_symbol)

            elif token.type in ["UNSIGNED_DECIMAL", "SIGNED_DECIMAL", "NUMBER_BINARY", "NUMBER_OCTAL",
                                "NUMBER_HEXADECIMAL", "CHARACTER", "STRING", "CONSTANT_TRUE", "CONSTANT_FALSE",
                                "UNSIGNED_REAL", "SIGNED_REAL"
                                ]:

                a_symbol = Constant(token.value, context_label, context_level, token.type, token.value)

            else:

                a_symbol = BaseSymbol(token.value, context_label, context_level, token.type, token.value)

            self._emitter.emit_action_8(a_symbol)
        print("[{0}] boolean expression".format(my_number))




