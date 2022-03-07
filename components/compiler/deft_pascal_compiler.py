"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from lark import Tree, Token
from components.deft_pascal_parser_3 import DeftPascalParser
from components.symbol_table import SymbolTable
from components.symbols.base_symbols import BaseKeyword, BaseExpression
from components.symbols.operator_symbols import Operator, BinaryOperator, UnaryOperator, NeutralOperator
from components.symbols.identifier_symbols import Identifier, TypeIdentifier, \
    ProcedureIdentifier, InBuiltProcedureWrite, ProcedureExternalIdentifier, ProcedureForwardIdentifier, \
    ConstantIdentifier, \
    FunctionIdentifier, FunctionExternalIdentifier, FunctionForwardIdentifier
from components.symbols.literals_symbols import BooleanLiteral, NilLiteral, NumericLiteral, StringLiteral
from components.symbols.type_symbols import PointerType, BasicType, StringType
from components.symbols.expression_symbols import ConstantExpression, IntegerExpression, BooleanExpression
from components.intermediate_code import IntermediateCode
from components.parameters import ActualParameter, FormalParameter

import copy
import logging


_LOG_ROLL_ = {"ERROR": [],
              "WARNING": [],
              "INFO": [],
              "DEBUG": []
              }


class LogRequestsHandler(logging.Handler):
    def emit(self, record):
        """Record any errors raised by the compiler.
        """
        msg = record.getMessage()
        _LOG_ROLL_[record.levelname.upper()].append(msg)

        #if record.levelname.upper() == "ERROR":
        #    _LOG_ROLL_["error"].append(msg)


_MODULE_LOGGER_ = logging.getLogger("deft_pascal_reborn")
_MODULE_LOGGER_.addHandler(LogRequestsHandler())
_MODULE_LOGGER_.setLevel(logging.DEBUG)


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
        #self._stack_begin = []
        #self._stack_end = []

        # self._error_list = []

        self._actions = {"PROGRAM_HEADING",
                         "LABEL_DECLARATION_PART",
                         "CONSTANT_DEFINITION_PART",
                         "CONSTANT_DEFINITION",
                         "CONSTANT_EXPRESSION",
                         "CONSTANT_ACCESS",
                         "TYPE_DEFINITION_PART",
                         "TYPE_DEFINITION",
                         "VARIABLE_DECLARATION_PART",
                         "VARIABLE_DECLARATION",
                         "VARIABLE_ACCESS",
                         "RESERVED_STRUCTURE_BEGIN",
                         "RESERVED_STRUCTURE_END",
                         "ASSIGNMENT_STATEMENT",
                         "PROCEDURE_CALL",
                         "PROCEDURE_DECLARATION",
                         "FUNCTION_DECLARATION",
                         "PROCEDURE_DECLARATION_WITH_DIRECTIVE",
                         "FUNCTION_DECLARATION_WITH_DIRECTIVE",
                         "EXPRESSION",
                         "CLOSED_FOR_STATEMENT",
                         "OPEN_FOR_STATEMENT",
                         "CLOSED_WHILE_STATEMENT",
                         "REPEAT_STATEMENT",
                         "COMPOUND_STATEMENT",
                         "CLOSED_IF_STATEMENT",
                         "OPEN_IF_STATEMENT"
                         }


    def check_syntax(self, input_program):
        error_list = self._parser.parse(input_program)
        if not error_list:
            self._ast = self._parser.ast
        else:
            self._ast = None

        _LOG_ROLL_["ERROR"].clear()
        _LOG_ROLL_["WARNING"].clear()
        _LOG_ROLL_["DEBUG"].clear()
        _LOG_ROLL_["INFO"].clear()

        _LOG_ROLL_["ERROR"] = error_list

        return _LOG_ROLL_

    def compile(self, ast=None):
        if not ast and not self._ast:
            raise ValueError("AST is not yet defined")

        if not ast and self._ast:
            ast = self._ast

        _LOG_ROLL_["ERROR"].clear()
        _LOG_ROLL_["WARNING"].clear()
        _LOG_ROLL_["DEBUG"].clear()
        _LOG_ROLL_["INFO"].clear()

        # _LOG_ROLL_.clear()
        for i in ast.children:
            self._internal_compile(i, [])

        return _LOG_ROLL_

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

    #def _log(self, log_type=INFO, log_info=""):
    #    pass
        # emit log
        # msg = "[{0}/{1}] {2}".format(self._symbol_table.current_scope, self._symbol_table.current_level, log_info)
        # if log_type == ERROR:
        #     # self._error_list.append(msg)
        #     _MODULE_LOGGER_.error(msg)
        # elif log_type == WARNING:
        #     _MODULE_LOGGER_.warning(msg)
        # elif log_type == INFO:
        #     _MODULE_LOGGER_.info(msg)
        # else:
        #     _MODULE_LOGGER_.debug(msg)

    def _compile_tree(self, a_tree, working_stack):
        action_name = a_tree.data.upper()
        if action_name in self._actions:
            method_to_call = getattr(DeftPascalCompiler, "_" + action_name.lower())
            return method_to_call(self, action_name, a_tree.children, working_stack)
        else:
            _MODULE_LOGGER_.error("action '{0}' not yet implemented for tree {1}".format(a_tree.data.upper(), a_tree))
            return working_stack


    def _compile_token(self, a_token, working_stack):
        action_name = a_token.type.upper()
        if action_name in self._actions:
            method_to_call = getattr(DeftPascalCompiler, "_" + action_name.lower())
            return method_to_call(self, action_name, a_token, working_stack)
        else:
            _MODULE_LOGGER_.error("action '{0}' not yet implemented for token {1}".format(a_token.type.upper(), a_token.value.upper()))
            return working_stack


    def _internal_compile(self, ast, working_stack):
        if isinstance(ast, Tree):
            if len(ast.children) > 0:
                return self._compile_tree(ast, working_stack)
        elif isinstance(ast, Token):
            return self._compile_token(ast, working_stack)
        else:
            _MODULE_LOGGER_.error('Error - unknown AST object {0}'.format(ast))
            raise TypeError


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

        # add the in-built procedures to the symbol table
        self._symbol_table.append(InBuiltProcedureWrite.in_built_procedure_write())
        self._symbol_table.append(InBuiltProcedureWrite.in_built_procedure_writeln())

        # add all operators to the operator table
        self._operator_table.append(BinaryOperator.operator_multiply())
        self._operator_table.append(BinaryOperator.operator_plus())
        self._operator_table.append(BinaryOperator.operator_minus())
        self._operator_table.append(BinaryOperator.operator_divide())
        self._operator_table.append(BinaryOperator.operator_div())
        self._operator_table.append(BinaryOperator.operator_mod())
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
        #self._stack_begin.append(self._GLB_MAIN_BEGIN)
        #self._stack_end.append(self._GLB_MAIN_END)

        # initialise the intermediate_code engine
        self._ic.init(action_name)

        # push intermediate code
        self._ic.push(token_list[0])
        self._ic.push(token_list[1])
        self._ic.flush()

        if len(token_list) > 2:
            _MODULE_LOGGER_.warning("[{0}] variables detected - all will be ignored".format(action_name))


    def _compound_statement(self, action_name, input_list, working_stack):
        """
        COMPOUND_STATEMENT
        input_list -> BEGIN Tree() Tree() Tree() ... END
        """
        while input_list:
            self._internal_compile(input_list.pop(0), working_stack)


    def _reserved_structure_begin(self, action_name, input_token, working_stack):
        """
        RESERVED_STRUCTURE_BEGIN
        currently implemented as a token.
        """
        if self._symbol_table.current_level == 2:
            action = self._GLB_MAIN_BEGIN
        else:
            action = self._GLB_BLOCK_BEGIN

        #action = self._stack_begin.pop(-1)
        #self._stack_begin.append(self._GLB_BLOCK_BEGIN)
        #if not action == self._GLB_MAIN_BEGIN:
        #    self._stack_end.append(self._GLB_BLOCK_END)

        self._ic.init(action)
        self._ic.push(input_token)
        self._ic.flush()


    def _reserved_structure_end(self, action_name, input_token, working_stack):
        """
        RESERVED_STRUCTURE_END
        currently implemented as a token.
        """
        if self._symbol_table.current_level == 2:
            action = self._GLB_MAIN_END
        else:
            action = self._GLB_BLOCK_END

        self._ic.init(action)
        self._ic.push(input_token)
        self._ic.flush()

        if action == self._GLB_MAIN_END:
            for i in self._symbol_table.instances_of(ProcedureForwardIdentifier):
                _MODULE_LOGGER_.error("unresolved forward reference to '{0}'".format(i))


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

            self._internal_compile(constant_definition, [])

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
            _MODULE_LOGGER_.error("[{0}] constant identifier '{1}' already declared ".format(action_name, constant_identifier))

        else:
            # discard the operator =
            input_list.pop(0)

            # process the constant_expression (literals)
            stack = self._internal_compile(input_list.pop(0), [])
            if stack:
                expression = ConstantExpression.from_list(stack)
                if expression is None:
                    msg = "[{0}] incompatible types in expression: {1}"
                    _MODULE_LOGGER_.error(msg.format(action_name, expression))

                else:
                    new_constant = ConstantIdentifier(constant_identifier, expression)

                    # constant - its value must not exceed the types available in the target environment
                    compliant = new_constant.complies_to_type_restrictions()
                    if compliant is None:
                        _MODULE_LOGGER_.warning("[{0}] constant expression '{1}' cannot be validated at compilation".format(action_name, constant_identifier))
                        compliant = True

                    if compliant:
                        # push the new constant into the symbol_table
                        self._symbol_table.append(new_constant)

                        # push the new constant into the intermediate_code engine
                        self._ic.push(new_constant)

                        # log successful declaration
                        _MODULE_LOGGER_.debug("[{0}] new constant declared : {1}".format(action_name, new_constant))

                    else:
                        _MODULE_LOGGER_.error("[{0}] constant '{1}' not compatible with type limitations".format(action_name, new_constant))

            else:
                _MODULE_LOGGER_.error("[{0}] invalid expression in definition of constant '{1}'".format(action_name, constant_identifier))

        return working_stack


    def _constant_expression(self, action_name, input_list, working_stack):
        """
        CONSTANT_EXPRESSION == 'AN EXPRESSION OF LITERALS'
        process constant expressions
        this is called from other actions and therefore it does not create its own action on the intermediate code
        it also does not need to flush the intermediate code. this will be done in another action.
        """
        """
        FreePascal rule: The compiler must be able to evaluate the expression in a constant declaration at compile time. 
        This means that most of the functions in the Run-Time library cannot be used in a constant declaration. 
        Operators such as +, -, *, /, not, and, or, div, mod, ord, chr, sizeof, pi, int, trunc, round, frac, odd can be 
        used, however.
        """
        # TODO: Check the expression to ensure no PROCEDURE OR FUNCTION references are included.
        return self._expression(action_name, input_list, working_stack)


    def _constant_access(self, action_name, input_list, working_stack):
        """
        input_list -> [Token(IDENTIFIER, 'C2')]
        This method will push the identifier to the expression stack and intermediate code stack
        """
        identifier_name = input_list[0].value

        # identifier - it must exist in the symbol table
        identifier_symbol = self._symbol_table.retrieve(identifier_name, equal_level_only=False)

        if identifier_symbol:
            working_stack.append(identifier_symbol)

        else:
            msg = "[{0}] :  Reference to undeclared constant '{1}'"
            _MODULE_LOGGER_.error(msg.format(action_name, identifier_name))

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

            self._internal_compile(variable_declaration, [])

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

        # type_identifier = input_list.pop().value.upper()
        type_identifier = input_list.pop()
        if type_identifier.type == "IDENTIFIER":
            # identifier is of a custom type and their definition is case sensitive/relevant
            type_identifier = type_identifier.value
        else:
            # identifier is a basic type and those are stored in the symbol table as uppercase
            type_identifier = type_identifier.value.upper()

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
                type_symbol = PointerType.for_type(type_symbol)
                # type_symbol.type = aux

            # process each identifier for the given variable_type
            for token in input_list:

                if not token.type == "COMMA":

                    identifier = token.value

                    # identifier - it must not exist in the symbol_table yet
                    if self._symbol_table.contains(identifier, equal_level_only=False):

                        msg = "[{0}] identifier '{1}' already declared."
                        _MODULE_LOGGER_.error(msg.format(action_name, identifier))

                    else:

                        new_variable = Identifier(identifier, type_symbol, None)

                        # push the new variable into the symbol_table
                        self._symbol_table.append(new_variable)

                        # push the new variable into the intermediate_code engine
                        self._ic.push(new_variable)

                        # log successful declaration
                        _MODULE_LOGGER_.debug("[{0}] new identifier declared : {1}".format(action_name, new_variable))

        else:

            msg = "[{0}] unknown type '{1}' reference in declaration."
            _MODULE_LOGGER_.error(msg.format(action_name, type_identifier))


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
            _MODULE_LOGGER_.error('Error - unknown AST object {0}'.format(input_list))
            raise TypeError

        # identifier - it must exist in the symbol table
        identifier_symbol = self._symbol_table.retrieve(identifier_name, equal_level_only=False)

        if identifier_symbol:
            working_stack.append(identifier_symbol)
            if operator_symbol:
                working_stack.append(operator_symbol)

        else:
            msg = "[{0}] :  Reference to undeclared variable '{1}'"
            _MODULE_LOGGER_.error(msg.format(action_name, identifier_name))

        return working_stack


    def _label_declaration_part(self, action_name, input_list, working_stack):
        """
        process LABEL_DECLARATION_PART
        """
        _MODULE_LOGGER_.warning("[{0}] - all will be ignored".format(action_name))


    def _assignment_statement(self, action_name, input_list, working_stack):
        """
        ASSIGNMENT_STATEMENT
        [Tree(variable_access, [IDENTIFIER]), OPERATOR_ASSIGNMENT, Tree(expression, [Token(UNSIGNED_DECIMAL, '0')])])
        token_list -> identifier := expression
        """
        # process the identifier
        working_stack = self._internal_compile(input_list.pop(0), [])

        if working_stack:

            # the working stack can contain only the variable or variable and dereference operator.
            # the identifier is always at position 0
            identifier = working_stack[0]

            # check the identifier receiving the assignment is variable.
            if isinstance(identifier, ConstantIdentifier):
                _MODULE_LOGGER_.error("[{0}] : invalid assignment to constant '{1}'".format(action_name, working_stack))

            # consume the operator :=
            token = input_list.pop(0)
            operator = self._operator_table.retrieve(token.type, equal_level_only=False)
            if not operator:
                raise SystemError("Operator table not working correctly")
            working_stack.append(operator)

            # process the expression
            expression_stack = self._internal_compile(input_list.pop(), [])

            if expression_stack:

                expression = BaseExpression.from_list(working_stack + expression_stack)
                if expression is None:
                    msg = "[{0}] incompatible types in expression: {1}"
                    _MODULE_LOGGER_.error(msg.format(action_name, expression))

                else:
                    expression = BaseExpression.from_list(expression_stack)
                    # check type compatibility
                    # expression_type = self._perform_type_check(action_name, working_stack + expression_stack)

                    #TODO: if the assignment is to a string variable, need to check the string being assigned is compatible with the variable dimension.

                    # push the expression to the working stack
                    # g = BaseExpression.from_list(expression_stack)
                    # g.type = expression_type
                    working_stack.append(expression)

                    # generate the intermediate code
                    self._ic.init(action_name)
                    self._ic.push(working_stack)
                    self._ic.flush()

                    _MODULE_LOGGER_.debug("[{0}] : {1}".format(action_name, working_stack))

        return working_stack


    def _expression(self, action_name, token_list, working_stack):
        # process expressions in assignments
        # this is called from other actions and therefore it does not create its own action on the intermediate code
        # it also does not need to flush the intermediate code. this will be done in another action.
        for token in token_list:
            if isinstance(token, Tree):
                working_stack = self._internal_compile(token, working_stack)

            elif isinstance(token, Token):
                a_symbol = self._symbol_table.retrieve(token.value, equal_level_only=False)
                if not a_symbol:

                    a_symbol = self._symbol_table.retrieve(token.type, equal_level_only=False)
                    if not a_symbol:

                        a_symbol = self._operator_table.retrieve(token.type, equal_level_only=False)
                        if not a_symbol:

                            if token.type in ["UNSIGNED_DECIMAL", "SIGNED_DECIMAL", "NUMBER_BINARY", "NUMBER_OCTAL",
                                              "NUMBER_HEXADECIMAL", "UNSIGNED_REAL", "SIGNED_REAL"]:
                                a_symbol = NumericLiteral.from_token(token)
                                if not a_symbol:
                                    _MODULE_LOGGER_.error("[{0}] literal '{1}' not compatible with type limitations".format(action_name, token))

                            elif token.type in ["CHARACTER", "STRING_VALUE"]:
                                a_symbol = StringLiteral.from_token(token)
                                if not a_symbol:
                                    _MODULE_LOGGER_.error("[{0}] literal '{1}' not compatible with type limitations".format(action_name, token))

                            else:
                                msg = "[{0}] unknown symbol '{1}' used in expression"
                                _MODULE_LOGGER_.error(msg.format(action_name, token.type))

                if a_symbol:
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
        keyword = BaseKeyword.from_token(input_list.pop(0))
        working_stack.append(keyword)
        self._ic.push(working_stack)
        self._ic.flush()
        _MODULE_LOGGER_.debug("[{0}] {1}".format(action_name, working_stack))

        # process statements
        working_stack = []
        while True:
            token = input_list.pop(0)
            if isinstance(token, Token) and token.type == "RESERVED_STATEMENT_UNTIL":
                keyword = BaseKeyword.from_token(token)
                working_stack.append(keyword)
                break
            else:
                self._internal_compile(token, [])

        # switch the action name to match the UNTIL part of the REPEAT
        action_name = action_name + "_UNTIL"

        # process expression after UNTIL
        expression_stack = self._internal_compile(input_list.pop(0), [])
        expression = BooleanExpression.from_list(expression_stack)

        if expression is None:
            msg = "[{0}] expected boolean expression but found: {1}"
            _MODULE_LOGGER_.error(msg.format(action_name, expression_stack))

        else:
            working_stack.append(expression)

            # generate the intermediate code
            self._ic.init(action_name)
            self._ic.push(working_stack)
            self._ic.flush()

            _MODULE_LOGGER_.debug("[{0}] {1}".format(action_name, working_stack))

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
        keyword = BaseKeyword.from_token(input_list.pop(0))
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
        expression = IntegerExpression.from_list(control_variable_stack + expression_stack)

        if expression is None:
            msg = "[{0}] expected integer expression but found: {1}"
            _MODULE_LOGGER_.error(msg.format(action_name, expression_stack))

        else:
            expression = IntegerExpression.from_list(expression_stack)
            working_stack.append(expression)

        # emit reserved word to / downto
        keyword = BaseKeyword.from_token(input_list.pop(0))
        working_stack.append(keyword)

        # process the 'final_value' on the for
        expression_stack = self._internal_compile(input_list.pop(0), [])
        expression = IntegerExpression.from_list(control_variable_stack + expression_stack)

        if expression is None:
            msg = "[{0}] expected integer expression but found: {1}"
            _MODULE_LOGGER_.error(msg.format(action_name, expression_stack))

        else:
            expression = IntegerExpression.from_list(expression_stack)
            working_stack.append(expression)

        # emit reserved word do
        keyword = BaseKeyword.from_token(input_list.pop(0))
        working_stack.append(keyword)

        # generate the intermediate code
        self._ic.init(action_name)
        self._ic.push(working_stack)
        self._ic.flush()

        _MODULE_LOGGER_.debug("[{0}] {1}".format(action_name, working_stack))

        # process statements nested inside the for
        self._increase_scope(action_name)
        result = self._internal_compile(input_list.pop(0), [])
        self._decrease_scope()
        return result

    def _open_for_statement(self, action_name, input_list, working_stack):
        """
        OPEN_FOR_STATEMENT
        input_list will have: FOR identifier := Tree(expression) TO/DOWNTO Tree(expression) DO BEGIN Tree(assignment_statement END
        expression is a Tree of multiple objects
        assignment_statement is a Tree of multiple objects
        """
        working_stack = []

        # process reserved word FOR
        keyword = BaseKeyword.from_token(input_list.pop(0))
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
        expression = IntegerExpression.from_list(control_variable_stack + expression_stack)

        if expression is None:
            msg = "[{0}] expected integer expression but found: {1}"
            _MODULE_LOGGER_.error(msg.format(action_name, expression_stack))

        else:
            expression = IntegerExpression.from_list(expression_stack)
            working_stack.append(expression)

        # emit reserved word to / downto
        keyword = BaseKeyword.from_token(input_list.pop(0))
        working_stack.append(keyword)

        # process the 'final_value' on the for
        expression_stack = self._internal_compile(input_list.pop(0), [])
        expression = IntegerExpression.from_list(control_variable_stack + expression_stack)

        if expression is None:
            msg = "[{0}] expected integer expression but found: {1}"
            _MODULE_LOGGER_.error(msg.format(action_name, expression_stack))

        else:
            expression = IntegerExpression.from_list(expression_stack)
            working_stack.append(expression)

        # emit reserved word do
        keyword = BaseKeyword.from_token(input_list.pop(0))
        working_stack.append(keyword)

        # generate the intermediate code
        self._ic.init(action_name)
        self._ic.push(working_stack)
        self._ic.flush()

        _MODULE_LOGGER_.debug("[{0}] {1}".format(action_name, working_stack))

        # process statements nested inside the for
        self._increase_scope(action_name)
        result = self._internal_compile(input_list.pop(0), [])
        self._decrease_scope()
        return result

    def _closed_while_statement(self, action_name, input_list, working_stack):
        """
        CLOSED_WHILE_STATEMENT
        input_list will have: WHILE expression DO Tree(compound_statement)
        expression is a Tree of multiple objects
        compound_statement is a Tree of multiple objects
        """
        working_stack = []

        # process reserved word WHILE
        keyword = BaseKeyword.from_token(input_list.pop(0))
        working_stack.append(keyword)

        # process control expression
        expression_stack = self._internal_compile(input_list.pop(0), [])
        expression = BooleanExpression.from_list(expression_stack)

        if expression is None:
            msg = "[{0}] expected boolean expression but found: {1}"
            _MODULE_LOGGER_.error(msg.format(action_name, expression_stack))

        else:
            working_stack.append(expression)

        # emit reserved word do
        keyword = BaseKeyword.from_token(input_list.pop(0))
        working_stack.append(keyword)

        # generate the intermediate code
        self._ic.init(action_name)
        self._ic.push(working_stack)
        self._ic.flush()

        _MODULE_LOGGER_.debug("[{0}] {1}".format(action_name, working_stack))

        # process statements nested inside the while
        self._increase_scope(action_name)
        result = self._internal_compile(input_list.pop(0), [])
        self._decrease_scope()
        return result


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

            self._internal_compile(type_definition, [])

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
            _MODULE_LOGGER_.error(msg.format(action_name, identifier))

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

                # TODO: Address the pointer type definition

                new_type_symbol = TypeIdentifier(identifier, type_symbol)
                # new_type_symbol = type_class(identifier, type_symbol.type, None)

                # push the new type to the symbol_table
                self._symbol_table.append(new_type_symbol)

                # push the new variable into the intermediate_code engine
                self._ic.push(new_type_symbol)

                # log successful declaration
                _MODULE_LOGGER_.debug("[{0}] new type defined {1}".format(action_name, new_type_symbol))

            else:

                msg = "[{0}] reference to unknown type '{1}'"
                _MODULE_LOGGER_.error(msg.format(action_name, type_identifier))

        return working_stack

    def _procedure_call(self, action_name, input_list, working_stack):
        """
        PROCEDURE_CALL
        input_list -> [IDENTIFIER, LEFT_PARENTHESES, Tree(actual_parameter(Tree expression), COMMA, Tree(expression), ... RIGHT_PARENTHESES]
        """
        working_stack = []

        # retrieve the actual procedure identifier from the symbol_table
        token = input_list.pop(0)

        # ensure in built procedures use a lowercase name
        if token.value.upper() in ["WRITE", "WRITELN"]:
            token.value = token.value.lower()

        identifier = self._symbol_table.retrieve(token.value, equal_level_only=False)
        if identifier:
            # push the identifier to the working stack
            working_stack.append(identifier)

            # discard the open and close parentheses operands
            input_list.pop(0)
            input_list.pop(-1)

            # calculate the number of parameters in the procedure call
            parameters_counter = len(input_list) - input_list.count(",")
            if not identifier.accepts_parameters_count(parameters_counter):
                msg = "[{0}] :  '{1}' parameters passed to procedure {2} but '{3}' expected."
                _MODULE_LOGGER_.error(msg.format(action_name, parameters_counter, identifier.name, identifier.argument_counter))

            # process each parameter expression, discard the commas used as separators
            parameter_index = 0
            for token in input_list:
                if isinstance(token, Token):
                    if not token.type == "COMMA":
                        msg = "[{0}] :  Unknown token '{1}' passed in procedure parameter."
                        _MODULE_LOGGER_.error(msg.format(action_name, token))

                elif isinstance(token, Tree):
                    parameter_index = parameter_index + 1

                    value_to_print_stack = self._internal_compile(token.children[0], [])
                    expression_value_to_print = BaseExpression.from_list(value_to_print_stack)

                    expression_field_width = None
                    expression_decimal_field = None

                    if token.data.upper() in ["BINARY_PARAMETER", "TERNARY_PARAMETER"]:
                        temp_stack = self._internal_compile(token.children[1], [])
                        expression_field_width = IntegerExpression.from_list(temp_stack)

                    if token.data.upper() == "TERNARY_PARAMETER":
                        temp_stack = self._internal_compile(token.children[2], [])
                        expression_decimal_field = IntegerExpression.from_list(temp_stack)

                    if (expression_field_width or expression_decimal_field) and identifier.name.upper() not in ["WRITE", "WRITELN"]:
                        msg = "[{0}] Formatting parameters incompatible with {1}}. Formatting will be ignored."
                        _MODULE_LOGGER_.warning(msg.format(action_name, identifier.name))
                        expression_field_width = None
                        expression_decimal_field = None

                    # create the actual parameter
                    parameter = ActualParameter(expression_value_to_print, expression_field_width, expression_decimal_field)

                    if not identifier.is_parameter_compatible(parameter, parameter_index):
                        msg = "[{0}] :  Incompatible parameter '{1}' passed to procedure {2}"
                        _MODULE_LOGGER_.error(msg.format(action_name, parameter, identifier))

                    else:
                        # push to the working stack
                        working_stack.append(parameter)

                else:
                    msg = "[{0}] :  Unknown parameter '{1}' passed to procedure {2}"
                    _MODULE_LOGGER_.error(msg.format(action_name, token, identifier))

            # generate the intermediate code
            self._ic.init(action_name)
            self._ic.push(working_stack)
            self._ic.flush()

            _MODULE_LOGGER_.debug("[{0}] {1} {2} {3}".format(action_name, identifier, parameters_counter, working_stack))

        else:

            msg = "[{0}] {1} :  Unknown procedure '{1}' referenced."
            _MODULE_LOGGER_.error(msg.format(action_name, token.value))

        return working_stack


    def _procedure_declaration(self, action_name, input_list, working_stack):
        return self._generic_procedure_or_function_declaration(action_name, input_list, working_stack)

    def _function_declaration(self, action_name, input_list, working_stack):
        """
         Tree('function_declaration', [Tree('function_heading', "
         "[Token('RESERVED_DECLARATION_FUNCTION', 'FUNCTION'), Token('IDENTIFIER', "
         "'F1'), Tree('formal_parameter_list', [Token('LEFT_PARENTHESES', '('), "
         "Tree('formal_parameter_section_list', [Tree('formal_parameter_section_list', "
         "[Tree('formal_parameter_section', [Tree('value_parameter_specification', "
         "[Token('IDENTIFIER', 'SP1'), Token('IDENTIFIER', 'INTEGER')])])]), "
         "Tree('formal_parameter_section', [Tree('value_parameter_specification', "
         "[Token('IDENTIFIER', 'SP2'), Token('IDENTIFIER', 'BOOLEAN')])])]), "
         "Token('RIGHT_PARENTHESES', ')')]), Tree('result_type', [Token('IDENTIFIER', "
         "'INTEGER')])]), Tree('function_block', [Tree('label_declaration_part', []), "
         "Tree('constant_definition_part', []), Tree('type_definition_part', []), "
         "Tree('variable_declaration_part', []), Tree('compound_statement', "
         "[Token('RESERVED_STRUCTURE_BEGIN', 'BEGIN'), Token('RESERVED_STRUCTURE_END', "
         "'END')])])])
        """
        return self._generic_procedure_or_function_declaration(action_name, input_list, working_stack)

    def _function_declaration_with_directive(self, action_name, input_list, working_stack):
        """
        Example:
        input_list -> [Token('RESERVED_DECLARATION_FUNCTION', 'FUNCTION'),
                       Token('IDENTIFIER', 'first_function'),
                       Tree('parameter_list', [ ... ]),
                       Tree('return_type', [Token('IDENTIFIER', 'TYPE')]),
                       Tree('directive', [Token('RESERVED_STATEMENT_FORWARD', 'FORWARD')])]

        """
        # initialise the intermediate code engine
        self._ic.init(action_name)

        # set the context
        context = input_list.pop(0)
        if context != "FUNCTION":
            raise ValueError("Internal Error - Unknown context '{0}' in action '{1}'".format(context, action_name))

        # the function declaration in hand can be an external or a forward declaration
        # confirm a directive is present and verify its type
        if input_list[-1].data.upper() != "DIRECTIVE":
            raise KeyError("Internal Error - Unexpected keyword '{0}' in action '{1}'".format(input_list[-1].data, action_name))
        else:
            directive = input_list[-1].children[0].value.upper()
            if directive not in ["FORWARD", "EXTERNAL"]:
                raise KeyError("Internal Error - Unknown directive '{0}' in action '{1}'".format(input_list[-1].data, action_name))
            input_list.pop(-1)

        # retrieve the token identifier for the new function
        identifier = input_list.pop(0).value

        # verify if the function identifier has already been declared by checking the symbol table
        symbol = self._symbol_table.retrieve(identifier, equal_level_only=False)
        if symbol:

            msg = "[{0}] {2} '{1}' already declared"
            _MODULE_LOGGER_.error(msg.format(action_name, identifier, context))

        else:

            # a new function is being declared
            if input_list[-1].data.upper() != "RETURN_TYPE":

                raise KeyError("Unexpected keyword '{0}' in action '{1}'".format(input_list[-1].data, action_name))

            else:

                # as we are dealing with a function, a type declaration is expected
                type_identifier = input_list.pop(-1).children

                string_dimension = None
                if type_identifier[-1].type == "RIGHT_PARENTHESES":  # handling the string with dimension special case
                    type_identifier.pop(-1)  # discard the )
                    string_dimension = type_identifier.pop(-1)
                    type_identifier.pop(-1)  # discard the (

                type_identifier = type_identifier[0]
                if type_identifier.type == "IDENTIFIER":
                    # identifier is of a custom type and their definition is case sensitive/relevant
                    type_identifier = type_identifier.value
                else:
                    # identifier is a basic type and those are stored in the symbol table as uppercase
                    type_identifier = type_identifier.value.upper()

                # retrieve the type from the symbol table
                type_symbol = self._symbol_table.retrieve(type_identifier, equal_level_only=False)
                if not type_symbol:

                    msg = "[{0}] unknown type '{1}' used in function declaration."
                    _MODULE_LOGGER_.error(msg.format(action_name, type_identifier))

                else:

                    # handle scenario function returns a string
                    if string_dimension:
                        type_symbol = copy.copy(type_symbol)
                        type_symbol.dimension = string_dimension

                    # with the identifier and type create a new function object
                    if directive == "FORWARD":
                        new_function = FunctionForwardIdentifier(identifier, type_symbol, None)
                    elif directive == "EXTERNAL":
                        new_function = FunctionExternalIdentifier(identifier, type_symbol, None)

                    # add new function to symbol table as we know it is not yet declared
                    self._symbol_table.append(new_function)

                    # push the new function into the intermediate_code engine
                    self._ic.push(new_function)
                    self._ic.flush()

                    # increase scope in preparation for processing the function parameters
                    self._increase_scope(new_function.name)

                    # process the function parameters if those are present
                    if len(input_list) > 0 and input_list[0].data.upper() == "PARAMETER_LIST":

                        argument_list = input_list.pop(0).children

                        # discard open and close parameters characters -> (  )
                        argument_list.pop(0)
                        argument_list.pop(-1)

                        # process each argument
                        for ast in argument_list:
                            if ast.data.upper() == "VALUE_PARAMETER_SPECIFICATION":

                                # process the type of the argument list
                                token = ast.children.pop(-1)
                                if token.type == "IDENTIFIER":
                                    # identifier is of a custom type and their definition is case sensitive/relevant
                                    type_identifier = self._symbol_table.retrieve(token.value, equal_level_only=False)
                                else:
                                    # identifier is a basic type and those are stored in the symbol table as uppercase
                                    type_identifier = self._symbol_table.retrieve(token.value.upper(), equal_level_only=False)

                                if type_identifier:
                                    # process the arguments
                                    for token in ast.children:
                                        if token.type == "IDENTIFIER":
                                            # create the variables using the parameter_type
                                            new_variable = Identifier(token.value, type_identifier, None)

                                            # add the new variable to the symbol_table
                                            self._symbol_table.append(new_variable)

                                            # create the formal parameter
                                            argument = FormalParameter(token.value, type_identifier)

                                            # add the variable as formal argument to the procedure
                                            new_function.add_argument(argument)
                                else:
                                    msg = "[{0}] unknown type '{1}' reference in {2} declaration."
                                    _MODULE_LOGGER_.error(msg.format(action_name, type_identifier, identifier))

                            else:
                                _MODULE_LOGGER_.error("parameter class '{0}' not yet supported".format(ast))

                        # log successful declaration
                        _MODULE_LOGGER_.debug("[{0}] new function declared : {1}".format(action_name, new_function))

                    else:
                        # log successful declaration
                        _MODULE_LOGGER_.debug("[{0}] new function declared : {1}".format(action_name, new_function))

                    self._decrease_scope()

        return working_stack

    def _procedure_declaration_with_directive(self, action_name, input_list, working_stack):
        """
        Example:
            input_list -> [Token(RESERVED_DECLARATION_PROCEDURE, 'PROCEDURE'),
                       Token(IDENTIFIER, 'first_procedure'),
                       Tree(procedure_block, [])
                       OR proc_or_func_directive	forward
                       OR proc_or_func_directive	external
                      ]
        """
        raise NotImplementedError

    def _generic_procedure_or_function_declaration(self, action_name, input_list, working_stack):
        """
        input_list -> [Token(RESERVED_DECLARATION_PROCEDURE, 'PROCEDURE'),
                       Token(IDENTIFIER, 'first_procedure'),
                       Tree(procedure_block, [])
                       OR proc_or_func_directive	forward
                       OR proc_or_func_directive	external
                      ]

        """
        # initialise the intermediate code engine
        self._ic.init(action_name)
        context = action_name.lower().replace("_declaration", "")

        # discard the token reserved word PROCEDURE / FUNCTION
        input_list.pop(0)

        # retrieve the token identifier for the new procedure or function
        identifier = input_list.pop(0).value

        # the procedure or function declaration in hand can be an external, a forward or a standard one
        # this is identified by the token after the identifier.
        # it can be a proc_or_func_directive, a procedure_block or a function_block
        if input_list[-1].data.upper() == "PROC_OR_FUNC_DIRECTIVE":
            if input_list[-1].children[0].value.upper() == "FORWARD":
                if context == "function":
                    pi_class = FunctionForwardIdentifier
                elif context == "procedure":
                    pi_class = ProcedureForwardIdentifier
                else:
                    raise ValueError("Internal Error - Unknown context '{0}' in Forward directive".format(action_name))
            elif input_list[-1].children[0].value.upper() == "EXTERNAL":
                if context == "function":
                    pi_class = FunctionExternalIdentifier
                elif context == "procedure":
                    pi_class = ProcedureExternalIdentifier
                else:
                    raise ValueError("Internal Error - Unknown context '{0}' in External directive".format(action_name))
            else:
                raise KeyError("unexpected keyword '{0}' in proc_or_func_directive".format(input_list[0].value))
            input_list.pop(-1)

        else:
            if context == "function":
                pi_class = FunctionIdentifier
            elif context == "procedure":
                pi_class = ProcedureIdentifier
            else:
                raise ValueError("Internal Error - Unknown context '{0}'".format(action_name))

        pi = pi_class(identifier, 'RESERVED_TYPE_POINTER', None)

        # store procedure identifier in the symbol table
        symbol = self._symbol_table.retrieve(identifier, equal_level_only=False)
        if not symbol:
            self._symbol_table.append(pi)
            _MODULE_LOGGER_.debug("[{0}] new {2} defined {1}".format(action_name, pi, context))

        elif isinstance(symbol, ProcedureForwardIdentifier) or isinstance(symbol, FunctionForwardIdentifier):
            # replace in the symbol_table a forward declaration with the actual declaration
            self._symbol_table.replace(identifier, pi)
            _MODULE_LOGGER_.debug("[{0}] forward {2} '{1}' resolved".format(action_name, identifier, context))

        else:
            msg = "[{0}] {2} '{1}' already declared"
            _MODULE_LOGGER_.error(msg.format(action_name, identifier, context))

        self._ic.push(pi)
        self._ic.flush()

        self._increase_scope(pi.name)

        # process the procedure / function parameters if those are present
        if len(input_list) > 0 and input_list[0].data.upper() == "FORMAL_PARAMETER_LIST":
            argument_list = input_list.pop(0).children

            # discard open and close parameters characters -> (  )
            argument_list.pop(0)
            argument_list.pop(-1)

            # process each argument
            for ast in argument_list:
                if ast.data.upper() == "VALUE_PARAMETER_SPECIFICATION":

                    # process the type of the argument list
                    token = ast.children.pop(-1)
                    if token.type == "IDENTIFIER":
                        # identifier is of a custom type and their definition is case sensitive/relevant
                        type_identifier = self._symbol_table.retrieve(token.value, equal_level_only=False)
                    else:
                        # identifier is a basic type and those are stored in the symbol table as uppercase
                        type_identifier = self._symbol_table.retrieve(token.value.upper(), equal_level_only=False)

                    if type_identifier:
                        # process the arguments
                        for token in ast.children:
                            if token.type == "IDENTIFIER":
                                # create the variables using the parameter_type
                                new_variable = Identifier(token.value, type_identifier, None)

                                # add the new variable to the symbol_table
                                self._symbol_table.append(new_variable)

                                # create the formal parameter
                                argument = FormalParameter(token.value, type_identifier)

                                # add the variable as formal argument to the procedure
                                pi.add_argument(argument)
                    else:
                        msg = "[{0}] unknown type '{1}' reference in {2} declaration."
                        _MODULE_LOGGER_.error(msg.format(action_name, type_identifier, identifier))

                else:
                    _MODULE_LOGGER_.error("parameter class '{0}' not yet supported".format(ast))

        # process the procedure or function body
        if len(input_list) > 0 and input_list[0].data.upper() in ["PROCEDURE_BLOCK", "FUNCTION_BLOCK"]:
            for ast in input_list[0].children:
                if (ast.data.upper() in ["PROCEDURE_DECLARATION", "FUNCTION_DECLARATION]"]) and len(ast.children) > 0:
                    msg = "nested {1} definition is currently not supported. '{0}' will be ignored."
                    _MODULE_LOGGER_.error(msg.format(ast.children[1], context))
                else:

                    self._internal_compile(ast, [])
            input_list.pop(0)

        self._decrease_scope()

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
        keyword = BaseKeyword.from_token(input_list.pop(0))
        working_stack.append(keyword)

        # process boolean expression
        expression_stack = self._internal_compile(input_list.pop(0), [])
        expression = BaseExpression.from_list(expression_stack)

        if expression is None:
            msg = "[{0}] incompatible types in expression: {1}"
            _MODULE_LOGGER_.error(msg.format(action_name, expression))

        elif not expression.type == "RESERVED_TYPE_BOOLEAN":
            msg = "[{0}] expected boolean expression but found: {1}"
            _MODULE_LOGGER_.error(msg.format(action_name, expression.type))

        else:
            working_stack.append(expression)

        # process reserved word THEN
        keyword = BaseKeyword.from_token(input_list.pop(0))
        working_stack.append(keyword)

        # generate the intermediate code
        self._ic.init(action_name)
        self._ic.push(working_stack)
        self._ic.flush()
        _MODULE_LOGGER_.debug("[{0}] {1}".format(action_name, working_stack))

        # process statements after IF and before ELSE
        token = input_list.pop(0)
        self._increase_scope(action_name)
        self._internal_compile(token, [])
        self._decrease_scope()

        # switch the action name to match the ELSE part of the IF
        action_name = action_name + "_ELSE"

        # process reserved word ELSE
        working_stack = []
        keyword = BaseKeyword.from_token(input_list.pop(0))
        working_stack.append(keyword)

        # generate the intermediate code
        self._ic.init(action_name)
        self._ic.push(working_stack)
        self._ic.flush()
        _MODULE_LOGGER_.debug("[{0}] {1}".format(action_name, working_stack))

        # process statements after ELSE
        token = input_list.pop(0)
        self._increase_scope(action_name)
        self._internal_compile(token, [])
        self._decrease_scope()

        return working_stack

    def _open_if_statement(self, action_name, input_list, working_stack):
        """
        _open_if_statement
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
        keyword = BaseKeyword.from_token(input_list.pop(0))
        working_stack.append(keyword)

        # process boolean expression
        expression_stack = self._internal_compile(input_list.pop(0), [])
        expression = BaseExpression.from_list(expression_stack)

        if expression is None:
            msg = "[{0}] incompatible types in expression: {1}"
            _MODULE_LOGGER_.error(msg.format(action_name, expression))

        elif not expression.type == "RESERVED_TYPE_BOOLEAN":
            msg = "[{0}] expected boolean expression but found: {1}"
            _MODULE_LOGGER_.error(msg.format(action_name, expression.type))

        else:
            working_stack.append(expression)

        # process reserved word THEN
        keyword = BaseKeyword.from_token(input_list.pop(0))
        working_stack.append(keyword)

        # generate the intermediate code
        self._ic.init(action_name)
        self._ic.push(working_stack)
        self._ic.flush()
        _MODULE_LOGGER_.debug("[{0}] {1}".format(action_name, working_stack))

        # process statements after IF and before ELSE
        token = input_list.pop(0)
        self._increase_scope(action_name)
        self._internal_compile(token, [])
        self._decrease_scope()

        ## switch the action name to match the ELSE part of the IF
        #action_name = action_name + "_ELSE"

        # process reserved word ELSE
        #working_stack = []
        #keyword = BaseKeyword.from_token(input_list.pop(0))
        #working_stack.append(keyword)

        # generate the intermediate code
        #self._ic.init(action_name)
        #self._ic.push(working_stack)
        #self._ic.flush()
        #_MODULE_LOGGER_.debug("[{0}] {1}".format(action_name, working_stack))

        # process statements after ELSE
        #token = input_list.pop(0)
        #self._increase_scope(action_name)
        #self._internal_compile(token, [])
        #self._decrease_scope()

        return working_stack
