"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from components.symbols.literals_symbols import *
from components.symbols.type_symbols import *
import logging


_MODULE_LOGGER = logging.getLogger(__name__)


class Operator(BaseSymbol):

    def __init__(self, *args, **kwargs):
        #
        super().__init__(*args, **kwargs)
        self._compatible = None

    def __str__(self):
        return "{0}({1})".format(self.category, self.type)

    def __repr__(self):
        return "{0}({1})".format(self.category, self.type)


class NeutralOperator(Operator):

    @classmethod
    def operator_left_parentheses(cls):
        operator = cls("LEFT_PARENTHESES", 'LEFT_PARENTHESES', "(")
        return operator

    @classmethod
    def operator_right_parentheses(cls):
        operator = cls("RIGHT_PARENTHESES", 'RIGHT_PARENTHESES', ")")
        return operator


class BinaryOperator(Operator):
    """
    The _compatible list maps to the types in the following order:
                 LEFT SYMBOL
        #        0      1    2     3     4     5     6     7     8
        #        INT   REAL  SET   CHAR  STR   BOOL  POINT TEXT  ARRAY
        0 INT   [0   , 1   , None, None, None, None, None, None, None]
        1 REAL  [1   , 1   , None, None, None, None, None, None, None]
        2 SET   [None, None, 2   , None, None, None, None, None, None]
        3 CHAR  [None, None, None, None, None, None, None, None, None]
        4 STR   [None, None, None, None, None, None, None, None, None]
        5 BOOL  [None, None, None, None, None, None, None, None, None]
        6 POINT [None, None, None, None, None, None, None, None, None]
        7 TEXT  [None, None, None, None, None, None, None, None, None]
        8 ARRAY [None, None, None, None, None, None, None, None, None]

        (row, column, cell)
        [(0,0,0),(1,1,1),(2,2,2),(0,1,1),(1,0,1)]

    """

    def _as_type(self, symbol_right, symbol_left):
        """
        Evaluates an operator using the passed symbols as parameter (operands).
        returns None if the operator is not compatible with the operands
        otherwise returns a tuple representing the resulting type of the operator execution
        raises an warning if the operand is not an instance of BaseType.
        """
        if not isinstance(symbol_right, BaseType):
            _MODULE_LOGGER.warning("symbol '{0}' is not a BaseType.".format(symbol_right))
            return None

        if not isinstance(symbol_left, BaseType):
            _MODULE_LOGGER.warning("symbol '{0}' is not a BaseType.".format(symbol_left))
            return None

        result = [t for t in self._compatible if t[0] == symbol_left.index and t[1] == symbol_right.index]

        if len(result) > 1:
            raise KeyError("unexpected multiple results in method")

        if not result:
            return None

        return result[0]

    def is_compatible(self, symbol_right, symbol_left):
        """
        Check if an operator is compatible with the symbols passed as parameter (operands).
        returns False if the operator is not compatible with the operands
        otherwise returns True
        raises and exception if the operand is not an instance of Literal or BaseType.
        """
        result = self._as_type(symbol_right, symbol_left)
        return True if result else False

    def evaluate_to_type(self, symbol_right, symbol_left):
        """
        Evaluates an operator using the passed symbols as parameter (operands).
        returns None if the operator is not compatible with the operands
        otherwise returns an instance of BasicType representing the evaluation of the operator with the operands
        raises and exception if the operand is not an instance of Literal or BaseType.

        Special case for PointerTypes. For those, expectation is that the symbol.type will return another
        type symbol, representing the situation of a ^INTEGER or similar (a pointer to an integer type)

        Unit tests are adjusted to reflect that.
        """
        result = self._as_type(symbol_right, symbol_left)
        if result == (6,6,6):    # this is the scenario for pointer operations. a compiler directive could be used to control it. if flexibility is given, OO programing could be considered
            assert isinstance(symbol_right.type, BaseType) and isinstance(symbol_left.type, BaseType), "property 'type' for PointerType must be a BaseType. Found '{0}' and '{1}'".format(symbol_left, symbol_right)
            result = self._as_type(symbol_right.type, symbol_left.type)
        if not result:
            return None
        result = result[2]
        if result == 0:
            return BasicType.reserved_type_integer()
        if result == 1:
            return BasicType.reserved_type_real()
        if result == 2:
            return BasicType.reserved_type_set()
        if result == 3:
            return BasicType.reserved_type_char()
        if result == 4:
            return StringType.reserved_type_string()
        if result == 5:
            return BasicType.reserved_type_boolean()
        if result == 6:
            return PointerType.reserved_type_pointer()
        if result == 7:
            return BasicType.reserved_type_text()
        if result == 8:
            return BasicType.reserved_type_array()
        if result == 9:
            return BasicType.reserved_type_null()

    @classmethod
    def operator_multiply(cls):
        """
         #  0      1    2     3     4     5     6     7     8      9
         #  INT   REAL  SET   CHAR  STR   BOOL  POINT TEXT  ARRAY  NIL

        (row, column, cell)
        [(0,0,0),(1,1,1),(2,2,2),(0,1,1),(1,0,1)]

        """
        operator = cls("OPERATOR_MULTIPLY", 'OPERATOR_MULTIPLY', "*")
        operator._compatible = [(0,0,0), (1,1,1), (2,2,2), (0,1,1), (1,0,1)]
        # operator._as_type = lambda l, r, c: [t for t in c if t[0] == l.index and t[1] == r.index]
        return operator

    @classmethod
    def operator_plus(cls):
        """
         #  0      1    2     3     4     5     6     7     8      9
         #  INT   REAL  SET   CHAR  STR   BOOL  POINT TEXT  ARRAY  NIL

        (row, column, cell)
        [(0,0,0),(1,1,1),(2,2,2),(3,3,4),(4,4,4),(0,1,1),(1,0,1)]

        """
        operator = cls("OPERATOR_PLUS", 'OPERATOR_PLUS', "+")
        operator._compatible = [(0,0,0), (1,1,1), (2,2,2), (3,3,4), (4,4,4), (0,1,1), (1,0,1)]
        # operator._as_type = lambda l, r, c: [t for t in c if t[0] == l.index and t[1] == r.index]
        return operator

    @classmethod
    def operator_minus(cls):
        """
         #  0      1    2     3     4     5     6     7     8      9
         #  INT   REAL  SET   CHAR  STR   BOOL  POINT TEXT  ARRAY  NIL

        (row, column, cell)
        [(0,0,0),(1,1,1),(2,2,2),(0,1,1),(1,0,1)]

        """
        operator = cls("OPERATOR_MINUS", 'OPERATOR_MINUS', "-")
        operator._compatible = [(0,0,0),(1,1,1),(2,2,2),(0,1,1),(1,0,1)]
        # operator._as_type = lambda l, r, c: [t for t in c if t[0] == l.index and t[1] == r.index]
        return operator

    @classmethod
    def operator_divide(cls):
        """
         #  0      1    2     3     4     5     6     7     8      9
         #  INT   REAL  SET   CHAR  STR   BOOL  POINT TEXT  ARRAY  NIL

        (row, column, cell)
        [(0,0,1),(1,1,1),(0,1,1),(1,0,1)]

        """
        operator = cls("OPERATOR_DIVIDE", 'OPERATOR_DIVIDE', "/")
        operator._compatible = [(0,0,1),(1,1,1),(0,1,1),(1,0,1)]
        # operator._as_type = lambda l, r, c: [t for t in c if t[0] == l.index and t[1] == r.index]
        return operator

    @classmethod
    def operator_div(cls):
        """
         #  0      1    2     3     4     5     6     7     8      9
         #  INT   REAL  SET   CHAR  STR   BOOL  POINT TEXT  ARRAY  NIL

        (row, column, cell)
        [(0,0,0),(1,1,0),(0,1,0),(1,0,0)]

        """
        operator = cls("OPERATOR_DIV", 'OPERATOR_DIV', "DIV")
        operator._compatible = [(0,0,0),(1,1,0),(0,1,0),(1,0,0)]
        # operator._as_type = lambda l, r, c: [t for t in c if t[0] == l.index and t[1] == r.index]
        return operator

    @classmethod
    def operator_assignment(cls):
        """
         #  0      1    2     3     4     5     6     7     8      9
         #  INT   REAL  SET   CHAR  STR   BOOL  POINT TEXT  ARRAY  NIL

         (row, column, cell)
         [(0,0,0),(1,1,1),(2,2,2),(3,3,3),(4,4,4),(5,5,5),(6,6,6),(7,7,7),(8,8,8)(6,9,6)]

         """
        operator = cls("OPERATOR_ASSIGNMENT", "OPERATOR_ASSIGNMENT", ":=")
        operator._compatible = [(0,0,0),(1,1,1),(2,2,2),(3,3,3),(4,4,4),(5,5,5),(6,6,6),(7,7,7),(8,8,8),(6,9,6)]
        # operator._as_type = lambda l, r, c: [t for t in c if t[0] == l.index and t[1] == r.index]
        return operator

    @classmethod
    def operator_equal_to(cls):
        """
         #  0      1    2     3     4     5     6     7     8      9
         #  INT   REAL  SET   CHAR  STR   BOOL  POINT TEXT  ARRAY  NIL

         (row, column, cell)
         [(0,0,5),(1,1,5),(2,2,5),(3,3,5),(4,4,5),(5,5,5),(6,6,5),(7,7,5),(8,8,5),(6,9,5)]

        """
        operator = cls("OPERATOR_EQUAL_TO", "OPERATOR_EQUAL_TO", "=")
        operator._compatible = [(0,0,5),(1,1,5),(2,2,5),(3,3,5),(4,4,5),(5,5,5),(6,6,5),(7,7,5),(8,8,5),(6,9,5)]
        # operator._as_type = lambda l, r, c: [t for t in c if t[0] == l.index and t[1] == r.index]
        return operator

    @classmethod
    def operator_not_equal_to(cls):
        """
         #  0      1    2     3     4     5     6     7     8      9
         #  INT   REAL  SET   CHAR  STR   BOOL  POINT TEXT  ARRAY  NIL

         (row, column, cell)
         [(0,0,5),(1,1,5),(2,2,5),(3,3,5),(4,4,5),(5,5,5),(6,6,5),(7,7,5),(8,8,5),(6,9,5)]

        """
        operator = cls("OPERATOR_NOT_EQUAL_TO", "OPERATOR_NOT_EQUAL_TO", "<>")
        operator._compatible = [(0,0,5),(1,1,5),(2,2,5),(3,3,5),(4,4,5),(5,5,5),(6,6,5),(7,7,5),(8,8,5),(6,9,5)]
        # operator._as_type = lambda l, r, c: [t for t in c if t[0] == l.index and t[1] == r.index]
        return operator

    @classmethod
    def operator_starstar(cls):
        """
         #  0      1    2     3     4     5     6     7     8      9
         #  INT   REAL  SET   CHAR  STR   BOOL  POINT TEXT  ARRAY  NIL

         (row, column, cell)
         [(0,0,0),(1,0,1)]

        """
        operator = cls("OPERATOR_STARSTAR", "OPERATOR_STARSTAR", "**")
        operator._compatible = [(0,0,0),(1,0,1)]
        # operator._as_type = lambda l, r, c: [t for t in c if t[0] == l.index and t[1] == r.index]
        return operator

    @classmethod
    def operator_in(cls):
        """
         #  0      1    2     3     4     5     6     7     8      9
         #  INT   REAL  SET   CHAR  STR   BOOL  POINT TEXT  ARRAY  NIL

         (row, column, cell)
         [(0,2,5),(3,2,5),(5,2,5)]

        """
        operator = cls("OPERATOR_IN", "OPERATOR_IN", "IN")
        operator._compatible = [(0,2,5),(3,2,5),(5,2,5)]
        # operator._as_type = lambda l, r, c: [t for t in c if t[0] == l.index and t[1] == r.index]
        return operator

    @classmethod
    def operator_and(cls):
        """
         #  0      1    2     3     4     5     6     7     8      9
         #  INT   REAL  SET   CHAR  STR   BOOL  POINT TEXT  ARRAY  NIL

         (row, column, cell)
         [(0,0,0),(5,5,5)]

        """
        operator = cls("OPERATOR_AND", "OPERATOR_AND", "AND")
        operator._compatible = [(0,0,0),(5,5,5)]
        # operator._as_type = lambda l, r, c: [t for t in c if t[0] == l.index and t[1] == r.index]
        return operator

    @classmethod
    def operator_or(cls):
        """
         #  0      1    2     3     4     5     6     7     8      9
         #  INT   REAL  SET   CHAR  STR   BOOL  POINT TEXT  ARRAY  NIL

         (row, column, cell)
         [(0,0,0),(5,5,5)]

        """
        operator = cls("OPERATOR_OR", "OPERATOR_OR", "OR")
        operator._compatible = [(0,0,0),(5,5,5)]
        # operator._as_type = lambda l, r, c: [t for t in c if t[0] == l.index and t[1] == r.index]
        return operator

    @classmethod
    def operator_xor(cls):
        """
         #  0      1    2     3     4     5     6     7     8      9
         #  INT   REAL  SET   CHAR  STR   BOOL  POINT TEXT  ARRAY  NIL

         (row, column, cell)
         [(0,0,0),(5,5,5)]

        """
        operator = cls("OPERATOR_XOR", "OPERATOR_XOR", "XOR")
        operator._compatible = [(0,0,0),(5,5,5)]
        # operator._as_type = lambda l, r, c: [t for t in c if t[0] == l.index and t[1] == r.index]
        return operator

    @classmethod
    def operator_lsr(cls):
        """
         #  0      1    2     3     4     5     6     7     8      9
         #  INT   REAL  SET   CHAR  STR   BOOL  POINT TEXT  ARRAY  NIL

         (row, column, cell)
         [(0,0,0)]

        """
        operator = cls("OPERATOR_LSR", "OPERATOR_LSR", "LSR")
        operator._compatible = [(0,0,0)]
        # operator._as_type = lambda l, r, c: [t for t in c if t[0] == l.index and t[1] == r.index]
        return operator

    @classmethod
    def operator_lsl(cls):
        """
         #  0      1    2     3     4     5     6     7     8      9
         #  INT   REAL  SET   CHAR  STR   BOOL  POINT TEXT  ARRAY  NIL

         (row, column, cell)
         [(0,0,0)]

        """
        operator = cls("OPERATOR_LSL", "OPERATOR_LSL", "LSL")
        operator._compatible = [(0,0,0)]
        # operator._as_type = lambda l, r, c: [t for t in c if t[0] == l.index and t[1] == r.index]
        return operator


    @classmethod
    def operator_greater_than(cls):
        """
         #  0      1    2     3     4     5     6     7     8      9
         #  INT   REAL  SET   CHAR  STR   BOOL  POINT TEXT  ARRAY  NIL

         (row, column, cell)
         [(0,0,5),(1,1,5),(3,3,5),(4,4,5),(5,5,5),(0,1,5),(1,0,5)]

        """
        operator = cls("OPERATOR_GREATER_THAN", "OPERATOR_GREATER_THAN", ">")
        operator._compatible = [(0,0,5),(1,1,5),(3,3,5),(4,4,5),(5,5,5),(0,1,5),(1,0,5)]
        # operator._as_type = lambda l, r, c: [t for t in c if t[0] == l.index and t[1] == r.index]
        return operator

    @classmethod
    def operator_less_than(cls):
        """
         #  0      1    2     3     4     5     6     7     8      9
         #  INT   REAL  SET   CHAR  STR   BOOL  POINT TEXT  ARRAY  NIL

         (row, column, cell)
         [(0,0,5),(1,1,5),(3,3,5),(4,4,5),(5,5,5),(0,1,5),(1,0,5)]

        """
        operator = cls("OPERATOR_LESS_THAN", "OPERATOR_LESS_THAN", "<")
        operator._compatible = [(0,0,5),(1,1,5),(3,3,5),(4,4,5),(5,5,5),(0,1,5),(1,0,5)]
        # operator._as_type = lambda l, r, c: [t for t in c if t[0] == l.index and t[1] == r.index]
        return operator

    @classmethod
    def operator_greater_or_equal_to(cls):
        """
         #  0      1    2     3     4     5     6     7     8      9
         #  INT   REAL  SET   CHAR  STR   BOOL  POINT TEXT  ARRAY  NIL

         (row, column, cell)
         [(0,0,5),(1,1,5),(2,2,5),(3,3,5),(4,4,5),(5,5,5),(0,1,5),(1,0,5)]

        """
        operator = cls("OPERATOR_GREATER_OR_EQUAL_TO", "OPERATOR_GREATER_OR_EQUAL_TO", ">=")
        operator._compatible = [(0,0,5),(1,1,5),(2,2,5),(3,3,5),(4,4,5),(5,5,5),(0,1,5),(1,0,5)]
        # operator._as_type = lambda l, r, c: [t for t in c if t[0] == l.index and t[1] == r.index]
        return operator

    @classmethod
    def operator_less_or_equal_to(cls):
        """
         #  0      1    2     3     4     5     6     7     8      9
         #  INT   REAL  SET   CHAR  STR   BOOL  POINT TEXT  ARRAY  NIL

         (row, column, cell)
         [(0,0,5),(1,1,5),(2,2,5),(3,3,5),(4,4,5),(5,5,5),(0,1,5),(1,0,5)]

        """
        operator = cls("OPERATOR_LESS_OR_EQUAL_TO", "OPERATOR_LESS_OR_EQUAL_TO", "<=")
        operator._compatible = [(0,0,5),(1,1,5),(2,2,5),(3,3,5),(4,4,5),(5,5,5),(0,1,5),(1,0,5)]
        # operator._as_type = lambda l, r, c: [t for t in c if t[0] == l.index and t[1] == r.index]
        return operator


class UnaryOperator(Operator):

    """
    The _compatible list maps to the types in the following order:
      0    1    2    3     4    5     6      7     8
     [INT  REAL SET  CHAR  STR  BOOL  POINT  TEXT  ARRAY]
    """

    def _as_type(self, symbol):
        """
        Evaluates an operator using the passed symbol as parameter (operand).
        returns None if the operator is not compatible with the operand
        otherwise returns an integer representing the resulting type of the operator execution
        raises an warning if the operand is not an instance of BaseType.
        """
        if not isinstance(symbol, BaseType):
            _MODULE_LOGGER.warning("symbol '{0}' is not a BaseType.".format(symbol))
            return None
        return self._compatible[symbol.index]

    def is_compatible(self, symbol):
        """
        Check if an operator is compatible with the symbols passed as parameter (operands).
        returns False if the operator is not compatible with the operands
        otherwise returns True
        raises and exception if the operand is not an instance of Literal or BaseType.
        """
        result = self._as_type(symbol)
        return False if result is None else True

    def evaluate_to_type(self, symbol):
        """
        Evaluates an operator using the passed symbols as parameter (operand).
        returns None if the operator is not compatible with the operand
        returns an instance of BasicType if the operator is compatible with the operand
        raises and exception if the operand is not an instance of Literal or BaseType.
        """
        result = self._as_type(symbol)
        if result == 0:
            return BasicType.reserved_type_integer()
        if result == 1:
            return BasicType.reserved_type_real()
        if result == 2:
            return BasicType.reserved_type_set()
        if result == 3:
            return BasicType.reserved_type_char()
        if result == 4:
            return StringType.reserved_type_string()
        if result == 5:
            return BasicType.reserved_type_boolean()
        if result == 6:
            return PointerType.reserved_type_pointer()
        if result == 7:
            return BasicType.reserved_type_text()
        if result == 8:
            return BasicType.reserved_type_array()
        if result == 9:
            return BasicType.reserved_type_null()
        if result == -1:    # action triggered by the UPARROW operator which is basically a de-pointer operation
            result = symbol.type
        return result

    @classmethod
    def operator_not(cls):
        operator = cls("OPERATOR_NOT", "OPERATOR_NOT", "NOT")
        #                       0     1     2     3     4     5     6     7     8     9
        #                       INT   REAL  SET   CHAR  STR   BOOL  POINT TEXT  ARRAY NIL
        operator._compatible = [None, None, None, None, None, 5  ,  None, None, None, None]
        return operator

    @classmethod
    def operator_abs(cls):
        operator = cls("OPERATOR_ABS", "OPERATOR_ABS", "ABS")
        #                       0     1     2     3     4     5     6     7     8     9
        #                       INT   REAL  SET   CHAR  STR   BOOL  POINT TEXT  ARRAY NIL
        operator._compatible = [0   , 1   , None, None, None, None, None, None, None, None]
        return operator

    @classmethod
    def operator_arithmetic_negation(cls):
        operator = cls("OPERATOR_ARITHMETIC_NEGATION", "OPERATOR_ARITHMETIC_NEGATION", "-")
        #                       0     1     2     3     4     5     6     7     8     9
        #                       INT   REAL  SET   CHAR  STR   BOOL  POINT TEXT  ARRAY NIL
        operator._compatible = [0   , 1,    None, None, None, None, None, None, None, None]
        return operator

    @classmethod
    def operator_arithmetic_neutral(cls):
        operator = cls("OPERATOR_ARITHMETIC_NEUTRAL", "OPERATOR_ARITHMETIC_NEUTRAL", "+")
        #                       0     1     2     3     4     5     6     7     8     9
        #                       INT   REAL  SET   CHAR  STR   BOOL  POINT TEXT  ARRAY NIL
        operator._compatible = [0  ,  1  ,  None, None, None, None, None, None, None, None]
        return operator

    @classmethod
    def operator_uparrow(cls):
        operator = cls("OPERATOR_UPARROW", "OPERATOR_UPARROW", "^")
        #                       0     1     2     3     4     5     6      7     8     9
        #                       INT   REAL  SET   CHAR  STR   BOOL  POINT  TEXT  ARRAY NIL
        operator._compatible = [None, None, None, None, None, None, -1   , None, None, None]
        return operator
