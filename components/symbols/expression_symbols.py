"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from components.symbols.base_symbols import BaseExpression
import logging

_MODULE_LOGGER_ = logging.getLogger("deft_pascal_reborn")


class ConstantExpression(BaseExpression):

    @classmethod
    def from_list(cls, expression_list):
        """
        :return: None if the expression_list contains incompatible types
        :return: an instance of ConstantExpression if the expression_list contains compatible_types.
        """
        expression = super().from_list(expression_list)
        if not expression:
            # scenario - expression has incompatible symbols.
            return None

        #if expression.cardinality > 1 and (expression.type in ["RESERVED_TYPE_CHAR", "RESERVED_TYPE_STRING"]):
        #    _MODULE_LOGGER_.error("string based constant expressions are not supported: {0}".format(expression))
        #    expression.trim_cardinality_down()

        return expression


class IntegerExpression(BaseExpression):

    @classmethod
    def from_list(cls, expression_list):
        """
        :return: None if the expression_list contains incompatible types
        :return: an instance of IntegerExpression if the expression_list contains compatible_types.
        """
        expression = super().from_list(expression_list)
        if not expression or expression.type not in ["RESERVED_TYPE_INTEGER"]:
            # scenario - expression has incompatible symbols or it is not of the expected class.
            return None

        return expression


class BooleanExpression(BaseExpression):

    @classmethod
    def from_list(cls, expression_list):
        """
        :return: None if the expression_list contains incompatible types
        :return: an instance of BooleanExpression if the expression_list contains compatible_types.
        """
        expression = super().from_list(expression_list)
        if not expression or expression.type not in ["RESERVED_TYPE_BOOLEAN"]:
            # scenario - expression has incompatible symbols or it is not of the expected class.
            return None

        return expression
