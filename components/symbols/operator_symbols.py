"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from components.symbols.base_symbols import BaseSymbol
from components.symbols.constant_symbols import BooleanConstant, Constant, NilConstant


class Operator(BaseSymbol):

    # this is defined from the symbol_left perspective.
    _compatibility_matrix = {"OPERATOR_MULTIPLY": ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_REAL", "RESERVED_TYPE_SET"],
                             "OPERATOR_PLUS": ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_REAL", "RESERVED_TYPE_SET", "RESERVED_TYPE_CHAR", "RESERVED_TYPE_STRING"],
                             "OPERATOR_MINUS": ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_REAL", "RESERVED_TYPE_SET", "RESERVED_TYPE_CHAR", "RESERVED_TYPE_STRING"],
                             "OPERATOR_DIVIDE": ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_REAL"],
                             "OPERATOR_DIV": ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_REAL"],
                             "OPERATOR_ASSIGNMENT": ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_REAL", "RESERVED_TYPE_SET", "RESERVED_TYPE_BOOLEAN", "RESERVED_TYPE_CHAR", "RESERVED_TYPE_STRING", "RESERVED_TYPE_POINTER"],
                             "OPERATOR_EQUAL_TO": ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_REAL",  "RESERVED_TYPE_SET", "RESERVED_TYPE_BOOLEAN", "RESERVED_TYPE_CHAR", "RESERVED_TYPE_STRING", "RESERVED_TYPE_POINTER"],
                             "OPERATOR_NOT_EQUAL_TO": ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_REAL",  "RESERVED_TYPE_SET", "RESERVED_TYPE_BOOLEAN", "RESERVED_TYPE_CHAR", "RESERVED_TYPE_STRING", "RESERVED_TYPE_POINTER"],
                             "OPERATOR_STARSTAR": ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_REAL"],
                             "OPERATOR_IN": ["RESERVED_TYPE_CHAR", "RESERVED_TYPE_INTEGER"],
                             "OPERATOR_AND": ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_BOOLEAN"],
                             "OPERATOR_OR": ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_BOOLEAN"],
                             "OPERATOR_GREATER_THEN": ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_REAL", "RESERVED_TYPE_BOOLEAN", "RESERVED_TYPE_CHAR", "RESERVED_TYPE_STRING"],
                             "OPERATOR_GREATER_OR_EQUAL_TO": ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_REAL", "RESERVED_TYPE_BOOLEAN", "RESERVED_TYPE_CHAR", "RESERVED_TYPE_STRING"],
                             "OPERATOR_LESS_THEN": ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_REAL", "RESERVED_TYPE_BOOLEAN", "RESERVED_TYPE_CHAR", "RESERVED_TYPE_STRING"],
                             "OPERATOR_LESS_OR_EQUAL_TO": ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_REAL", "RESERVED_TYPE_BOOLEAN", "RESERVED_TYPE_CHAR", "RESERVED_TYPE_STRING"],
                             }

    def is_unary(self):
        return self.type in ["OPERATOR_NOT", "OPERATOR_ABS", "OPERATOR_ARITHMETIC_NEGATION",
                             "OPERATOR_ARITHMETIC_NEUTRAL"]

    def _evaluate_type_unary(self, symbol):
        if self.is_unary():
            if self.type == "OPERATOR_NOT" and symbol.type == "RESERVED_TYPE_BOOLEAN":
                return BooleanConstant.true()
            elif self.type in ["OPERATOR_ARITHMETIC_NEGATION", "OPERATOR_ARITHMETIC_NEUTRAL"] and symbol.type in ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_REAL"]:
                return Constant(None, None, None, symbol.type, None)
            else:
                raise NotImplementedError("Not yet implemented '{0}' '{1}'".format(self, symbol))
        else:
            raise TypeError("Symbol '{0}' is not an unary operator.".format(self))

    @staticmethod
    def _test_compatibility_operator_greater_or_equal_to(symbol_right, symbol_left):
        """
        checks involved:
        2 - if the types of the operands (symbol_right and symbol_left) match
        """
        if symbol_right.type == symbol_left.type:
            return BooleanConstant.true()
        return None

    @staticmethod
    def _test_compatibility_operator_greater_then(symbol_right, symbol_left):
        """
        checks involved:
        2 - if the types of the operands (symbol_right and symbol_left) match
        """
        if symbol_right.type == symbol_left.type:
            return BooleanConstant.true()
        return None

    @staticmethod
    def _test_compatibility_operator_less_then(symbol_right, symbol_left):
        """
        checks involved:
        2 - if the types of the operands (symbol_right and symbol_left) match
        """
        if symbol_right.type == symbol_left.type:
            return BooleanConstant.true()
        return None

    @staticmethod
    def _test_compatibility_operator_or(symbol_right, symbol_left):
        """
        checks involved:
        2 - if the types of the operands (symbol_right and symbol_left) match
        """
        if symbol_left.type == symbol_right.type:
            if symbol_right.type == "RESERVED_TYPE_BOOLEAN":
                return BooleanConstant.true()
            elif symbol_right.type == "RESERVED_TYPE_INTEGER":
                return Constant(None, None, None, symbol_right.type, None)
        return None

    @staticmethod
    def _test_compatibility_operator_and(symbol_right, symbol_left):
        """
        checks involved:
        2 - if the types of the operands (symbol_right and symbol_left) match
        """
        if symbol_left.type == symbol_right.type:
            if symbol_right.type == "RESERVED_TYPE_BOOLEAN":
                return BooleanConstant.true()
            elif symbol_right.type == "RESERVED_TYPE_INTEGER":
                return Constant(None, None, None, symbol_right.type, None)
        return None

    @staticmethod
    def _test_compatibility_operator_in(symbol_right, symbol_left):
        """
        checks involved:
        2 - if the types of the operands (symbol_right and symbol_left) match
        """
        if symbol_left.type == "RESERVED_TYPE_SET":
            return BooleanConstant.true()
        return None

    @staticmethod
    def _test_compatibility_operator_starstar(symbol_right, symbol_left):
        """
        checks involved:
        2 - if the types of the operands (symbol_right and symbol_left) match
        """
        if symbol_right.type == "RESERVED_TYPE_INTEGER":
            return Constant(None, None, None, symbol_left.type, None)
        return None

    @staticmethod
    def _test_compatibility_operator_not_equal_to(symbol_right, symbol_left):
        """
        checks involved:
        2 - if the types of the operands (symbol_right and symbol_left) match
        """
        if symbol_left.type == symbol_right.type:
            return BooleanConstant.true()
        return None

    @staticmethod
    def _test_compatibility_operator_equal_to(symbol_right, symbol_left):
        """
        checks involved:
        2 - if the types of the operands (symbol_right and symbol_left) match
        """
        if symbol_left.type == symbol_right.type:
            return BooleanConstant.true()
        return None

    @staticmethod
    def _test_compatibility_operator_assignment(symbol_right, symbol_left):
        """
        checks involved:
        2 - if the types of the operands (symbol_right and symbol_left) match
        """
        if symbol_left.type == "RESERVED_TYPE_POINTER" or "^" in symbol_left.type or symbol_left.is_pointer:
            if symbol_right.type == "RESERVED_TYPE_POINTER" or "^" in symbol_left.type or symbol_right.is_pointer:
                return NilConstant.nil(None, None)
        elif symbol_left.type == symbol_right.type:
            return Constant(None, None, None, symbol_left.type, None)
        return None

    @staticmethod
    def _test_compatibility_operator_div(symbol_right, symbol_left):
        """
        integer division - accepts integer and real operands mixed together - result is always an integer
        checks involved:
        2 - if the types of the operands (symbol_right and symbol_left) match
        """
        if symbol_right.type in ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_REAL"]:
            return Constant(None, None, None, "RESERVED_TYPE_INTEGER", None)
        return None

    @staticmethod
    def _test_compatibility_operator_divide(symbol_right, symbol_left):
        """
        real division - accepts integer and real operands mixed together - result is always a real
        checks involved:
        2 - if the types of the operands (symbol_right and symbol_left) match
        """
        if symbol_right.type in ["RESERVED_TYPE_INTEGER", "RESERVED_TYPE_REAL"]:
            return Constant(None, None, None, "RESERVED_TYPE_REAL", None)
        return None

    @staticmethod
    def _test_compatibility_operator_minus(symbol_right, symbol_left):
        """
        checks involved:
        2 - if the types of the operands (symbol_right and symbol_left) match
        """
        # TODO -> Operator MINUS for SETS
        if symbol_left.type == symbol_right.type:
            return Constant(None, None, None, symbol_left.type, None)
        return None

    @staticmethod
    def _test_compatibility_operator_plus(symbol_right, symbol_left):
        """
        checks involved:
        2 - if the types of the operands (symbol_right and symbol_left) match
        """
        # TODO -> Operator PLUS for SETS
        if symbol_left.type == symbol_right.type:
            return Constant(None, None, None, symbol_left.type, None)
        return None

    @staticmethod
    def _test_compatibility_operator_multiply(symbol_right, symbol_left):
        """
        checks involved:
        2 - if the types of the operands (symbol_right and symbol_left) match
        """
        if symbol_left.type == symbol_right.type:
            return Constant(None, None, None, symbol_left.type, None)
        if symbol_left.type == "RESERVED_TYPE_REAL" and symbol_right.type == "RESERVED_TYPE_INTEGER":
            return Constant(None, None, None, symbol_left.type, None)
        if symbol_left.type == "RESERVED_TYPE_INTEGER" and symbol_right.type == "RESERVED_TYPE_REAL":
            return Constant(None, None, None, symbol_right.type, None)
        return None

    def evaluate_to_type(self, symbol_right, symbol_left=None):
        """
        the evaluation results in True or False values
        returns a subclass of BaseSymbol because the type_checking routine operates
        over a list of symbols
        checks involved:
        1 - [TESTED IN THIS METHOD] what types can be used with the operator
        2 - [TESTED IN THE OPERAND METHOD] if the types of the operands (symbol_right and symbol_left) match
        """
        if not symbol_left:
            return self._evaluate_type_unary(symbol_right)
        else:
            if symbol_left.type in Operator._compatibility_matrix[self.type]:
                if self.type == "OPERATOR_IN":
                    return self._test_compatibility_operator_in(symbol_right, symbol_left)
                if self.type == "OPERATOR_AND":
                    return self._test_compatibility_operator_and(symbol_right, symbol_left)
                if self.type == "OPERATOR_OR":
                    return self._test_compatibility_operator_or(symbol_right, symbol_left)
                if self.type == "OPERATOR_GREATER_THEN":
                    return self._test_compatibility_operator_greater_then(symbol_right, symbol_left)
                if self.type == "OPERATOR_LESS_THEN":
                    return self._test_compatibility_operator_less_then(symbol_right, symbol_left)
                if self.type == "OPERATOR_GREATER_OR_EQUAL_TO":
                    return self._test_compatibility_operator_greater_then(symbol_right, symbol_left)
                if self.type == "OPERATOR_LESS_OR_EQUAL_TO":
                    return self._test_compatibility_operator_less_then(symbol_right, symbol_left)
                elif self.type == "OPERATOR_STARSTAR":
                    return self._test_compatibility_operator_starstar(symbol_right, symbol_left)
                elif self.type == "OPERATOR_EQUAL_TO":
                    return self._test_compatibility_operator_equal_to(symbol_right, symbol_left)
                elif self.type == "OPERATOR_NOT_EQUAL_TO":
                    return self._test_compatibility_operator_equal_to(symbol_right, symbol_left)
                elif self.type == "OPERATOR_ASSIGNMENT":
                    return self._test_compatibility_operator_assignment(symbol_right, symbol_left)
                elif self.type == "OPERATOR_MULTIPLY":
                    return self._test_compatibility_operator_multiply(symbol_right, symbol_left)
                elif self.type == "OPERATOR_PLUS":
                    return self._test_compatibility_operator_plus(symbol_right, symbol_left)
                elif self.type == "OPERATOR_MINUS":
                    return self._test_compatibility_operator_plus(symbol_right, symbol_left)
                elif self.type == "OPERATOR_DIVIDE":
                    return self._test_compatibility_operator_divide(symbol_right, symbol_left)
                elif self.type == "OPERATOR_DIV":
                    return self._test_compatibility_operator_div(symbol_right, symbol_left)
                else:
                    raise NotImplementedError(self)
            else:
                raise NotImplementedError(symbol_left)