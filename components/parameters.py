"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

import logging
from components.symbols.base_symbols import BaseIdentifier, BaseExpression

_MODULE_LOGGER_ = logging.getLogger("deft_pascal_reborn")


class BaseParameter:

    @property
    def category(self):
        return type(self).__name__


class ActualParameter(BaseParameter):

    def __init__(self, value, field_width=None, decimal_places=None):
        if not isinstance(value, BaseExpression):
            raise ValueError("a parameter must be subclass of BaseExpression")
        if field_width and not isinstance(field_width, BaseExpression):
            raise ValueError("a parameter must be subclass of BaseExpression")
        if decimal_places and not isinstance(decimal_places, BaseExpression):
            raise ValueError("a parameter must be subclass of BaseExpression")

        self._value = value
        self._width = field_width
        self._decimal = decimal_places

    def __str__(self):
        return "{0}({1}:{2}:{3})".format(self.category,
                                         self._value.value,
                                         self._width.value if self._width else None,
                                         self._decimal.value if self._decimal else None)

    def __repr__(self):
        return "{0}({1}:{2}:{3})".format(self.category,
                                         self._value.value,
                                         self._width.value if self._width else None,
                                         self._decimal.value if self._decimal else None)


    @property
    def cardinality(self):
        return 1 + (1 if self._width else 0) + (1 if self._decimal else 0)

    @property
    def value(self):
        return self._value

    @property
    def field_width(self):
        return self._width

    @property
    def decimal_places(self):
        return self._decimal


class FormalParameter(BaseParameter):

    def do_nothing(self):
        pass

