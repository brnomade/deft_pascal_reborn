
class AST(object):

    def __init__(self):
        self.__token = None

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
        super().__init__()
        self.__left_operand = left_operand
        self.__token = operator
        self.__right_operand = right_operand

    def __str__(self):
        return "{0}('{1}'|{2})".format(self.left,
                                       self.token,
                                       self.right)

    def __repr__(self):
        return "{0}('{1}'|{2})".format(self.left,
                                       self.token,
                                       self.right)

    @property
    def left(self):
        return self.__left_operand



    @property
    def right(self):
        return self.__right_operand

    @left.setter
    def left(self, new_left):
        self.__left_operand = new_left

    @right.setter
    def right(self, new_right):
        self.__right_operand = new_right


class Number(AST):
    def __init__(self, token):
        super.__init__()
        self.token = token
        self.value = token.value

