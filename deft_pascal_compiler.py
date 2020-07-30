from lark import Tree, Token, UnexpectedToken, UnexpectedCharacters
from deft_pascal_parser_3 import DeftPascalParser
from symbol_table import SymbolTable
from symbols import BaseSymbol, Operator, Constant, Identifier
from symbols import BasicType, PointerType, PointerIdentifier, BooleanConstant, NilConstant
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
                         "TYPE_DEFINITION_PART": self._action_11,
                         "CLOSED_FOR_STATEMENT": self._action_10,
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
        # returns None if symbol not found

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
            a_variable = self._symbol_table.get_from_lower_scope(a_variable)
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

    def _increase_scope(self, scope_label=None):
        # retrieve current scope details from the stack
        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]

        # increase scope
        context_level = context_level + 1
        if scope_label:
            context_label = scope_label

        # push the new scope into the scope stack
        self._stack_scope.append((context_label, context_level))


    def _decrease_scope(self):
        # remove current scope details from the stack
        context_label = self._stack_scope.pop()[0]
        context_level = self._stack_scope.pop()[1]


    def _action_0(self, action_number, action_name, token_list):
        """
        token_list : PROGRAM a_program_name
        """
        # initialise the scope stack
        identifier = token_list[1].value
        self._stack_scope.append((identifier, 0))

        # retrieve the scope details from the stack
        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]

        # add the system constants to the symbol table
        self._symbol_table.append(BooleanConstant.true(context_label, context_level))
        self._symbol_table.append(BooleanConstant.false(context_label, context_level))
        self._symbol_table.append(NilConstant.nil(context_label, context_level))

        # add the base types to the symbol table
        self._symbol_table.append(BasicType.reserved_type_integer(context_label, context_level))
        self._symbol_table.append(BasicType.reserved_type_real(context_label, context_level))
        self._symbol_table.append(BasicType.reserved_type_boolean(context_label, context_level))
        self._symbol_table.append(BasicType.reserved_type_char(context_label, context_level))
        self._symbol_table.append(BasicType.reserved_type_string(context_label, context_level))
        self._symbol_table.append(BasicType.reserved_type_text(context_label, context_level))

        # initialise the intermediate_code engine
        self._ic.init(action_number, action_name)

        # push intermediate code
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
        self._increase_scope()

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
        CONSTANT_DEFINITION_PART
        input_list -> [CONST constant_definition C1 = VALUE constant_definition C2 = VALUE]
        """
        # retrieve the scope details from the stack
        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]

        # initialise the intermediate_code engine
        self._ic.init(action_number, action_name)

        # discard reserved word CONST
        input_list.pop(0)

        # process declarations
        for constant_definition in input_list:
            declaration = constant_definition.children

            # the constant definition (declaration) has 3 parts: identifier, operator and constant
            constant_identifier = declaration[0].value
            constant_type = declaration[-1].type
            constant_value = declaration[-1].value

            # identifier - it must not exist in the symbol_table yet
            if self._symbol_table.contains_name(constant_identifier, context_label, context_level, equal_level_only=False):

                self._log(ERROR, 'Identifier already declared')

            else:

                new_constant = Constant(constant_identifier, context_label, context_level, constant_type, constant_value)

                # push the new constant into the symbol_table
                self._symbol_table.append(new_constant)

                # push the new constant into the intermediate_code engine
                self._ic.push(new_constant)

                # log successful declaration
                self._log(INFO, "[{0}] {1} : {2}".format(action_number, action_name, new_constant))

        # generate the intermediate code
        self._ic.flush()


    def _action_3(self, action_number, action_name, input_list):
        """
        input_list -> VAR [v1 v2 INTEGER] [v3 REAL] [V4 V5 ^ A_NEW_TYPE]...
        """
        # retrieve the scope details from the stack
        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]

        # initialise the intermediate_code engine
        self._ic.init(action_number, action_name)

        # discard reserved word VAR
        input_list.pop(0)

        # process declarations
        for variable_declaration in input_list:
            declaration = variable_declaration.children

            # the TYPE is always at the end of the children list. pop it out and collect the value.
            type_identifier = declaration.pop().value

            # check if a pointer is being declared - if so, pop it out and adjust the class for the incoming identifiers
            is_pointer = declaration[-1].type == "UPARROW"
            if is_pointer:
                declaration.pop()

            # retrieve the actual type from the symbol_table
            type_symbol = self._symbol_table.retrieve_by_name(type_identifier, context_label, context_level, equal_level_only=False)
            if type_symbol:

                # if the type_symbol is itself a pointer, than the variable being declared must be a pointer too
                is_pointer = is_pointer or type_symbol.is_pointer
                identifier_class = Identifier
                if is_pointer:
                    identifier_class = PointerIdentifier

                # process each identifier for the given variable_type
                for token in variable_declaration.children:

                    identifier = token.value

                    # identifier - it must not exist in the symbol_table yet
                    if self._symbol_table.contains_name(identifier, context_label, context_level, equal_level_only=False):

                        msg = "[{0}] {1} :  Identifier '{2}' already declared."
                        self._log(ERROR, msg.format(action_number, action_name, identifier))

                    else:

                        new_variable = identifier_class(identifier, context_label, context_level, type_symbol.type, None)

                        # push the new variable into the symbol_table
                        self._symbol_table.append(new_variable)

                        # push the new variable into the intermediate_code engine
                        self._ic.push(new_variable)

                        # log successful declaration
                        self._log(INFO, "[{0}] {1} : {2}".format(action_number, action_name, new_variable))

            else:

                msg = "[{0}] {1} :  Unknown type '{2}' reference in variable declaration."
                self._log(ERROR, msg.format(action_number, action_name, type_identifier))

        # generate the intermediate code
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
        self._decrease_scope()

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
        # retrieve the scope details from the stack
        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]

        # initialise the intermediate_code engine
        self._ic.init(action_number, action_name)

        # identifier - it must exist in the symbol table
        identifier_name = token_list.pop(0).value
        identifier_symbol = self._symbol_table.retrieve_by_name(identifier_name, context_label, context_level, equal_level_only=False)
        if identifier_symbol:
            self._ic.push(identifier_symbol)

            # consume the operator :=
            token = token_list.pop(0)
            operator = Operator(token.value, context_label, context_level, token.type, token.value)
            self._ic.push(operator)

            # prepare stacks to process the expression
            self._stack_expression = []
            self._stack_expression.append(identifier_symbol)
            self._stack_expression.append(operator)

            # process the expression
            expression = token_list.pop()
            self._internal_compile(expression)

            # perform type checking
            z = check_type_compatibility(self._stack_expression)
            if not check_type_compatibility(self._stack_expression):
                self._log(ERROR, "[{0}] {1} : incompatible types detected {2}".format(action_number, action_name, self._stack_expression))
            else:
                self._log(INFO, "[{0}] {1} : {2}".format(action_number, action_name, self._stack_expression))

        else:

            msg = "[{0}] {1} :  Reference to undeclared variable '{2}'"
            self._log(ERROR, msg.format(action_number, action_name, identifier_name))

        # generate the intermediate code
        self._ic.flush()


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

                # assuming token is an identifier, attempt to retrieve from the symbol table at any level
                a_symbol = self._symbol_table.retrieve_by_name(token.value, context_label, context_level, equal_level_only=False)

                if not a_symbol:

                    # attempt to retrieve from the symbol table at any current level but based on token type
                    a_symbol = self._symbol_table.retrieve_by_name(token.type, context_label, context_level, equal_level_only=False)

                    if not a_symbol:

                        #  if still not present in the symbol table, token might be a constant
                        if token.type in ["UNSIGNED_DECIMAL", "SIGNED_DECIMAL", "NUMBER_BINARY", "NUMBER_OCTAL",
                                          "NUMBER_HEXADECIMAL", "CHARACTER", "STRING", "UNSIGNED_REAL", "SIGNED_REAL"
                                          ]:

                            a_symbol = Constant(token.value, context_label, context_level, token.type, token.value)

                        else:

                            a_symbol = BaseSymbol(token.value, context_label, context_level, token.type, token.value)
                            if a_symbol.is_operator:
                                a_symbol = Operator(token.value, context_label, context_level, token.type, token.value)

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
        # token = token_list[1]
        # identifier = token.value if token.type == "IDENTIFIER" else self._exception_raiser(UnexpectedToken)
        # a_variable = Identifier(identifier, context_label, context_level)
        # a_variable = self._get_declared_variable(action_number, action_name, a_variable)
        # if a_variable:
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

        # for i in range(0, len(stack_expression) - 1):
        #    self._check_type_compatibility(action_number, action_name, stack_expression[i], stack_expression[i+1])

        self._log(INFO, "[{0}] {1}".format(action_number, action_name))

    def _action_11(self, action_number, action_name, input_list):
        """
        input_list -> TYPE  (T1 = INTEGER) (T2 = ^ REAL)
        """

        # retrieve the scope details from the stack
        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]

        # initialise the intermediate code engine
        self._ic.init(action_number, action_name)

        # discard reserved word TYPE
        input_list.pop(0)

        # process declarations
        for type_definition in input_list:

            declaration = type_definition.children

            # check if this type declaration involves a pointer
            is_pointer = declaration[2].type == "UPARROW"

            """
            the type definition (declaration) has 3 parts: 
            identifier i.e. 'T1' 
            operator i.e '='  
            type_identifier, i.e. INTEGER
            """
            identifier = declaration[0].value
            # operator = Operator.from_token(declaration[1], context_label, context_level)
            type_identifier = declaration[-1].value

            # identifier - it must not exist in the symbol_table yet
            if self._symbol_table.contains_name(identifier, context_label, context_level, equal_level_only=False):

                msg = "[{0}] {1} :  Identifier '{2}' already declared in current scope"
                self._log(ERROR, msg.format(action_number, action_name, identifier))

            else:

                # type_identifier - it must exist in the symbol table
                type_symbol = self._symbol_table.retrieve_by_name(type_identifier, context_label, context_level, equal_level_only=False)
                if type_symbol:

                    # at this point we know:
                    # the type being declared is pointer or not
                    # the type being declared references a custom or a basic type
                    # the name for the type being declared
                    # so let's create the new_type

                    # if the type_symbol is itself a pointer, than the variable being declared must be a pointer too
                    is_pointer = is_pointer or type_symbol.is_pointer
                    type_class = BasicType
                    if is_pointer:
                        type_class = PointerType

                    new_type_symbol = type_class(identifier, context_label, context_level, type_symbol.type, None)

                    # push the new type to the symbol_table
                    self._symbol_table.append(new_type_symbol)
                    self._log(INFO, "[{0}] {1} : {2}".format(action_number, action_name, new_type_symbol))

                else:

                    msg = "[{0}] {1} :  Reference to unknown type '{2}'"
                    self._log(ERROR, msg.format(action_number, action_name, type_identifier))
