from lark import Tree, Token, UnexpectedToken, UnexpectedCharacters
from deft_pascal_parser_3 import DeftPascalParser
from symbol_table import SymbolTable
from symbols import BaseSymbol, Operator, Constant, Identifier, Keyword, GenericExpression
from symbols import BasicType, PointerType, PointerIdentifier, ProcedureIdentifier, BooleanConstant, NilConstant
from intermediate_code import IntermediateCode
from compiler_utils import check_type_compatibility
import logging
from logging import ERROR, WARNING, INFO

logger = logging.getLogger(__name__)


class DeftPascalCompiler:

    _GLB_MAIN_BEGIN = "RESERVED_STRUCTURE_BEGIN_PROGRAM"
    _GLB_MAIN_END = "RESERVED_STRUCTURE_END_PROGRAM"
    _GLB_BLOCK_BEGIN = "RESERVED_STRUCTURE_BEGIN_BLOCK"
    _GLB_BLOCK_END = "RESERVED_STRUCTURE_END_BLOCK"

    def __init__(self):
        self._parser = DeftPascalParser()
        self._symbol_table = SymbolTable()

        # self._emiter = None
        self._stack_emiter = []

        self._ic = IntermediateCode()

        self._context = 0

        # self._stack_expression = []
        # self._stack_variables = []
        self._stack_scope = []
        self._stack_begin = []
        self._stack_end = []

        self._actions = {"PROGRAM_HEADING",
                         "LABEL_DECLARATION_PART",
                         "CONSTANT_DEFINITION_PART",
                         "CONSTANT_DEFINITION",
                         "VARIABLE_DECLARATION_PART",
                         "VARIABLE_DECLARATION",
                         "VARIABLE_ACCESS",
                         "RESERVED_STRUCTURE_BEGIN",
                         "RESERVED_STRUCTURE_END",
                         "ASSIGNMENT_STATEMENT",
                         "PROCEDURE_CALL",
                         "EXPRESSION",
                         "CLOSED_FOR_STATEMENT",
                         "COMPOUND_STATEMENT"
                         }

        # self._actions = {"PROGRAM_HEADING": self._action_0,
        #                  "LABEL_DECLARATION_PART": self._action_4,
        #                  "CONSTANT_DEFINITION_PART": self._action_2,
        #                  "TYPE_DEFINITION_PART": self._action_11,
        #                  "VARIABLE_DECLARATION_PART": self._action_3,
        #                  "ASSIGNMENT_STATEMENT": self._action_6,
        #                  "EXPRESSION": self._action_7,
        #                  "REPEAT_STATEMENT": self._action_8,
        #                  "CLOSED_FOR_STATEMENT": self._action_10,
        #                  "PROCEDURE_CALL": self._action_12,
        #                  }
        #                "BOOLEAN_EXPRESSION": self._action_9,
        #self._token_actions = {"IDENTIFIER": self._token_action_0,
        #                       "RESERVED_STRUCTURE_BEGIN": self._action_1,
        #                       "RESERVED_STRUCTURE_END"  : self._action_5,
        #                       }


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
        # retrieve current scope details from the stack
        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]
        # emit log
        msg = "[{0}/{1}] {2}".format(context_label, context_level, log_info)
        if log_type == ERROR:
            self._error_list.append(msg)
            logger.error(msg)
        elif log_type == WARNING:
            logger.warning(msg)
        else:
            logger.info(msg)

    def _compile_tree(self, a_tree, working_stack):
        action_name = a_tree.data.upper()
        if action_name in self._actions:
            method_to_call = getattr(DeftPascalCompiler, "_" + action_name.lower())
            return method_to_call(self, action_name, a_tree.children, working_stack)
        else:
            self._log(ERROR, "action '{0}' not yet implemented for tree {1}".format(a_tree.data.upper(), a_tree))

    def _compile_token(self, a_token, working_stack):
        action_name = a_token.type.upper()
        if action_name in self._actions:
            method_to_call = getattr(DeftPascalCompiler, "_" + action_name.lower())
            return method_to_call(self, action_name, a_token, working_stack)
        else:
            self._log(ERROR, "action '{0}' not yet implemented for token {1}".format(a_token.type.upper(), a_token.value.upper()))

    def _internal_compile(self, ast, working_stack=[]):
        if isinstance(ast, Tree):
            if len(ast.children) > 0:
                return self._compile_tree(ast, working_stack)
        elif isinstance(ast, Token):
            return self._compile_token(ast, working_stack)
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


    # def _retrieve_from_symbol_table(self, action_number, action_name, a_symbol):
    #     # check symbol exists
    #     # scenarios:
    #     # - symbol not declared
    #     # - symbol declared on same scope
    #     # - symbol declared on a lower scope
    #     # returns None if symbol not found
    #
    #     if self._symbol_table.has_equal(a_symbol, equal_class=False, equal_type=False, equal_level=True, equal_name=True):
    #         a_symbol = self._symbol_table.get(a_symbol)
    #     elif self._symbol_table.has_equal(a_symbol, equal_class=False, equal_type=False, equal_level=False, equal_name=True):
    #         a_symbol = self._symbol_table.get_from_lower_scope(a_symbol)
    #     else:
    #         msg = "Error! [{0}] {1} - Reference to undeclared symbol {2}"
    #         self._log(ERROR, msg.format(action_number, action_name, a_symbol))
    #         a_symbol = None
    #     return a_symbol

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

    def _perform_type_check(self, action_name, expression):
        """
        expression - is a list of tokens.
        """
        compatible = check_type_compatibility(expression)
        if compatible:
            # instead of returning an instance of symbol, return only the type of that symbol.
            compatible = compatible.type
        else:
            msg = "[{0}] incompatible types in expression: {1}"
            self._log(ERROR, msg.format(action_name, expression))
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


    def _token_action_0(self, action_number, action_name, token):
        """
        token -> IDENTIFIER
        """
        # retrieve the scope details from the stack
        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]

        # retrieve the actual identifier from the symbol_table
        identifier = self._symbol_table.retrieve_by_name(token.value, context_label, context_level, equal_level_only=False)
        if identifier:

            pass

        else:

            msg = "[{0}] {1} :  Unknown identifier '{2}' reference."
            self._log(ERROR, msg.format(action_number, action_name, identifier))


    def _program_heading(self, action_name, token_list, working_stack):
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

        # add the in-built procedures to the symbol table
        self._symbol_table.append(ProcedureIdentifier.in_built_procedure_write(context_label, context_level))
        self._symbol_table.append(ProcedureIdentifier.in_built_procedure_writeln(context_label, context_level))

        # initialize the control stack for BEGIN and END
        self._stack_begin.append(self._GLB_MAIN_BEGIN)
        self._stack_end.append(self._GLB_MAIN_END)

        # initialise the intermediate_code engine
        self._ic.init(action_name)

        # push intermediate code
        self._ic.push(token_list[0])
        self._ic.push(token_list[1])
        self._ic.flush()

        self._log(INFO, "[{0}] : '{1}' - stack: {2} {3}".format(action_name,
                                                                identifier,
                                                                self._symbol_table,
                                                                self._stack_scope))

        if len(token_list) > 2:
            self._log(WARNING, "[{0}] variables detected - all will be ignored".format(action_name))


    def _compound_statement(self, action_name, input_list, working_stack):
        """
        COMPOUND_STATEMENT
        input_list -> BEGIN Tree() Tree() Tree() ... END
        """
        while input_list:
            self._internal_compile(input_list.pop(0))

    def _reserved_structure_begin(self, action_name, input_token, working_stack):
        """
        RESERVED_STRUCTURE_BEGIN
        currently implemented as a token.
        """
        action = self._stack_begin.pop(-1)
        self._stack_begin.append(self._GLB_BLOCK_BEGIN)
        if not action == self._GLB_MAIN_BEGIN:
            self._stack_end.append(self._GLB_BLOCK_END)

        self._ic.init(action)
        self._ic.push(input_token)
        self._ic.flush()

        self._log(INFO, "[{0}] : {1} {2}".format(action, self._symbol_table, self._stack_scope))

    def _reserved_structure_end(self, action_name, input_token, working_stack):
        """
        RESERVED_STRUCTURE_END
        currently implemented as a token.
        """
        action = self._stack_end.pop(-1)
        self._ic.init(action)
        self._ic.push(input_token)
        self._ic.flush()

        self._log(INFO, "[{0}] : {1}".format(action, self._symbol_table))


    def _constant_definition_part(self, action_name, input_list, working_stack):
        """
        CONSTANT_DEFINITION_PART
        input_list -> [CONST Tree(constant_definition C1 = VALUE) Tree(constant_definition C2 = VALUE)]
        """
        # retrieve the scope details from the stack
        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]

        # initialise the intermediate_code engine
        self._ic.init(action_name)

        # discard reserved word CONST
        input_list.pop(0)

        # process declarations
        for constant_definition in input_list:

            self._internal_compile(constant_definition)

        # generate the intermediate code
        self._ic.flush()


    def _constant_definition(self, action_name, input_list, working_stack):
        """
        CONSTANT_DEFINITION
        input_list -> [C1 = VALUE]
        """
        # retrieve the scope details from the stack
        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]

        # the constant definition (declaration) has 3 parts: identifier, operator and constant
        constant_identifier = input_list[0].value
        constant_type = input_list[-1].type
        constant_value = input_list[-1].value

        # identifier - it must not exist in the symbol_table yet
        if self._symbol_table.contains_name(constant_identifier, context_label, context_level, equal_level_only=False):

            self._log(ERROR, "[{0}] identifier '{1}' already declared ".format(action_name, constant_identifier))

        else:

            new_constant = Constant(constant_identifier, context_label, context_level, constant_type, constant_value)

            # push the new constant into the symbol_table
            self._symbol_table.append(new_constant)

            # push the new constant into the intermediate_code engine
            self._ic.push(new_constant)

            # log successful declaration
            self._log(INFO, "[{0}] new identifier declared : {1}".format(action_name, new_constant))


    def _variable_declaration_part(self, action_name, input_list, working_stack):
        """
        VARIABLE_DECLARATION_PART
        input_list -> [VAR Tree(variable_declaration v1 v2 INTEGER) Tree(variable_declaration v3 REAL) Tree(variable_declaration V4 V5 ^ A_NEW_TYPE)...
        """
        # retrieve the scope details from the stack
        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]

        # initialise the intermediate_code engine
        self._ic.init(action_name)

        # discard reserved word VAR
        input_list.pop(0)

        # process declarations
        for variable_declaration in input_list:

            self._internal_compile(variable_declaration)

        # generate the intermediate code
        self._ic.flush()

    def _variable_declaration(self, action_name, input_list, working_stack):
        """
        VARIABLE_DECLARATION
        input_list -> [v1 v2 INTEGER]
        """
        # retrieve the scope details from the stack
        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]

        # the TYPE is always at the end of the input list. pop it out and collect the value.
        type_identifier = input_list.pop().value.upper()

        # check if a pointer is being declared - if so, pop it out and adjust the class for the incoming identifiers
        is_pointer = input_list[-1].type == "UPARROW"
        if is_pointer:
            input_list.pop()

        # retrieve the actual type from the symbol_table
        type_symbol = self._symbol_table.retrieve_by_name(type_identifier, context_label, context_level, equal_level_only=False)
        if type_symbol:

            # if the type_symbol is itself a pointer, than the variable being declared must be a pointer too
            is_pointer = is_pointer or type_symbol.is_pointer
            identifier_class = Identifier
            if is_pointer:
                identifier_class = PointerIdentifier

            # process each identifier for the given variable_type
            for token in input_list:

                identifier = token.value

                # identifier - it must not exist in the symbol_table yet
                if self._symbol_table.contains_name(identifier, context_label, context_level, equal_level_only=False):

                    msg = "[{0}] identifier '{1}' already declared."
                    self._log(ERROR, msg.format(action_name, identifier))

                else:

                    new_variable = identifier_class(identifier, context_label, context_level, type_symbol.type, None)

                    # push the new variable into the symbol_table
                    self._symbol_table.append(new_variable)

                    # push the new variable into the intermediate_code engine
                    self._ic.push(new_variable)

                    # log successful declaration
                    self._log(INFO, "[{0}] new identifier declared : {1}".format(action_name, new_variable))

        else:

            msg = "[{0}] unknown type '{1}' reference in declaration."
            self._log(ERROR, msg.format(action_name, type_identifier))


    def _variable_access(self, action_name, input_list, working_stack):
        """
        VARIABLE_ACCESS
        input_list -> [Token(IDENTIFIER, 'fahren')]

        This method will push the identifier to the expression stack and intermediate code stack
        """
        # retrieve the scope details from the stack
        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]

        # identifier - it must exist in the symbol table
        identifier_name = input_list.pop(0).value
        identifier_symbol = self._symbol_table.retrieve_by_name(identifier_name, context_label, context_level, equal_level_only=False)
        if identifier_symbol:

            working_stack.append(identifier_symbol)
            # self._ic.push(identifier_symbol)

        else:

            msg = "[{0}] :  Reference to undeclared variable '{1}'"
            self._log(ERROR, msg.format(action_name, identifier_name))

        return working_stack

    def _label_declaration_part(self, action_name, input_list):
        """
        process LABEL_DECLARATION_PART
        """
        self._log(WARNING, "[{0}] - all will be ignored".format(action_name))


    def _assignment_statement(self, action_name, input_list, working_stack):
        """
        ASSIGNMENT_STATEMENT
        [Tree(variable_access, [IDENTIFIER]), OPERATOR_ASSIGNMENT, Tree(expression, [Token(UNSIGNED_DECIMAL, '0')])])
        token_list -> identifier := expression
        """
        # retrieve the scope details from the stack
        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]

        # process the identifier
        working_stack = self._internal_compile(input_list.pop(0), [])

        # consume the operator :=
        token = input_list.pop(0)
        operator = Operator(token.value, context_label, context_level, token.type, token.value)
        working_stack.append(operator)

        # process the expression
        expression_stack = self._internal_compile(input_list.pop(), [])

        # check type compatibility
        self._perform_type_check(action_name, working_stack + expression_stack)

        # push the expression to the working stack
        working_stack.append(GenericExpression.from_list(expression_stack))

        # generate the intermediate code
        self._ic.init(action_name)
        self._ic.push(working_stack)
        self._ic.flush()

        self._log(INFO, "[{0}] : {1}".format(action_name, working_stack))

        return working_stack


    def _expression(self, action_name, token_list, working_stack):

        # process expressions in assignments
        # this is called from other actions and therefore it does not create its own action on the intermediate code
        # it also does not need to flush the intermediate code. this will be done in another action.

        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]

        for token in token_list:
            if isinstance(token, Tree):

                working_stack = self._internal_compile(token, working_stack)

            elif isinstance(token, Token):

                # assuming token is an identifier, attempt to retrieve from the symbol table at any level
                a_symbol = self._symbol_table.retrieve_by_name(token.value, context_label, context_level, equal_level_only=False)

                if not a_symbol:

                    # attempt to retrieve from the symbol table at any current level but based on token type
                    a_symbol = self._symbol_table.retrieve_by_name(token.type, context_label, context_level, equal_level_only=False)

                    if not a_symbol:

                        #  if still not present in the symbol table, token might be a constant
                        if token.type in ["UNSIGNED_DECIMAL", "SIGNED_DECIMAL", "NUMBER_BINARY", "NUMBER_OCTAL",
                                          "NUMBER_HEXADECIMAL", "CHARACTER", "STRING_VALUE", "UNSIGNED_REAL",
                                          "SIGNED_REAL"
                                          ]:

                            a_symbol = Constant(token.value, context_label, context_level, token.type, token.value)

                        else:

                            a_symbol = BaseSymbol(token.value, context_label, context_level, token.type, token.value)
                            if a_symbol.is_operator:
                                a_symbol = Operator(token.value, context_label, context_level, token.type, token.value)

                working_stack.append(a_symbol)
                # self._ic.push(a_symbol)

            else:

                self._exception_raiser(KeyError)

        return working_stack

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

        # retrieve the scope details from the stack
        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]

        # initialise the intermediate code engine
        self._ic.init(action_name)

        # process REPEAT
        self._ic.push(token_list.pop(0))
        self._log(INFO, "[{0}] {1} : REPEAT".format(action_number, action_name))
        self._ic.flush()

        # process statements
        while True:
            token = token_list.pop(0)
            if isinstance(token, Token) and token.type == "RESERVED_STATEMENT_UNTIL":
                self._ic.init(action_name)
                self._ic.push(token)
                self._log(INFO, "[{0}] {1} : UNTIL".format(action_number, action_name))
                break
            else:
                self._internal_compile(token)

        # process expression after UNTIL
        # TODO: Here a list with all tokens from the expression need to be returned so that type check can be done.
        # TODO: Must call _perform_type_check
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
            self._perform_type_check(action_name, stack_expression[i], stack_expression[i+1])

        self._log(INFO, "[{0}] {1} : {2}".format(action_number, action_name, stack_expression))

    def _closed_for_statement(self, action_name, input_list, working_stack):
        """
        CLOSED_FOR_STATEMENT
        input_list will have: FOR identifier := Tree(expression) TO/DOWNTO Tree(expression) DO BEGIN Tree(assignment_statement END
        expression is a Tree of multiple objects
        assignment_statement is a Tree of multiple objects
        """

        # retrieve the scope details from the stack
        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]
        working_stack = []

        # emit reserved word FOR
        keyword = Keyword.from_token(input_list.pop(0), context_label, context_level)
        working_stack.append(keyword)

        # process the control variable (or expression)
        control_variable_stack = self._internal_compile(input_list.pop(0), [])
        working_stack = working_stack + control_variable_stack

        # consume the operator :=
        token = input_list.pop(0)
        operator = Operator(token.value, context_label, context_level, token.type, token.value)
        control_variable_stack.append(operator)
        working_stack.append(operator)

        # process the 'initial_value' (or expression) on the for
        expression_stack = self._internal_compile(input_list.pop(0), [])
        working_stack.append(GenericExpression.from_list(expression_stack))

        # check type compatibility of the control_variable := expression(initial_value)
        self._perform_type_check(action_name, control_variable_stack + expression_stack)

        # emit reserved word to / downto
        keyword = Keyword.from_token(input_list.pop(0), context_label, context_level)
        working_stack.append(keyword)

        # process the 'final_value' on the for
        expression_stack = self._internal_compile(input_list.pop(0), [])
        working_stack.append(GenericExpression.from_list(expression_stack))

        # check compatibility of the control_variable := expression(final_value)
        self._perform_type_check(action_name, control_variable_stack + expression_stack)

        # emit reserved word do
        keyword = Keyword.from_token(input_list.pop(0), context_label, context_level)
        working_stack.append(keyword)

        # generate the intermediate code
        self._ic.init(action_name)
        self._ic.push(working_stack)
        self._ic.flush()

        self._log(INFO, "[{0}] {1}".format(action_name, working_stack))

        # process statements nested inside the for
        return self._internal_compile(input_list.pop(0), [])


    def _action_11(self, action_number, action_name, input_list):
        """
        input_list -> TYPE  (T1 = INTEGER) (T2 = ^ REAL) (T3 = T1)
        """

        # retrieve the scope details from the stack
        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]

        # initialise the intermediate code engine
        self._ic.init(action_name)

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

            # identifier - it must NOT exist in the symbol_table yet
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

                    # push the new variable into the intermediate_code engine
                    self._ic.push(new_type_symbol)

                    # log successful declaration
                    self._log(INFO, "[{0}] {1} : {2}".format(action_number, action_name, new_type_symbol))

                else:

                    msg = "[{0}] {1} :  Reference to unknown type '{2}'"
                    self._log(ERROR, msg.format(action_number, action_name, type_identifier))

        # generate the intermediate code
        self._ic.flush()


    def _procedure_call(self, action_name, input_list, working_stack):
        """
        PROCEDURE_CALL
        input_list -> [IDENTIFIER, LEFT_PARENTHESES, Tree(actual_parameter(Tree expression), COMMA, Tree(expression), ... RIGHT_PARENTHESES]
        """

        # retrieve the scope details from the stack
        context_label = self._stack_scope[-1][0]
        context_level = self._stack_scope[-1][1]
        working_stack = []

        # retrieve the actual procedure identifier from the symbol_table
        identifier = input_list.pop(0)
        identifier = self._symbol_table.retrieve_by_name(identifier.value, context_label, context_level, equal_level_only=False)
        if identifier:

            # push the identifier to the working stack
            working_stack.append(identifier)

            # discard the open and close parentheses operands
            input_list.pop(0)
            input_list.pop(-1)

            # process each parameter expression, discard the commas used as separators
            parameters_counter = 0
            for token in input_list:

                if isinstance(token, Token):

                    if not token.type == "COMMA":

                        msg = "[{0}] :  Unknown token '{1}' passed in procedure parameter."
                        self._log(ERROR, msg.format(action_name, token))

                elif isinstance(token, Tree):

                    parameters_counter = parameters_counter + 1

                    value_to_print_stack = self._internal_compile(token.children[0], [])
                    field_width_stack = None
                    decimal_field_width_stack = None

                    # type checking the expression passed as parameter
                    generic_expression_type = self._perform_type_check(action_name, value_to_print_stack)

                    # TODO: check if the expression type is compatible with the procedure parameter type definition

                    if token.data.upper() in ["BINARY_PARAMETER", "TERNARY_PARAMETER"]:

                        field_width_stack = self._internal_compile(token.children[1], [])
                        self._perform_type_check(action_name, field_width_stack)

                    if token.data.upper() == "TERNARY_PARAMETER":

                        decimal_field_width_stack = self._internal_compile(token.children[2], [])
                        self._perform_type_check(action_name, decimal_field_width_stack)

                    if (field_width_stack or decimal_field_width_stack) and identifier.name.upper() not in ["WRITE", "WRITELN"]:

                        msg = "[{0}] formatting parameters incompatible with {1}}. Formatting will be ignored."
                        self._log(WARNING, msg.format(action_name, identifier.name))
                        field_width_stack = None
                        decimal_field_width_stack = None

                    # create the parameter as a generic expression
                    generic_expression = GenericExpression.from_list((GenericExpression.from_list(value_to_print_stack),
                                                                      GenericExpression.from_list(field_width_stack) if field_width_stack else None,
                                                                      GenericExpression.from_list(decimal_field_width_stack) if decimal_field_width_stack else None
                                                                      ))
                    generic_expression.type = generic_expression_type

                    # push to the working stack
                    working_stack.append(generic_expression)

                else:

                    msg = "[{0}] :  Unknown object '{1}' passed to procedure {2} parameter."
                    self._log(ERROR, msg.format(action_name, token, identifier))

            if identifier.value and not identifier.parameter_counter == parameters_counter:

                msg = "[{0}] :  '{1}' parameters passed to procedure {2} but '{3}' expected."
                self._log(ERROR, msg.format(action_name, parameters_counter, identifier.name, identifier.parameter_counter))

            # generate the intermediate code
            self._ic.init(action_name)
            self._ic.push(working_stack)
            self._ic.flush()

            self._log(INFO, "[{0}] {1} {2} {3}".format(action_name, identifier, parameters_counter, working_stack))

        else:

            msg = "[{0}] {1} :  Unknown procedure '{1}' reference."
            self._log(ERROR, msg.format(action_name, identifier))

        return working_stack
