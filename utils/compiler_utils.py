"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

# from components.symbols.base_symbols import BaseType
from components.symbols.operator_symbols import Operator, UnaryOperator, NeutralOperator, BinaryOperator
import tokenize
from io import StringIO
from collections import deque
import os
import subprocess
import platform

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


#def token_is_an_operator(token):
#    return "OPERATOR_" in token.type


def compile_in_gcc(input_c, remove_file_after_test=True):

    home_dir = os.getcwd()

    mig_dir = "C:\\MinGW\\bin"

    if platform.system() == "Windows":
        sources_path = "output\\sources"
        bin_path = "output\\bin"
        logs_path = "output\\logs"
    else:
        sources_path = ""
        bin_path = ""
        logs_path = ""

    input_source = os.path.join(home_dir, sources_path, input_c)
    output_err = os.path.join(home_dir, logs_path, input_c.split(".")[0] + ".err")
    output_out = os.path.join(home_dir, logs_path, input_c.split(".")[0] + ".out")
    output_exe = os.path.join(home_dir, bin_path, input_c.split(".")[0] + ".exe")
    #
    if platform.system() == "Windows":
        gcc_name = "gcc.exe"
    else:
        gcc_name = "gcc"
    #
    # c_compiler = "{0} -S -c -o {1}".format(gcc_name, output_exe)
    # c_env = "{0} {1} > {2} 2> {3}".format(c_compiler, input_source, output_out, output_err)
    c_compiler = "{0} -S -c".format(gcc_name)
    c_env = "{0} {1} > {2} 2> {3}".format(c_compiler, input_source, output_out, output_err)

    print(c_env)
    #
    if platform.system() == "Windows":
        os.chdir(mig_dir)
        env_variables = os.environ.copy()
        env_variables["PATH"] = mig_dir + ";" + env_variables["PATH"]
        subprocess.run(c_env, shell=True, env=env_variables)
    else:
        subprocess.run(c_env, shell=True)
    #
    if platform.system() == "Windows":
        os.chdir(home_dir)
    #
    result_out = "error"
    if os.path.exists(os.path.join(home_dir, output_out)):
        file = open(output_out)
        result_out = file.read()
        file.close()
        if result_out:
            print(result_out)
        if remove_file_after_test:
            os.remove(output_out)

    result_err = "error"
    if os.path.exists(os.path.join(home_dir, output_err)):
        file = open(output_err)
        result_err = file.read()
        file.close()
        if result_err:
            print(result_err)
        if remove_file_after_test:
            os.remove(output_err)

    if remove_file_after_test:
        os.remove(input_c)

    return result_out + result_err


def run_in_shell(c_file_filename):
    #
    filename = os.path.basename(c_file_filename)
    filepath = os.path.dirname(c_file_filename)
    #
    filename = filename.split(".")[0] + ".exe"
    #
    executable_file = os.path.join(filepath, filename)
    #
    msg = "{0} does not exist or cannot be found at {1}"
    if not os.path.isfile(executable_file):
        print(msg.format("Compiler executable", executable_file))
    return subprocess.run(executable_file)


def _execute_syntax_chek(compiler, pascal_source):
    log = compiler.check_syntax(pascal_source)
    if log["ERROR"]:
        print(log["ERROR"])
    #
    if not log["ERROR"] and self._arguments.save_steps:
        self._save_to_file(self._compiler.ast.pretty(), "ast")
    #
    return log


