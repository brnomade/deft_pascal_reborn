"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from lark import Tree, Token
from components.deft_pascal_parser_3 import DeftPascalParser
from components.symbol_table import SymbolTable
from components.symbols.base_symbols import BaseSymbol, Keyword, GenericExpression
from components.symbols.operator_symbols import Operator, BinaryOperator, UnaryOperator, NeutralOperator
from components.symbols.identifier_symbols import Identifier, PointerIdentifier, ProcedureIdentifier, ConstantIdentifier
from components.symbols.literals_symbols import Literal, BooleanLiteral, NilLiteral, NumericLiteral, StringLiteral
from components.symbols.type_symbols import PointerType, BasicType, StringType
from components.intermediate_code import IntermediateCode
from utils.compiler_utils import check_type_compatibility, token_is_an_operator
import copy
import logging
from logging import ERROR, WARNING, INFO, DEBUG

_MODULE_LOGGER = logging.getLogger(__name__)


class DeftPascalCompiler:

    _GLB_MAIN_BEGIN = "RESERVED_STRUCTURE_BEGIN_PROGRAM"
    _GLB_MAIN_END = "RESERVED_STRUCTURE_END_PROGRAM"
    _GLB_BLOCK_BEGIN = "RESERVED_STRUCTURE_BEGIN_BLOCK"
    _GLB_BLOCK_END = "RESERVED_STRUCTURE_END_BLOCK"

    def __init__(self, cmoc=False):
        self._parser = DeftPascalParser()
        self._ast = None
        self._symbol_table = SymbolTable()
        self._symbol_table.increase_level("symbol_table_root")
        self._operator_table = SymbolTable()
        self._operator_table.increase_level("operator_table_root")
        self._ic = IntermediateCode(cmoc)

        self._context = 0

        self._stack_emiter = []
        self._stack_scope = []
        self._stack_begin = []
        self._stack_end = []

        self._error_list = []

        self._actions = {"PROGRAM_HEADING",
                         "LABEL_DECLARATION_PART",
                         "CONSTANT_DEFINITION_PART",
                         "CONSTANT_DEFINITION",
                         "CONSTANT_EXPRESSION",
                         "TYPE_DEFINITION_PART",
                         "TYPE_DEFINITION",
                         "VARIABLE_DECLARATION_PART",
                         "VARIABLE_DECLARATION",
                         "VARIABLE_ACCESS",
                         "RESERVED_STRUCTURE_BEGIN",
                         "RESERVED_STRUCTURE_END",
                         "ASSIGNMENT_STATEMENT",
                         "PROCEDURE_CALL",
                         "EXPRESSION",
                         "CLOSED_FOR_STATEMENT",
                         "CLOSED_WHILE_STATEMENT",
                         "REPEAT_STATEMENT",
                         "COMPOUND_STATEMENT",
                         "CLOSED_IF_STATEMENT"
                         }


    def check_syntax(self, input_program):
        error_list = self._parser.parse(input_program)
        if not error_list:
            self._ast = self._parser.ast
        else:
            self._ast = None
        return error_list

    def compile(self, ast=None):
        _MODULE_LOGGER.debug("start compile")
        if not ast and not self._ast:
            raise ValueError("AST is not yet defined")
        #
        if not ast and self._ast:
            ast = self._ast
        #
        self._error_list = []
        for i in ast.children:
            self._internal_compile(i)
        #
        return self._error_list

    @property
    def ast(self):
        if self._ast:
            return self._ast
        else:
            raise ValueError("AST is not yet defined")

    @property
    def intermediate_code(self):
        return str(self._ic)

    def generate(self):
        return self._ic.generate()

    def _log(self, log_type=INFO, log_info=""):
        # retrieve the scope details from the stack
        context_label = self._symbol_table.current_scope
        context_level = self._symbol_table.current_level
        # emit log
        msg = "[{0}/{1}] {2}".format(context_label, context_level, log_info)
        if log_type == ERROR:
            self._error_list.append(msg)
            _MODULE_LOGGER.error(msg)
        elif log_type == WARNING:
            _MODULE_LOGGER.warning(msg)
        elif log_type == INFO:
            _MODULE_LOGGER.info(msg)
        else:
            _MODULE_LOGGER.debug(msg)

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


    def _perform_type_check(self, action_name, expression):
        """
        expression - is a list of tokens.
        always returns an instance of BasicType if the expression passes type checking
        returns None if expression is not conformant
        """
        compatible = check_type_compatibility(expression)
        if compatible:
            # instead of returning an instance of symbol, return only the type of that symbol.
            compatible = compatible if isinstance(compatible, BasicType) else compatible.type
        else:
            msg = "[{0}] incompatible types in expression: {1}"
            self._log(ERROR, msg.format(action_name, expression))
            assert compatible is None, "received {0}".format(compatible)

        assert compatible is not None or not isinstance(compatible, BasicType), "received {0}".format(compatible)

        return compatible


    def _increase_scope(self, scope_label=None):
        # retrieve current scope details from the stack
        context_label = self._symbol_table.current_scope

        # increase scope
        if scope_label:
            context_label = scope_label
        self._symbol_table.increase_level(context_label)


    def _decrease_scope(self):
        # remove current scope details from the stack
        self._symbol_table.decrease_level()


    def _program_heading(self, action_name, token_list, working_stack):
        """
        token_list : PROGRAM a_program_name
        """
        # initialise the scope stack
        identifier = token_list[1].value
        self._increase_scope(identifier)

        # add the system constants to the symbol table
        self._symbol_table.append(BooleanLiteral.true())
        self._symbol_table.append(BooleanLiteral.false())
        self._symbol_table.append(NilLiteral.nil())

        # add the base types to the symbol table
        self._symbol_table.append(BasicType.reserved_type_integer())
        self._symbol_table.append(BasicType.reserved_type_real())
        self._symbol_table.append(BasicType.reserved_type_boolean())
        self._symbol_table.append(BasicType.reserved_type_char())
        self._symbol_table.append(StringType.reserved_type_string())
        self._symbol_table.append(BasicType.reserved_type_text())

        # add the in-built procedures to the symbol table - they are added twice, in lower and upper cases
        for procedure in [ProcedureIdentifier.in_built_procedure_write,
                          ProcedureIdentifier.in_built_procedure_writeln
                          ]:
            # lower case scenario
            p = procedure()
            self._symbol_table.append(p)
            # upper case scenario
            p = procedure()
            p.name = p.name.upper()
            self._symbol_table.append(p)

        # initialise the operator table
        self._operator_table.append(BinaryOperator.operator_multiply())
        self._operator_table.append(BinaryOperator.operator_plus())
        self._operator_table.append(BinaryOperator.operator_minus())
        self._operator_table.append(BinaryOperator.operator_divide())
        self._operator_table.append(BinaryOperator.operator_div())
        self._operator_table.append(BinaryOperator.operator_assignment())
        self._operator_table.append(BinaryOperator.operator_equal_to())
        self._operator_table.append(BinaryOperator.operator_not_equal_to())
        self._operator_table.append(BinaryOperator.operator_starstar())
        self._operator_table.append(BinaryOperator.operator_in())
        self._operator_table.append(BinaryOperator.operator_and())
        self._operator_table.append(BinaryOperator.operator_or())
        self._operator_table.append(BinaryOperator.operator_greater_than())
        self._operator_table.append(BinaryOperator.operator_greater_or_equal_to())
        self._operator_table.append(BinaryOperator.operator_less_than())
        self._operator_table.append(BinaryOperator.operator_less_or_equal_to())
        self._operator_table.append(UnaryOperator.operator_not())
        self._operator_table.append(UnaryOperator.operator_abs())
        self._operator_table.append(UnaryOperator.operator_arithmetic_negation())
        self._operator_table.append(UnaryOperator.operator_arithmetic_neutral())
        self._operator_table.append(UnaryOperator.operator_uparrow())
        self._operator_table.append(NeutralOperator.operator_left_parentheses())
        self._operator_table.append(NeutralOperator.operator_right_parentheses())

        # initialize the control stack for BEGIN and END
        self._stack_begin.append(self._GLB_MAIN_BEGIN)
        self._stack_end.append(self._GLB_MAIN_END)

        # initialise the intermediate_code engine
        self._ic.init(action_name)

        # push intermediate code
        self._ic.push(token_list[0])
        self._ic.push(token_list[1])
        self._ic.flush()

        self._log(DEBUG, "[{0}] : '{1}' - stack: {2} {3}".format(action_name, identifier, self._symbol_table, self._stack_scope))

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

        self._log(DEBUG, "[{0}] : {1} {2}".format(action, self._symbol_table, self._stack_scope))


    def _reserved_structure_end(self, action_name, input_token, working_stack):
        """
        RESERVED_STRUCTURE_END
        currently implemented as a token.
        """
        action = self._stack_end.pop(-1)
        self._ic.init(action)
        self._ic.push(input_token)
        self._ic.flush()

        self._log(DEBUG, "[{0}] : {1}".format(action, self._symbol_table))


    def _constant_definition_part(self, action_name, input_list, working_stack):
        """
        CONSTANT_DEFINITION_PART
        input_list -> [CONST Tree(constant_definition C1 = VALUE) Tree(constant_definition C2 = VALUE)]
        """
        # initialise the intermediate_code engine
        self._ic.init(action_name)

        # discard reserved word CONST
        input_list.pop(0)

        # process declarations
        for constant_definition in input_list:

            self._internal_compile(constant_definition)

        # generate the intermediate code
        self._ic.flush()

        return working_stack


    def _constant_definition(self, action_name, input_list, working_stack):
        """
        CONSTANT_DEFINITION
        input_list -> [
                       Token(IDENTIFIER, 'C1'),
                       Token(OPERATOR_EQUAL_TO, '='),
                       Tree(constant_expression, [Token(CONSTANT_TRUE, 'True')])
                      ]
        """
        # extract the identifier
        constant_identifier = input_list.pop(0).value

        # identifier - it must not exist in the symbol_table yet
        if self._symbol_table.contains(constant_identifier, equal_level_only=False):
            self._log(ERROR, "[{0}] constant identifier '{1}' already declared ".format(action_name, constant_identifier))

        else:
            # discard the operator =
            input_list.pop(0)

            # process the constant_expression (literals)
            expression_stack = self._internal_compile(input_list.pop(0), [])

            if expression_stack:
                # check type compatibility
                constant_type = self._perform_type_check(action_name, expression_stack)

                g = GenericExpression.from_list(expression_stack)
                g.type = constant_type

                new_constant = ConstantIdentifier(constant_identifier, constant_type, g)

                # constant - its value must not exceed the types available in the target environment
                compliant = new_constant.complies_to_type_restrictions()
                if compliant is None:
                    self._log(WARNING, "[{0}] complex constant expression '{1}' cannot be validated for type compliance during compilation".format(action_name, constant_identifier))

                elif compliant:
                    # push the new constant into the symbol_table
                    self._symbol_table.append(new_constant)

                    # push the new constant into the intermediate_code engine
                    self._ic.push(new_constant)

                    # log successful declaration
                    self._log(DEBUG, "[{0}] new constant declared : {1}".format(action_name, new_constant))

                else:
                    self._log(ERROR, "[{0}] constant '{1}' not compatible with type limitations".format(action_name, new_constant))

            else:
                self._log(ERROR, "[{0}] invalid expression in constant definition".format(action_name))

        return working_stack


    def _constant_expression(self, action_name, input_list, working_stack):
        """
        CONSTANT_EXPRESSION == 'AN EXPRESSION OF LITERALS'
        process constant expressions
        this is called from other actions and therefore it does not create its own action on the intermediate code
        it also does not need to flush the intermediate code. this will be done in another action.
        """
        for token in input_list:
            if isinstance(token, Tree):
                working_stack = self._internal_compile(token, working_stack)

            elif isinstance(token, Token):
                """
                on a constant_expression, any element present can only be:
                - a pre-defined ConstantIdentifier or Literal
                - a brand new Literal
                """
                a_symbol = self._symbol_table.retrieve(token.type, equal_level_only=False)
                if a_symbol:

                    if isinstance(a_symbol, ConstantIdentifier) or isinstance(a_symbol, BooleanLiteral) or isinstance(a_symbol, NilLiteral):
                        working_stack.append(a_symbol)

                    else:
                        msg = "[{0}] : invalid symbol '{1}' used in constant definition expression"
                        self._log(ERROR, msg.format(action_name, token.type))

                else:

                    if token.type in ["UNSIGNED_DECIMAL", "SIGNED_DECIMAL", "NUMBER_BINARY", "NUMBER_OCTAL",
                                      "NUMBER_HEXADECIMAL", "UNSIGNED_REAL", "SIGNED_REAL"]:
                        a_symbol = NumericLiteral.from_token(token)
                        working_stack.append(a_symbol)

                    elif token.type in ["CHARACTER", "STRING_VALUE"]:
                        a_symbol = StringLiteral.from_token(token)
                        working_stack.append(a_symbol)

                    else:
                        msg = "[{0}] invalid symbol '{1}' used in constant definition expression"
                        self._log(ERROR, msg.format(action_name, token.type))

            else:
                raise NotImplementedError("expected a Token or a Tree but received '{0}'".format(token))

        return working_stack


    def _variable_declaration_part(self, action_name, input_list, working_stack):
        """
        VARIABLE_DECLARATION_PART
        input_list -> [VAR Tree(variable_declaration v1 v2 INTEGER) Tree(variable_declaration v3 REAL) Tree(variable_declaration V4 V5 ^ A_NEW_TYPE)...
        """
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
        input_list -> [v1 , v2 ^ STRING ( 60 ) ]
                      [v1 , v2 INTEGER]
                      [V1 , V2 ^ INTEGER]
                      [v1 , v2 STRING ( 60 )]
        there are 2 scenarios:
        - (special case) the TYPE might be a string with a specific dimension. 
            In this case, there are following tokens after type: '(' 'NUMBER' ')'
            We detect the special case based on the '(' presence
            pop the 3 of them and let the default case code continue.
        - (default case) the TYPE is at the end of the input list. 
            In this case, pop it out and collect the value.
        """
        string_dimension = None
        if input_list[-1].type == "RIGHT_PARENTHESES":    # handling the string with dimension special case
            input_list.pop()    # discard the )
            string_dimension = input_list.pop()
            input_list.pop()    # discard the (

        type_identifier = input_list.pop().value.upper()

        # check if a pointer is being declared - if so, pop it out
        is_pointer = False
        if input_list[-1].type == "OPERATOR_UPARROW":
            is_pointer = True
            input_list.pop()

        type_symbol = self._symbol_table.retrieve(type_identifier, equal_level_only=False)

        if type_symbol:

            if string_dimension:
                type_symbol = copy.copy(type_symbol)
                type_symbol.dimension = string_dimension

            if is_pointer:
                aux = type_symbol
                type_symbol = PointerType.reserved_type_pointer()
                type_symbol.type = aux

            # process each identifier for the given variable_type
            for token in input_list:

                if not token.type == "COMMA":

                    identifier = token.value

                    # identifier - it must not exist in the symbol_table yet
                    if self._symbol_table.contains(identifier, equal_level_only=False):

                        msg = "[{0}] identifier '{1}' already declared."
                        self._log(ERROR, msg.format(action_name, identifier))

                    else:

                        new_variable = Identifier(identifier, type_symbol, None)

                        # push the new variable into the symbol_table
                        self._symbol_table.append(new_variable)

                        # push the new variable into the intermediate_code engine
                        self._ic.push(new_variable)

                        # log successful declaration
                        self._log(DEBUG, "[{0}] new identifier declared : {1}".format(action_name, new_variable))

        else:

            msg = "[{0}] unknown type '{1}' reference in declaration."
            self._log(ERROR, msg.format(action_name, type_identifier))


    def _variable_access(self, action_name, input_list, working_stack):
        """
        VARIABLE_ACCESS
        scenario 1 - non-pointer
        input_list -> [Token(IDENTIFIER, 'V1')]
        scenario 2 - pointer
        input_list ->[ Tree(variable_access, [Token(IDENTIFIER, 'V1')]),
                       Token(OPERATOR_UPARROW, '^')
                    ]

        This method will push the identifier to the expression stack and intermediate code stack
        """
        if len(input_list) == 1:    # scenario 1 - access to a non-pointer identifier
            identifier_name = input_list[0].value
            operator_symbol = None

        elif len(input_list) == 2:  # scenario 2 - access to a pointer identifier
            identifier_name = input_list[0].children[0].value
            operator_name = input_list[1].type
            operator_symbol = self._operator_table.retrieve(operator_name, equal_level_only=False)

        else:
            self._log(ERROR, 'Error - unknown AST object {0}'.format(input_list))
            raise TypeError

        # identifier - it must exist in the symbol table
        identifier_symbol = self._symbol_table.retrieve(identifier_name, equal_level_only=False)

        if identifier_symbol:
            working_stack.append(identifier_symbol)
            if operator_symbol:
                working_stack.append(operator_symbol)

        else:
            msg = "[{0}] :  Reference to undeclared variable '{1}'"
            self._log(ERROR, msg.format(action_name, identifier_name))

        return working_stack


    def _label_declaration_part(self, action_name, input_list, working_stack):
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
        # process the identifier
        working_stack = self._internal_compile(input_list.pop(0), [])

        if working_stack:

            identifier = working_stack[-1]

            # check the identifier receiving the assignment is variable.
            if isinstance(identifier, ConstantIdentifier):
                self._log(ERROR, "[{0}] : invalid assignment to constant '{1}'".format(action_name, working_stack))

            # consume the operator :=
            token = input_list.pop(0)
            operator = self._operator_table.retrieve(token.type, equal_level_only=False)
            if not operator:
                raise SystemError("Operator table not working correctly")
            working_stack.append(operator)

            # process the expression
            expression_stack = self._internal_compile(input_list.pop(), [])

            if expression_stack:

                # check type compatibility
                expression_type = self._perform_type_check(action_name, working_stack + expression_stack)

                #TODO: if the assignment is to a string variable, need to check the string being assigned is compatible with the variable dimension.

                # push the expression to the working stack
                g = GenericExpression.from_list(expression_stack)
                g.type = expression_type
                working_stack.append(g)

                # generate the intermediate code
                self._ic.init(action_name)
                self._ic.push(working_stack)
                self._ic.flush()

                self._log(DEBUG, "[{0}] : {1}".format(action_name, working_stack))

        return working_stack


    def _expression(self, action_name, token_list, working_stack):
        # process expressions in assignments
        # this is called from other actions and therefore it does not create its own action on the intermediate code
        # it also does not need to flush the intermediate code. this will be done in another action.
        for token in token_list:
            if isinstance(token, Tree):

                working_stack = self._internal_compile(token, working_stack)

            elif isinstance(token, Token):

                # assuming token is an identifier, attempt to retrieve from the symbol table at any level
                a_symbol = self._symbol_table.retrieve(token.value, equal_level_only=False)

                if not a_symbol:
                    # attempt to retrieve from the symbol table at any current level but based on token type
                    a_symbol = self._symbol_table.retrieve(token.type, equal_level_only=False)

                    if not a_symbol:
                        if token.type in ["UNSIGNED_DECIMAL", "SIGNED_DECIMAL", "NUMBER_BINARY", "NUMBER_OCTAL",
                                          "NUMBER_HEXADECIMAL", "UNSIGNED_REAL", "SIGNED_REAL"]:
                            a_symbol = NumericLiteral.from_token(token)

                        elif token.type in ["CHARACTER", "STRING_VALUE"]:
                            a_symbol = StringLiteral.from_token(token)

                        elif token_is_an_operator(token) or token.type in ["LEFT_PARENTHESES", "RIGHT_PARENTHESES"]:
                            a_symbol = self._operator_table.retrieve(token.type, equal_level_only=False)
                            if not a_symbol:
                                raise SystemError("Operator table not working correctly")

                        else:
                            msg = "[{0}] invalid symbol '{1}' used in expression"
                            self._log(ERROR, msg.format(action_name, token.type))

                working_stack.append(a_symbol)

            else:
                raise NotImplementedError("expected a Token or a Tree but received '{0}'".format(token))

        return working_stack


    def _repeat_statement(self, action_name, input_list, working_stack):
        """
        REPEAT_STATEMENT
        input_list will have:
            REPEAT
                statement;
                statement;
                ...
            UNTIL
            expression	True
        """
        # generate the intermediate code
        self._ic.init(action_name)
        working_stack = []

        # process reserved word REPEAT
        keyword = Keyword.from_token(input_list.pop(0))
        working_stack.append(keyword)
        self._ic.push(working_stack)
        self._ic.flush()
        self._log(DEBUG, "[{0}] {1}".format(action_name, working_stack))

        # process statements
        working_stack = []
        while True:
            token = input_list.pop(0)
            if isinstance(token, Token) and token.type == "RESERVED_STATEMENT_UNTIL":
                keyword = Keyword.from_token(token)
                working_stack.append(keyword)
                break
            else:
                self._internal_compile(token, [])

        # switch the action name to match the UNTIL part of the REPEAT
        action_name = action_name + "_UNTIL"

        # process expression after UNTIL
        expression_stack = self._internal_compile(input_list.pop(0), [])

        # check type compatibility of the expression and ensure it returns a boolean type
        expression_type = self._perform_type_check(action_name, expression_stack)
        if not expression_type == BasicType.reserved_type_boolean():
            msg = "[{0}] expected boolean expression but found: {1}"
            self._log(ERROR, msg.format(action_name, expression_type))

        # append the generic expression to the stack
        g = GenericExpression.from_list(expression_stack)
        g.type = expression_type
        working_stack.append(g)

        # generate the intermediate code
        self._ic.init(action_name)
        self._ic.push(working_stack)
        self._ic.flush()
        self._log(DEBUG, "[{0}] {1}".format(action_name, working_stack))

        return working_stack


    def _closed_for_statement(self, action_name, input_list, working_stack):
        """
        CLOSED_FOR_STATEMENT
        input_list will have: FOR identifier := Tree(expression) TO/DOWNTO Tree(expression) DO BEGIN Tree(assignment_statement END
        expression is a Tree of multiple objects
        assignment_statement is a Tree of multiple objects
        """
        working_stack = []

        # process reserved word FOR
        keyword = Keyword.from_token(input_list.pop(0))
        working_stack.append(keyword)

        # process the control variable (or expression)
        control_variable_stack = self._internal_compile(input_list.pop(0), [])
        working_stack = working_stack + control_variable_stack

        # consume the operator :=
        token = input_list.pop(0)
        operator = self._operator_table.retrieve(token.type, equal_level_only=False)
        if not operator:
            raise SystemError("Operator table not working correctly")

        control_variable_stack.append(operator)
        working_stack.append(operator)

        # process the 'initial_value' (or expression) on the for
        expression_stack = self._internal_compile(input_list.pop(0), [])

        # check type compatibility of the control_variable := expression(initial_value)
        expression_type = self._perform_type_check(action_name, control_variable_stack + expression_stack)
        if not expression_type == BasicType.reserved_type_integer():
            msg = "[{0}] expected integer expression but found: {1}"
            self._log(ERROR, msg.format(action_name, expression_type))

        # append the generic expression to the stack
        g = GenericExpression.from_list(expression_stack)
        g.type = expression_type
        working_stack.append(g)

        # emit reserved word to / downto
        keyword = Keyword.from_token(input_list.pop(0))
        working_stack.append(keyword)

        # process the 'final_value' on the for
        expression_stack = self._internal_compile(input_list.pop(0), [])

        # check compatibility of the control_variable := expression(final_value)
        expression_type = self._perform_type_check(action_name, control_variable_stack + expression_stack)
        if not expression_type == BasicType.reserved_type_integer():
            msg = "[{0}] expected integer expression but found: {1}"
            self._log(ERROR, msg.format(action_name, expression_type))

        # append the generic expression to the stack
        g = GenericExpression.from_list(expression_stack)
        g.type = expression_type
        working_stack.append(g)

        # emit reserved word do
        keyword = Keyword.from_token(input_list.pop(0))
        working_stack.append(keyword)

        # generate the intermediate code
        self._ic.init(action_name)
        self._ic.push(working_stack)
        self._ic.flush()

        self._log(DEBUG, "[{0}] {1}".format(action_name, working_stack))

        # process statements nested inside the for
        return self._internal_compile(input_list.pop(0), [])

    def _closed_while_statement(self, action_name, input_list, working_stack):
        """
        CLOSED_WHILE_STATEMENT
        input_list will have: WHILE expression DO Tree(compound_statement)
        expression is a Tree of multiple objects
        compound_statement is a Tree of multiple objects
        """
        working_stack = []

        # process reserved word WHILE
        keyword = Keyword.from_token(input_list.pop(0))
        working_stack.append(keyword)

        # process control expression
        expression_stack = self._internal_compile(input_list.pop(0), [])

        # check type compatibility of the expression and ensure it returns a boolean type
        expression_type = self._perform_type_check(action_name, expression_stack)
        if not expression_type == BasicType.reserved_type_boolean():
            msg = "[{0}] expected boolean expression but found: {1}"
            self._log(ERROR, msg.format(action_name, expression_type))

        # append the generic expression to the stack
        g = GenericExpression.from_list(expression_stack)
        g.type = expression_type
        working_stack.append(g)

        # emit reserved word do
        keyword = Keyword.from_token(input_list.pop(0))
        working_stack.append(keyword)

        # generate the intermediate code
        self._ic.init(action_name)
        self._ic.push(working_stack)
        self._ic.flush()

        self._log(DEBUG, "[{0}] {1}".format(action_name, working_stack))

        # process statements nested inside the while
        return self._internal_compile(input_list.pop(0), [])

    def _type_definition_part(self, action_name, input_list, working_stack):
        """
        TYPE DEFINITION PART

        input_list -> TYPE  (T1 = INTEGER) (T2 = ^ REAL) (T3 = T1)
        """
        # initialise the intermediate code engine
        self._ic.init(action_name)

        # discard reserved word TYPE
        input_list.pop(0)

        # process declarations
        for type_definition in input_list:

            self._internal_compile(type_definition)

        # generate the intermediate code
        self._ic.flush()


    def _type_definition(self, action_name, input_list, working_stack):
        """
        TYPE_DEFINITION
        input_list -> [T1 = ^ INTEGER]
        """
        # check if this type declaration involves a pointer
        is_pointer = input_list[2].type == "OPERATOR_UPARROW"
        """
        the type definition has 3 parts:
            identifier i.e. 'T1'
            operator i.e '='
            type_identifier, i.e. INTEGER
        """
        identifier = input_list[0].value
        operator = Operator.from_token(input_list[1])
        type_identifier = input_list[-1].value

        # identifier - it must NOT exist in the symbol_table yet
        if self._symbol_table.contains(identifier, equal_level_only=False):
            msg = "[{0}] identifier '{1}' already declared in current scope"
            self._log(ERROR, msg.format(action_name, identifier))

        else:

            # type_identifier - it must exist in the symbol table
            type_symbol = self._symbol_table.retrieve(type_identifier, equal_level_only=False)
            if type_symbol:

                # at this point we know:
                # the type being declared is pointer or not
                # the type being declared references a custom or a basic type
                # the name for the type being declared
                #
                # if the type_symbol is itself a pointer, than the variable being declared must be a pointer too
                is_pointer = is_pointer or isinstance(type_symbol, PointerType)
                type_class = BasicType
                if is_pointer:
                    type_class = PointerType

                new_type_symbol = type_class(identifier, type_symbol.type, None)

                # push the new type to the symbol_table
                self._symbol_table.append(new_type_symbol)

                # push the new variable into the intermediate_code engine
                self._ic.push(new_type_symbol)

                # log successful declaration
                self._log(DEBUG, "[{0}] new type defined {1}".format(action_name, new_type_symbol))

            else:

                msg = "[{0}] reference to unknown type '{1}'"
                self._log(ERROR, msg.format(action_name, type_identifier))

        return working_stack

    def _procedure_call(self, action_name, input_list, working_stack):
        """
        PROCEDURE_CALL
        input_list -> [IDENTIFIER, LEFT_PARENTHESES, Tree(actual_parameter(Tree expression), COMMA, Tree(expression), ... RIGHT_PARENTHESES]
        """
        working_stack = []

        # retrieve the actual procedure identifier from the symbol_table
        token = input_list.pop(0)
        identifier = self._symbol_table.retrieve(token.value, equal_level_only=False)
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
                    expression_type = self._perform_type_check(action_name, value_to_print_stack)

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
                    generic_expression.type = expression_type

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

            self._log(DEBUG, "[{0}] {1} {2} {3}".format(action_name, identifier, parameters_counter, working_stack))

        else:

            msg = "[{0}] {1} :  Unknown procedure '{1}' referenced."
            self._log(ERROR, msg.format(action_name, token.value))

        return working_stack

    def _closed_if_statement(self, action_name, input_list, working_stack):
        """
        _closed_if_statement
        input_list -> [Token(RESERVED_STATEMENT_IF, 'if'),
                        Tree(expression, [...]),
                       Token(RESERVED_STATEMENT_THEN, 'then'),
                        Tree(compound_statement, [...]
                       Token(RESERVED_STATEMENT_ELSE, 'else'),
                        Tree(compound_statement, [...]
                      ]
        """
        working_stack = []

        # process reserved word IF
        keyword = Keyword.from_token(input_list.pop(0))
        working_stack.append(keyword)

        # process boolean expression
        expression_stack = self._internal_compile(input_list.pop(0), [])

        # check type compatibility of the expression and ensure it returns a boolean type
        expression_type = self._perform_type_check(action_name, expression_stack)
        if not expression_type == BasicType.reserved_type_boolean():
            msg = "[{0}] expected boolean expression but found: {1}"
            self._log(ERROR, msg.format(action_name, expression_type))

        # store the expression on the stack
        g = GenericExpression.from_list(expression_stack)
        g.type = expression_type
        working_stack.append(g)

        # process reserved word THEN
        keyword = Keyword.from_token(input_list.pop(0))
        working_stack.append(keyword)

        # generate the intermediate code
        self._ic.init(action_name)
        self._ic.push(working_stack)
        self._ic.flush()
        self._log(DEBUG, "[{0}] {1}".format(action_name, working_stack))

        # process statements after IF and before ELSE
        token = input_list.pop(0)
        self._internal_compile(token, [])

        # switch the action name to match the ELSE part of the IF
        action_name = action_name + "_ELSE"

        # process reserved word ELSE
        working_stack = []
        keyword = Keyword.from_token(input_list.pop(0))
        working_stack.append(keyword)

        # generate the intermediate code
        self._ic.init(action_name)
        self._ic.push(working_stack)
        self._ic.flush()
        self._log(DEBUG, "[{0}] {1}".format(action_name, working_stack))

        # process statements after ELSE
        token = input_list.pop(0)
        self._internal_compile(token, [])

        return working_stack

