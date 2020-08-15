"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
VERSION.......: 0.1
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from unittest import TestCase
from components.deft_pascal_compiler import DeftPascalCompiler
from parameterized import parameterized
from tests.common_test_cases import LanguageTests, TestSuit
import inspect
import logging
import os
import subprocess
import sys


GLB_LOGGER = logging.getLogger(__name__)

glb_output_filename = "my_scenario_program.c"
param_remove_file_after_test = True


class TestCodeGenerator(TestCase):

    def setUp(self):
        available_tests = [i[0] for i in inspect.getmembers(LanguageTests, predicate=inspect.isfunction) if
                           'scenario_' in i[0]]
        selected_tests = [i[0] for i in TestSuit().generator_tests_to_run() if 'scenario_' in i[0]]
        if not set(available_tests).issubset(set(selected_tests)):
            msg = "\n\nNot all test scenarios are being run. Review TestSuit class.\n\nDifferences:\n{0}\n\n"
            GLB_LOGGER.warning(msg.format(set(available_tests)-set(selected_tests)))

    @staticmethod
    def compile_in_gcc(input_c):

        home_dir = os.getcwd()
        mig_dir = "C:\\MinGW\\bin"

        sources_path = "output\\sources"
        bin_path = "output\\bin"
        logs_path = "output\\logs"

        input_source = os.path.join(home_dir, sources_path, input_c)
        output_err = os.path.join(home_dir, logs_path, input_c.split(".")[0] + ".err")
        output_out = os.path.join(home_dir, logs_path, input_c.split(".")[0] + ".out")
        output_exe = os.path.join(home_dir, bin_path, input_c.split(".")[0] + ".exe")

        c_compiler = "gcc.exe -o {0}".format(output_exe)
        c_env = "{0} {1} > {2} 2> {3}".format(c_compiler, input_source, output_out, output_err)

        GLB_LOGGER.debug(c_env)
        os.chdir(mig_dir)
        subprocess.run(c_env, shell=True)
        os.chdir(home_dir)

        result_out = "error"
        if os.path.exists(os.path.join(home_dir, output_out)):
            file = open(output_out)
            result_out = file.read()
            file.close()
            if not result_out:
                GLB_LOGGER.warning("no output from gcc")
            if param_remove_file_after_test:
                os.remove(output_out)

        result_err = "error"
        if os.path.exists(os.path.join(home_dir, output_err)):
            file = open(output_err)
            result_err = file.read()
            file.close()
            if not result_err:
                GLB_LOGGER.warning("no errors from gcc")
            if param_remove_file_after_test:
                os.remove(output_err)

        return result_out + result_err

    @staticmethod
    def run_in_shell(input_c):
        home_dir = os.getcwd()
        bin_path = "output\\bin"
        output_exe = os.path.join(home_dir, bin_path, input_c.split(".")[0] + ".exe")
        c_env = "{0}".format(output_exe)
        return subprocess.run(c_env, shell=True)


    @parameterized.expand(LanguageTests.generator_tests_to_run())
    def test_positive(self, name, source_code):
        compiler = DeftPascalCompiler(cmoc=False)
        #
        if "{{{0}}}" in source_code:
            source_code = source_code.replace("{{{0}}}", name)
        #
        error_log = compiler.check_syntax(source_code)
        if error_log:
            GLB_LOGGER.debug(error_log)
        self.assertIsNone(error_log)
        #
        #
        GLB_LOGGER.debug(compiler.ast.pretty())
        #
        error_log = compiler.compile()
        if error_log:
            GLB_LOGGER.debug(error_log)
        self.assertIsNone(error_log)
        #
        ic = compiler.intermediate_code
        GLB_LOGGER.debug(ic)
        #
        output = self.compile_in_gcc("{0}.c".format(name))
        GLB_LOGGER.debug(output)
        self.assertNotIn("error", output)
        self.assertNotIn("warning", output)
        #
        output = self.run_in_shell("{0}.c".format(name))
        self.assertEquals(0, output.returncode)
