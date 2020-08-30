"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from components.symbols.base_symbols import BaseType
from components.symbols.type_symbols import PointerType
from components.symbols.operator_symbols import Operator, UnaryOperator, NeutralOperator, BinaryOperator
# from components.symbols.identifier_symbols import Identifier
# from components.symbols.literals_symbols import Literal

import tokenize
from io import StringIO
from collections import deque

import logging
logger = logging.getLogger(__name__)


class ExpressionOriginal:

    # Set the precedence level of the operators
    precedence = {"^": 4,
                  "/": 3,
                  "*": 3,
                  "+": 2,
                  "-": 2,
                  "(": 1}

    def __init__(self, exp_str):
        self.exp_str = exp_str.strip()
        self.infix_tokens = []
        self.postfix_tokens = []

    def Evaluate(self):
        self.Tokenize()
        self.InfixToPostfix()
        result = []
        for token in self.postfix_tokens:
            try:
                v = int(token)
            except ValueError:
                v = token
            result.append(v)
        print("original algorithm - postfix expression : {0}\n\n".format(result))
        return result


    def Tokenize(self):

        tuplelist = tokenize.generate_tokens(StringIO(self.exp_str).readline)

        for x in tuplelist:
            if x.string:
                self.infix_tokens.append(x.string)

        print("\noriginal algorithm - expression : " + self.exp_str)


    def InfixToPostfix(self):

        stack = deque()
        stack.appendleft("(")
        self.infix_tokens.append(")")

        while self.infix_tokens:

            token = self.infix_tokens.pop(0)

            if token == "(":
                stack.appendleft(token)

            elif token == ")":
                # Pop out all the operators from the stack and append them to
                # postfix expression till an opening bracket "(" is found

                while stack[0] != "(":     # peek at topmost item in the stack
                    self.postfix_tokens.append(stack.popleft())
                stack.popleft()

            elif token == "*" or token == "/" or token == "+" or token == "-" or token == "^":

                # Pop out the operators with higher precedence from the top of the
                # stack and append them to the postfix expression before
                # pushing the current operator onto the stack.
                while stack and self.precedence[stack[0]] >= self.precedence[token]:
                    self.postfix_tokens.append(stack.popleft())
                stack.appendleft(token)

            else:
                # Positions of the operands do not change in the postfix
                # expression so append an operand as it is to the postfix expression
                self.postfix_tokens.append(token)

        return self.postfix_tokens


class Expression:

    def __init__(self, expression):
        self.infix_tokens = expression
        self.postfix_tokens = []
        # self.precedence_rules = {"OPERATOR_ARITHMETIC_NEGATION": 70,
        #                          "OPERATOR_ARITHMETIC_NEUTRAL": 70,
        #                          "OPERATOR_STARSTAR": 60,
        #                          "OPERATOR_DIVIDE": 50,
        #                          "OPERATOR_DIV": 50,
        #                          "OPERATOR_MOD": 50,
        #                          "OPERATOR_MULTIPLY": 50,
        #                          "OPERATOR_ABS": 40,
        #                          "OPERATOR_PLUS": 30,
        #                          "OPERATOR_MINUS": 30,
        #                          "OPERATOR_LSL": 20,
        #                          "OPERATOR_LSR": 20,
        #                          "OPERATOR_XOR": 20,
        #                          "OPERATOR_SHL": 20,
        #                          "OPERATOR_SHR": 20,
        #                          "OPERATOR_NOT": 10,
        #                          "OPERATOR_AND": 10,
        #                          "OPERATOR_OR": 10,
        #                          "OPERATOR_IN": 5,
        #                          "OPERATOR_EQUAL_TO": 5,
        #                          "OPERATOR_NOT_EQUAL_TO": 5,
        #                          "OPERATOR_LESS_THEN": 5,
        #                          "OPERATOR_GREATER_THAN": 5,
        #                          "OPERATOR_LESS_OR_EQUAL_TO": 5,
        #                          "OPERATOR_GREATER_OR_EQUAL_TO": 5,
        #                          "OPERATOR_ASSIGNMENT": 1,
        #                          "LEFT_PARENTHESES": 0
        #                          }

    def infix_to_postfix(self):
        # logger.info("infix_to_postfix\n")
        stack = deque()
        lp = NeutralOperator.operator_left_parentheses()
        rp = NeutralOperator.operator_right_parentheses()

        stack.appendleft(lp)
        self.infix_tokens.append(rp)

        while self.infix_tokens:
            token = self.infix_tokens.pop(0)

            if token.value == lp.value:
                stack.appendleft(token)

            elif token.value == rp.value:

                while not stack[0].value == lp.value:       # peek at topmost item in the stack
                    self.postfix_tokens.append(stack.popleft())
                stack.popleft()

            elif isinstance(token, BinaryOperator) or isinstance(token, UnaryOperator):

                # while stack and self.precedence_rules[stack[0].type] >= self.precedence_rules[token.type]:
                while stack and stack[0].precedence >= token.precedence:
                    self.postfix_tokens.append(stack.popleft())
                stack.appendleft(token)

            else:
                self.postfix_tokens.append(token)
        return self.postfix_tokens


def convert_to_postfix(expression):
    return Expression(expression.copy()).infix_to_postfix()


#def compatibility_for_operator(operator_name):
#    # this is defined from the symbol_left perspective.
#    if operator_name in glb_compatibility_matrix:
#        return glb_compatibility_matrix[operator_name]


def check_type_compatibility(expression):
    """
    expression - is a list of tokens.
    """
    #
    compatible = True
    stack = []
    for index, token in enumerate(convert_to_postfix(expression)):

        if isinstance(token, Operator):
            symbol_right = stack.pop()
            symbol_right = symbol_right if isinstance(symbol_right, BaseType) else symbol_right.type

            if isinstance(token, UnaryOperator):
                result = token.evaluate_to_type(symbol_right)

            elif isinstance(token, BinaryOperator):
                symbol_left = stack.pop()
                symbol_left = symbol_left if isinstance(symbol_left, BaseType) else symbol_left.type
                result = token.evaluate_to_type(symbol_right=symbol_right, symbol_left=symbol_left)

            if result:
                stack.append(result)

            else:
                return None

        else:
            stack.append(token)

    return stack[-1]


def token_is_an_operator(token):
    return "OPERATOR_" in token.type


# def identifier_from_token(parser_token, context_label, context_level):
#     """
#     return an Identifier (i.e. an identifier for anything different than TYPEs) from a parser input_token
#     """
#     return Identifier(parser_token.value, context_label, context_level, parser_token.type, parser_token.value)
