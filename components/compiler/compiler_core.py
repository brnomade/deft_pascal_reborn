"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from lark import Token, Tree


class CompilerCore:



def get_top_element(ast):
    """
    Retrieve and return the top most element (index = 0) from the ast
    The input ast is modified
    """
    return ast.pop(0)


def get_bottom_element(ast):
    """
    Retrieve and return the bottom most element (index = -1) from the ast
    The input ast is modified

    Parameters:
    ast: an AST

    Returns:
        Tree or Token depending on the ast content
    """
    return ast.pop(-1)


def get_value_from_asserted_top_token(ast, expected_type, label):
    """
    Retrieve the top most element (index = 0) from the ast and compare to the expected_context
    Raise an exception if it is not a Token instance.
    Raise a ValueError if they differ.
    The input ast is modified.

    Parameters:
    ast: an AST
    string: expected_context
    string: label for the error message

    Returns:
    string: The value of the token
    """
    element = get_top_element(ast)
    assert isinstance(element, Token)
    if element.type != expected_type:
        raise ValueError("Internal Error - Unknown context '{0}' in action '{1}'".format(element.type, label))
    return element.value


def retrieve_directive(ast, label):
    """
    Retrieve the bottom most element (index = -1) from the ast and extract the directive value
    Raises an exception if element is not a Tree instance.
    The input ast is modified.

    Parameters:
    ast: an ast
    string: label for the error message

    Returns:
    string: The directive name
    """
    element = get_bottom_element(ast)
    assert isinstance(element, Tree)
    if element.data.upper() != "DIRECTIVE":
        raise KeyError("Internal Error - Unexpected keyword '{0}' in action '{1}'".format(element.data, label))
    else:
        directive = element.children[0].value.upper()
        if directive not in ["FORWARD", "EXTERNAL"]:
            raise KeyError(
                "Internal Error - Unknown directive '{0}' in action '{1}'".format(element.data, label))
        return directive


def retrieve_identifier(ast):
    """
    Retrieve the value of the top most element (index = 0) from the ast and returns its value
    The input ast is modified.

    Parameters:
    ast: an ast

    Returns:
    string: The identifier
    """
    return get_top_element(ast).value


def retrieve_symbol_reporting_if_already_declared(symbol_table, identifier, context, label, logger):
    """
    Retrieve and verify if the identifier has already been declared in the symbol table
    Logs an error if identifier is already declared

    Parameter:
    SymbolTable: symbol_table
    string: identifier
    string: context
    string: label
    LogHandler: logger

    Returns:
        None if identifier is not present, otherwise the Identifier itself.
    """
    symbol = symbol_table.retrieve(identifier, equal_level_only=False)
    if symbol:
        msg = "[{0}] {2} '{1}' already declared"
        logger.error(msg.format(label, identifier, context))
    return symbol


def get_value_from_asserted_bottom_tree(ast, expected_type, label):
    """
    Retrieve the top most element (index = 0) from the ast and compare to the expected_context
    Raise an exception if it is not a Token instance.
    Raise a ValueError if they differ.
    The input ast is modified.

    Parameters:
    ast: an AST
    string: expected_context
    string: label for the error message

    Returns:
    string: The value of the token
    """
    element = get_top_element(ast)
    assert isinstance(element, Token)
    if element.type != expected_type:
        raise ValueError("Internal Error - Unknown context '{0}' in action '{1}'".format(element.type, label))
    return element.value
