"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

class AST(object):

    def __init__(self, token):
        self.__token = token

    @property
    def category(self):
        return type(self).__name__

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, new_token):
        self.__token = new_token


class BinaryOperation(AST):

    def __init__(self, left_operand, operator, right_operand):
        super().__init__(operator)
        self.__left_operand = left_operand
        self.__right_operand = right_operand

    def __str__(self):
        return "{0}({1}|{2}|{3})".format(self.category,
                                         self.left_operand,
                                         self.token,
                                         self.right_operand)

    def __repr__(self):
        return "{0}({1}|{2}|{3})".format(self.category,
                                         self.left_operand,
                                         self.token,
                                         self.right_operand)

    @property
    def left_operand(self):
        return self.__left_operand

    @property
    def right_operand(self):
        return self.__right_operand

    @left_operand.setter
    def left_operand(self, new_left):
        self.__left_operand = new_left

    @right_operand.setter
    def right_operand(self, new_right):
        self.__right_operand = new_right


class Number(AST):

    def __str__(self):
        return "{0}({1})".format(self.category, self.token)

    def __repr__(self):
        return "{0}({1})".format(self.category, self.token)

    @property
    def value(self):
        return self.token.value

