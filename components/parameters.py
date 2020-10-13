"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

import logging
from components.symbols.base_symbols import BaseExpression
from components.symbols.type_symbols import BasicType, StringType

_MODULE_LOGGER_ = logging.getLogger("deft_pascal_reborn")


class BaseParameter:

    @property
    def category(self):
        return type(self).__name__


class ActualParameter(BaseParameter):

    def __init__(self, value, field_width=None, decimal_places=None):
        assert isinstance(value, BaseExpression), "a parameter must be subclass of BaseExpression"
        if field_width:
            assert isinstance(field_width, BaseExpression), "field width must be subclass of BaseExpression"
        if decimal_places:
            assert isinstance(decimal_places, BaseExpression), "decimal places must be subclass of BaseExpression"
        self._value = value
        self._width = field_width
        self._decimal = decimal_places


    def __str__(self):
        return "{0}({1}:{2}:{3}:{4})".format(self.category,
                                             self.type,
                                             self._value.value,
                                             self._width.value if self._width else None,
                                             self._decimal.value if self._decimal else None)

    def __repr__(self):
        return "{0}({1}:{2}:{3}:{4})".format(self.category,
                                             self.type,
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

    @property
    def type(self):
        return self.value.native_type if self.value else None


class FormalParameter(BaseParameter):

    def __init__(self, a_name, a_type):
        assert isinstance(a_type, BasicType) or isinstance(a_type, StringType), "formal parameter type must be subclass of BasicType"
        self._name = a_name
        self._type = a_type

    def __str__(self):
        return "{0}('{1}'|{2})".format(self.category, self.name, self.type)

    def __repr__(self):
        return "{0}('{1}'|{2})".format(self.category, self.name, self.type)

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @type.setter
    def type(self, new_type):
        self._type = new_type


