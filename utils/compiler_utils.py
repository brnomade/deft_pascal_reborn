from components.symbols import Operator, Constant, Identifier, BaseSymbol

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
        self.precedence_rules = {"OPERATOR_ARITHMETIC_NEGATION": 70,
                                 "OPERATOR_ARITHMETIC_NEUTRAL": 70,
                                 "OPERATOR_STARSTAR": 60,
                                 "OPERATOR_DIVIDE": 50,
                                 "OPERATOR_DIV": 50,
                                 "OPERATOR_MOD": 50,
                                 "OPERATOR_MULTIPLY": 50,
                                 "OPERATOR_ABS": 40,
                                 "OPERATOR_PLUS": 30,
                                 "OPERATOR_MINUS": 30,
                                 "OPERATOR_LSL": 20,
                                 "OPERATOR_LSR": 20,
                                 "OPERATOR_XOR": 20,
                                 "OPERATOR_SHL": 20,
                                 "OPERATOR_SHR": 20,
                                 "OPERATOR_NOT": 10,
                                 "OPERATOR_AND": 10,
                                 "OPERATOR_OR": 10,
                                 "OPERATOR_IN": 5,
                                 "OPERATOR_EQUAL_TO": 5,
                                 "OPERATOR_NOT_EQUAL_TO": 5,
                                 "OPERATOR_LESS_THEN": 5,
                                 "OPERATOR_GREATER_THEN": 5,
                                 "OPERATOR_LESS_OR_EQUAL_TO": 5,
                                 "OPERATOR_GREATER_OR_EQUAL_TO": 5,
                                 "OPERATOR_ASSIGNMENT": 1,
                                 "LEFT_PARENTHESES": 0
                                 }

    def infix_to_postfix(self):
        # logger.info("infix_to_postfix\n")
        stack = deque()
        stack.appendleft(BaseSymbol("(", None, None, "LEFT_PARENTHESES", "("))
        self.infix_tokens.append(BaseSymbol(")", None, None, "RIGHT_PARENTHESES", ")"))

        # print("{0} ##\t {1} ##\t {2} ##\t {3}".format(" ",
        #                                              [i.value for i in self.infix_tokens],
        #                                              [i.value for i in self.postfix_tokens],
        #                                              [i.value for i in stack]
        #                                              ))

        # logger.info("{0} ##\t {1} ##\t {2} ##\t {3}".format(" ",
        #                                              [i.type for i in self.infix_tokens],
        #                                              [i.type for i in self.postfix_tokens],
        #                                              [i.type for i in stack]
        #                                              ))

        while self.infix_tokens:
            token = self.infix_tokens.pop(0)

            if token.type == "LEFT_PARENTHESES":
                stack.appendleft(token)

            elif token.type == "RIGHT_PARENTHESES":

                while not stack[0].type == "LEFT_PARENTHESES":       # peek at topmost item in the stack
                    self.postfix_tokens.append(stack.popleft())
                stack.popleft()

            elif token.is_operator:

                # while stack and self.precedence_rules[stack[0].type] >= self.precedence_rules[token.type]:
                while stack and stack[0].precedence >= token.precedence:
                    self.postfix_tokens.append(stack.popleft())
                stack.appendleft(token)

            else:
                self.postfix_tokens.append(token)

            # print("{0} ##\t {1} ##\t {2} ##\t {3}".format(token.value,
            #                                              [i.value for i in self.infix_tokens],
            #                                              [i.value for i in self.postfix_tokens],
            #                                              [i.value for i in stack]
            #                                              ))
            # logger.info("{0} ##\t {1} ##\t {2} ##\t {3}".format(token.type,
            #                                              [i.type for i in self.infix_tokens],
            #                                              [i.type for i in self.postfix_tokens],
            #                                              [i.type for i in stack]
            #                                              ))

        return self.postfix_tokens


def convert_to_tokens(expression):
    token_list = []
    for i in (expression.strip().split(" ")):
        if i == '+':
            t = Operator("+", None, None, "OPERATOR_PLUS", "+")
        elif i == '-':
            t = Operator("–", None, None, "OPERATOR_MINUS", "-")
        elif i == '*':
            t = Operator("*", None, None, "OPERATOR_MULTIPLY", "*")
        elif i == '/':
            t = Operator("/", None, None, "OPERATOR_DIVIDE", "/")
        elif i == '^' or i == "**":
            t = Operator("^", None, None, "OPERATOR_STARSTAR", "^")
        elif i == '(':
            t = Operator("(", None, None, "LEFT_PARENTHESES", "(")
        elif i == ')':
            t = Operator(")", None, None, "RIGHT_PARENTHESES", ")")
        else:
            t = Constant(i, None, None, "RESERVED_TYPE_INTEGER", int(i))
        token_list.append(t)
    return token_list


# def evaluate_postfix(expression):
#     stack = []
#     for i in expression:
#         print("{0}".format([i.value for i in stack]))
#         if i.is_operator():
#             b = stack.pop()
#             a = stack.pop()
#             if i.value == "+":
#                 v = a.value + b.value
#             elif i.value == "-":
#                 v = a.value - b.value
#             elif i.value == '*':
#                 v = a.value * b.value
#             elif i.value == "/":
#                 v = a.value / b.value
#             elif i.value == "^" or i.value == "**":
#                 v = a.value ** b.value
#             else:
#                 print("error", i)
#                 v = 0
#             c = Constant(str(v), None, None, "RESERVED_TYPE_INTEGER", v)
#             stack.append(c)
#         else:
#             stack.append(i)
#     return stack.pop()


def convert_to_postfix(expression):
    return Expression(expression.copy()).infix_to_postfix()


def check_type_compatibility(expression):
    """
    expression - is a list of tokens.
    """
    #
    compatible = True
    stack = []
    for index, token in enumerate(convert_to_postfix(expression)):

        if token.is_operator:

            symbol_right = stack.pop()
            symbol_left = None if token.is_unary() else stack.pop()
            result = token.evaluate_to_type(symbol_right=symbol_right, symbol_left=symbol_left)
            if result:
                stack.append(result)
            else:
                # logger.info("{0}".format([x for x in stack]))
                # compatible = False
                # break
                return None
        else:
            stack.append(token)

        # logger.info("{0}".format([x for x in stack]))
    #return compatible
    return stack[-1]

# def type_from_token(parser_token, context_label, context_level):
#   """
#    return a BaseSymbol from a parser input_token
#    """
#    return BaseSymbol(parser_token.value, context_label, context_level, parser_token.type, parser_token.value)


# def operator_from_token(parser_token, context_label, context_level):
#    """
#    return an Operator from a parser input_token
#    """
#    return Operator(parser_token.value, context_label, context_level, parser_token.type, parser_token.value)


# def type_identifier_from_token(parser_token, context_label, context_level):
#    """
#    return an TypeIdentifier (i.e. an identifier for TYPEs) from a parser input_token
#    """
#    return TypeIdentifier(parser_token.value, context_label, context_level, parser_token.type, parser_token.value)


# def pointer_type_identifier_from_token(parser_token, context_label, context_level):
#    """
#    return an TypeIdentifier (i.e. an identifier for TYPEs) from a parser input_token
#    """
#    return PointerTypeIdentifier(parser_token.value, context_label, context_level, parser_token.type, parser_token.value)


def identifier_from_token(parser_token, context_label, context_level):
    """
    return an Identifier (i.e. an identifier for anything different than TYPEs) from a parser input_token
    """
    return Identifier(parser_token.value, context_label, context_level, parser_token.type, parser_token.value)
