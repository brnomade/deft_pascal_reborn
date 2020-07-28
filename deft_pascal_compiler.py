from lark import Tree, Token, UnexpectedToken, UnexpectedCharacters
from deft_pascal_parser_3 import DeftPascalParser
from symbol_table import SymbolTable, BaseSymbol, Constant, Identifier, Operator, PointerIdentifier, BooleanConstant, NilConstant
from intermediate_code import IntermediateCode
from compiler_utils import check_type_compatibility
import logging
from logging import ERROR, WARNING, INFO

logger = logging.getLogger(__name__)


class DeftPascalCompiler:

    def __init__(self):
        self._parser = DeftPascalParser()
        self._symbol_table = SymbolTable()

        # self._emiter = None
        self._stack_emiter = []

        self._ic = IntermediateCode()

        self._context = 0

        self._stack_expression = []
        self._stack_variables = []
        self._stack_scope = []

        self._actions = {"PROGRAM_HEADING": self._action_0,
                         "RESERVED_STRUCTURE_BEGIN": self._action_1,
                         "CONSTANT_DEFINITION_PART": self._action_2,
                         "VARIABLE_DECLARATION_PART": self._action_3,
                         "LABEL_DECLARATION_PART": self._action_4,
                         "RESERVED_STRUCTURE_END": self._action_5,
                         "ASSIGNMENT_STATEMENT": self._action_6,
                         "EXPRESSION": self._action_7,
                         "REPEAT_STATEMENT": self._action_8,
                         "CLOSED_FOR_STATEMENT" : self._action_10,
                         }
# "BOOLEAN_EXPRESSION": self._action_9,
        #

        self._error_list = []


    def check_syntax(self, input_program):
        tree = None
        try:
            tree = self._parser.parse(input_program)
        except UnexpectedToken as error:
            self._log(ERROR, '1 - {0}'.format(error))
        except UnexpectedCharacters as error:
            self._log(ERROR, '2 - {0}'.format(error))
        return tree

    def compile(self, ast, intermediate=False, generate=False):
        self._error_list = []
        #
        for i in ast.children:
            self._internal_compile(i)
        #
        if intermediate:
            logger.info(self._ic)
        #
        if generate:
            self._ic.generate()
        #
        return self._error_list

    @staticmethod
    def _exception_raiser(exception):
        raise exception

    def _log(self, log_type=INFO, log_info=""):
        if log_type == ERROR:
            msg = "{0} - {1}".format("ERROR", log_info)
            self._error_list.append(msg)
            logger.error(log_info)
        elif log_type == WARNING:
            logger.warning(log_info)
        else:
            logger.info(log_info)

    def _compile_tree(self, a_tree):
        try:
            action_name = a_tree.data.upper()
            action_to_call = self._actions[action_name]
            action_number = int(action_to_call.__name__.split("_")[-1])
        except KeyError:
            self._log(ERROR, "action '{0}' not yet implemented".format(a_tree.data.upper()))
        else:
            action_to_call(action_number, action_name, a_tree.children)

    def _compile_token(self, a_token):
        try:
            action_name = a_token.type.upper()
            action_to_call = self._actions[action_name]
            action_number = int(action_to_call.__name__.split("_")[-1])
        except KeyError:
            self._log(ERROR, "action '{0}' not yet implemented".format(a_token.type.upper()))
        else:
            action_to_call(action_number, action_name, a_token)

    def _internal_compile(self, ast):
        if isinstance(ast, Tree):
            if len(ast.children) > 0:
                self._compile_tree(ast)
        elif isinstance(ast, Token):
            self._compile_token(ast)
        else:
            self._log(ERROR, 'Error - unknown AST object {0}'.format(ast))
            raise TypeError

    def _retrieve_global_boolean_constant(self, action_number, action_name, value):
        a_symbol = BooleanConstant.from_value(value)
        a_symbol.scope = self._stack_scope[-1][0]
        a_symbol.level = self._stack_scope[-1][1]
        if self._symbol_table.has_equal(a_symbol, equal_type=True, equal_level=False, equal_name=True):
            a_symbol = self._symbol_table.get(a_symbol)
        elif self._symbol_table.has_equal(a_symbol, equal_type=True, equal_level=False, equal_name=True):
            a_symbol = self._symbol_table.get_from_lower_scope(a_symbol)
        else:
            msg = "[{0}] {1} - undeclared boolean system constant {2}"
            self._log(ERROR, msg.format(action_number, action_name, a_symbol))
            a_symbol = None
        return a_symbol

    def _retrieve_from_symbol_table(self, action_number, action_name, a_symbol):
        # check symbol exists
        # scenarios:
        # - symbol not declared
        # - symbol declared on same scope
        # - symbol declared on a lower scope
        # returns None if seymbol not found

        if self._symbol_table.has_equal(a_symbol, equal_class=False, equal_type=False, equal_level=True, equal_name=True):
            a_symbol = self._symbol_table.get(a_symbol)
        elif self._symbol_table.has_equal(a_symbol, equal_class=False, equal_type=False, equal_level=False, equal_name=True):
            a_symbol = self._symbol_table.get_from_lower_scope(a_symbol)
        else:
            msg = "Error! [{0}] {1} - Reference to undeclared symbol {2}"
            self._log(ERROR, msg.format(action_number, action_name, a_symbol))
            a_symbol = None
        return a_symbol

    def _get_declared_variable(self, action_number, action_name, a_variable):
        # check variable exists
        # scenarios:
        # - identifier not declared
        # - identifier declared on same scope
        # - identifier declared on a lower scope

        if self._symbol_table.has_equal(a_variable, equal_class=True, equal_type=False, equal_level=True, equal_name=True):
            a_variable = self._symbol_table.get(a_variable)
        elif self._symbol_table.has_equal(a_variable, equal_class=True, equal_type=False, equal_level=False, equal_name=True):
            a_symbol = self._symbol_table.get_from_lower_scope(a_variable)
        else:
            msg = "[{0}] {1} - Reference to undeclared symbol {2}"
            self._log(ERROR, msg.format(action_number, action_name, a_variable))
            a_variable = None
        return a_variable

    def _check_type_compatibility(self, action_number, action_name, expression):
        """
        expression - is a list of tokens.
        """
        compatible = check_type_compatibility(expression)
        if not compatible:
            msg = "[{0}] {1} - type violation in expression: {2} {3} "
            self._log(ERROR, msg.format(action_number, action_name, expression, expression))
        #
        return compatible

    def _action_0(self, action_number, action_name, token_list):
        """
        process PROGRAM
        """
        identifier = token_list[1].value
        self._stack_scope.append((identifier, 0))
        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]

        self._symbol_table.append(BooleanConstant.true(context_label, context_level))
        self._symbol_table.append(BooleanConstant.false(context_label, context_level))
        self._symbol_table.append(NilConstant.nil((context_label, context_level)))

        # self._emiter = CEmitter(identifier)
        # self._emiter.emit_action_0()

        self._ic.init(action_number, action_name)
        self._ic.push(token_list[0])
        self._ic.push(token_list[1])
        self._ic.flush()

        self._log(INFO, "[{0}] {1} : '{2}' - stack: {3} {4}".format(action_number,
                                                                    action_name,
                                                                    identifier,
                                                                    self._symbol_table,
                                                                    self._stack_scope))

        if len(token_list) > 2:
            self._log(WARNING, "[{0}] {1} : variables detected - all will be ignored".format(action_number, action_name))

    def _action_1(self, action_number, action_name, input_token):
        """
        process RESERVED_STRUCTURE_BEGIN
        """
        self._ic.init(action_number, action_name)
        self._ic.push(input_token)
        self._ic.flush()

        # self._emiter.emit_action_1()
        self._log(INFO, "[{0}] {1} : stack: {2} {3}".format(action_number,
                                                            action_name,
                                                            self._symbol_table,
                                                            self._stack_scope))

    def _action_2(self, action_number, action_name, input_list):
        """
        process CONSTANT_DEFINITION_PART
        """
        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]
        self._ic.init(action_number, action_name)

        input_list = input_list[1:]
        for constant_definition in input_list:

            declaration = constant_definition.children
            # the constant definition (declaration) has 3 parts: identifier, operator and constant

            identifier = Identifier(declaration[0].value, context_label, context_level, declaration[0].type, declaration[0].value)
            operator = Operator(declaration[1].value, context_label, context_level, declaration[1].type, declaration[1].value)
            constant = Constant(declaration[2].value, context_label, context_level, declaration[2].type, declaration[2].value)
            identifier.type = constant.type
            identifier.value = constant.value

            if self._symbol_table.has_equal(identifier, equal_class=False, equal_type=False, equal_level=True, equal_name=True):
                self._log(ERROR, 'ERROR 6 - Identifier already declared in the current scope')
            else:
                self._symbol_table.append(identifier)
                # self._emiter.emit_action_2(identifier)

                self._ic.push([identifier, operator, constant])

                self._log(INFO, "[{0}] {1} : {2}".format(action_number, action_name, identifier))

        self._ic.flush()


    def _action_3(self, action_number, action_name, input_list):
        """
        input_list -> VAR [v1 v2 TYPE] [v3 TYPE] [V4 V5 ^TYPE]...
        """

        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]
        self._ic.init(action_number, action_name)

        # discard reserved word VAR
        input_list = input_list[1:]

        for variable_declaration in input_list:

            # the TYPE is always at the end of the children list. pop it out and collect the value.

            data_type = variable_declaration.children.pop().value

            # check if a pointer is being declared - if so, pop it out for emitter

            identifier_class = Identifier
            if variable_declaration.children[-1].type == "UPARROW":

                identifier_class = PointerIdentifier
                variable_declaration.children.pop()

            # check if the data_type is a type identifier
            if data_type in []

                # TODO: transforme type declaration to a compiler type
                # TODO: check if the identifier that is not a compiler type is a declared type via TYPE declaration

            # process each identifier for the given data_type

            for token in variable_declaration.children:

                a_symbol = identifier_class(token.value, context_label, context_level, data_type, token.value)

                # scenarios:
                # - identifier not declared
                # - identifier already declared

                if self._symbol_table.has_equal(a_symbol, equal_type=False):

                    msg = "[{0}] {1} :  Identifier '{2}' already declared in current scope"
                    self._log(ERROR, msg.format(action_number, action_name, a_symbol))

                else:

                    self._symbol_table.append(a_symbol)
                    # self._emiter.emit_action_3(a_symbol)
                    self._ic.push(a_symbol)
                    self._log(INFO, "[{0}] {1} : {2}".format(action_number, action_name, a_symbol))

        self._ic.flush()


    def _action_4(self, action_number, action_name, input_list):
        """
        process LABEL_DECLARATION_PART
        """
        self._log(WARNING, "[{0}] {1} - all will be ignored".format(action_number, action_name))

    def _action_5(self, action_number, action_name, input_token):
        """
        process END
        """
        # self._emiter.emit_action_5()

        self._ic.init(action_number, action_name)
        self._ic.push(input_token)
        self._ic.flush()
        self._log(INFO, "[{0}] {1} : {2}".format(action_number,
                                                 action_name,
                                                 self._symbol_table))


    def _action_6(self, action_number, action_name, token_list):
        """
        token_list -> identifier := expression
        """
        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]
        self._ic.init(action_number, action_name)

        # check identifier exists

        token = token_list[0]
        identifier = token.value if token.type == "IDENTIFIER" else self._exception_raiser(UnexpectedToken)
        a_symbol = Identifier(identifier, context_label, context_level)
        a_symbol = self._retrieve_from_symbol_table(action_number, action_name, a_symbol)

        self._ic.push(a_symbol)

        # prepare stacks to process the expression

        # self._stack_variables = []
        #self._stack_variables.append(a_symbol)

        self._stack_expression = []
        self._stack_expression.append(a_symbol)

        # consume the operator :=

        token = token_list[1]
        operator = Operator(token.value, context_label, context_level, token.type, token.value)
        self._ic.push(operator)

        self._stack_expression.append(operator)

        # process the expression

        self._internal_compile(token_list[2])

        # perform type checking

        if not check_type_compatibility(self._stack_expression):
            self._log(ERROR, "[{0}] {1} : incompatible types detected {2}".format(action_number, action_name, self._stack_expression))
        else:
            self._log(INFO, "[{0}] {1} : {2}".format(action_number, action_name, self._stack_expression))

        # emit everything
        # self._emiter.emit_action_6(self._stack_emiter)
        self._ic.flush()
        #self._stack_variables = []


    def _action_7(self, action_number, action_name, token_list):

        # process expressions in assignments
        # this is called from other actions and therefore it does not create its own action on the intermediate code
        # it also does not need to flush the intermediate code. this will be done in another action.

        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]

        for token in token_list:
            if isinstance(token, Tree):

                self._internal_compile(token)

            elif isinstance(token, Token):

                if token.type in ["CONSTANT_TRUE", "CONSTANT_FALSE"]:

                    a_symbol = self._retrieve_global_boolean_constant(action_number, action_name, token.value)

                elif token.type in ["UNSIGNED_DECIMAL", "SIGNED_DECIMAL", "NUMBER_BINARY", "NUMBER_OCTAL",
                                    "NUMBER_HEXADECIMAL", "CHARACTER", "STRING", "UNSIGNED_REAL", "SIGNED_REAL"
                                    ]:

                    a_symbol = Constant(token.value, context_label, context_level, token.type, token.value)

                elif token.type == "IDENTIFIER":

                    a_symbol = Identifier(token.value, context_label, context_level)
                    a_symbol = self._get_declared_variable(action_number, action_name, a_symbol)

                else:

                    a_symbol = BaseSymbol(token.value, context_label, context_level, token.type, token.value)
                    if a_symbol.is_operator():
                        a_symbol = Operator(token.value, context_label, context_level, token.type, token.value)

                # handling a boolean_expression used in repeat, while and if statements
                #if len(self._stack_variables) == 0:
                #    start_symbol = self._retrieve_global_boolean_constant(action_number, action_name, 'true')
                #else:
                #    start_symbol = self._stack_variables[-1]

                #self._check_type_compatibility(action_number, action_name, start_symbol, a_symbol)

                # self._stack_emiter.append(a_symbol)
                self._stack_expression.append(a_symbol)
                self._ic.push(a_symbol)

            else:

                self._exception_raiser(KeyError)


    def _action_8(self, action_number, action_name, token_list):
        """
            REPEAT
            assignment_statement
              v1
              :=
              expression	1
            assignment_statement
              v1
              :=
              expression	1
            UNTIL
            expression	True
        """
        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]
        self._ic.init(action_number, action_name)

        # process REPEAT
        self._ic.push(token_list.pop(0))
        self._log(INFO, "[{0}] {1} : REPEAT".format(action_number, action_name))
        self._ic.flush()

        while True:
            token = token_list.pop(0)
            if isinstance(token, Token) and token.type == "RESERVED_STATEMENT_UNTIL":
                self._ic.init(action_number, action_name)
                self._ic.push(token)
                self._log(INFO, "[{0}] {1} : UNTIL".format(action_number, action_name))
                break
            else:
                self._internal_compile(token)

        # process expression after UNTIL
        # TODO: Here a list with all tokens from the expression need to be returned so that type check can be done.
        # TODO: Must call _check_type_compatibility
        self._internal_compile(token_list.pop())
        self._ic.flush()

    def _action_9(self, action_number, action_name, token_list):

        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]

        stack_expression = []

        token_list = token_list.children
        for token in token_list:
            # print(token.type, token.value)

            if token.type in ["CONSTANT_TRUE", "CONSTANT_FALSE"]:

                a_symbol = self._retrieve_global_boolean_constant(action_number, action_name, token.value)
                stack_expression.append(a_symbol)

            elif token.type == "IDENTIFIER":

                a_symbol = Identifier(token.value, context_label, context_level)
                a_symbol = self._get_declared_variable(action_number, action_name, a_symbol)
                stack_expression.append(a_symbol)

            elif token.type in ["UNSIGNED_DECIMAL", "SIGNED_DECIMAL", "NUMBER_BINARY", "NUMBER_OCTAL",
                                "NUMBER_HEXADECIMAL", "CHARACTER", "STRING", "CONSTANT_TRUE", "CONSTANT_FALSE",
                                "UNSIGNED_REAL", "SIGNED_REAL"
                                ]:

                a_symbol = Constant(token.value, context_label, context_level, token.type, token.value)
                stack_expression.append(a_symbol)

            else:

                a_symbol = BaseSymbol(token.value, context_label, context_level, token.type, token.value)

            if a_symbol:
                # self._emiter.emit_action_9(a_symbol)
                pass

        for i in range(0, len(stack_expression) - 1):
            self._check_type_compatibility(action_number, action_name, stack_expression[i], stack_expression[i+1])

        self._log(INFO, "[{0}] {1} : {2}".format(action_number, action_name, stack_expression))

    def _action_10(self, action_number, action_name, token_list):
        """
        token_list will have: FOR identifier := expression TO/DOWNTO expression DO assignment_statement
        expression is a Tree of multiple objects
        assignment_statement is a Tree of multiple objects
        """

        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]

        # stack_expression = []

        # emit reserved word FOR

        # self._emiter.emit_action_10(token_list[0])

        # check control variable exists

        # TODO: Here a list with all tokens from the expression need to be returned so that type check can be done.
        # TODO: Must call _check_type_compatibility

        self._internal_compile(token_list[1])
        #token = token_list[1]
        #identifier = token.value if token.type == "IDENTIFIER" else self._exception_raiser(UnexpectedToken)
        #a_variable = Identifier(identifier, context_label, context_level)
        #a_variable = self._get_declared_variable(action_number, action_name, a_variable)
        #if a_variable:
        #    # self._emiter.emit_action_10(a_variable)

        # emit operator :=

        # self._emiter.emit_action_10(token_list[2])

        # process the expression

        self._internal_compile(token_list[3])

        # process reserved word TO/DOWNTO

        # self._emiter.emit_action_10(token_list[4])

        # process the expression

        self._internal_compile(token_list[5])

        # process reserved word DO

        # self._emiter.emit_action_10(token_list[4])

        # process the assignment_statement

        self._internal_compile(token_list[5])

        #for i in range(0, len(stack_expression) - 1):
        #    self._check_type_compatibility(action_number, action_name, stack_expression[i], stack_expression[i+1])

        self._log(INFO, "[{0}] {1}".format(action_number, action_name))



