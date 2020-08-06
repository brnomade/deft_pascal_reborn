from unittest import TestCase
from deft_pascal_compiler import DeftPascalCompiler
from parameterized import parameterized
from common_test_cases import LanguageTests, TestSuit
import inspect
import logging
import os
import subprocess
import sys


logger = logging.getLogger(__name__)
glb_output_filename = "my_scenario_program.c"
param_remove_file_after_test = True


def safe_path(in_str):
    # function to handle windows path names with empty spaces
    # in linux or ios this function is neutral
    if sys.platform.startswith('win'):
        out_str = '"' + in_str + '"'
    else:
        out_str = in_str
    return out_str


class TestCodeGenerator(TestCase):

    def setUp(self):
        available_tests = [i[0] for i in inspect.getmembers(LanguageTests, predicate=inspect.isfunction) if
                           'scenario_' in i[0]]
        selected_tests = [i[0] for i in TestSuit().generator_tests_to_run() if 'scenario_' in i[0]]
        if not set(available_tests).issubset(set(selected_tests)):
            msg = "\n\nNot all test scenarios are being run. Review TestSuit class.\n\nDifferences:\n{0}\n\n"
            logger.warning(msg.format(set(available_tests)-set(selected_tests)))

    @staticmethod
    def compile_in_gcc(input_c):

        mig_dir = "C:\\MinGW\\bin"
        home_dir = os.getcwd()

        dir_path = "output"

        input_c = os.path.join(home_dir, dir_path, input_c)
        output_err = os.path.join(home_dir, dir_path, input_c.split(".")[0] + ".err")
        output_out = os.path.join(home_dir, dir_path, input_c.split(".")[0] + ".out")

        c_compiler = "gcc.exe -c "
        c_env = "{0} {1} > {2} 2> {3}".format(c_compiler, input_c, output_out, output_err)

        logger.info(c_env)
        os.chdir(mig_dir)
        subprocess.run(c_env, shell=True)
        os.chdir(home_dir)

        result_out = "error"
        if os.path.exists(os.path.join(home_dir, output_out)):
            file = open(output_out)
            result_out = file.read()
            file.close()
            if result_out:
                logger.info(result_out)
            else:
                logger.info("no output from gcc")
            if param_remove_file_after_test:
                os.remove(output_out)

        result_err = "error"
        if os.path.exists(os.path.join(home_dir, output_err)):
            file = open(output_err)
            result_err = file.read()
            file.close()
            if result_err:
                logger.info(result_err)
            else:
                logger.info("no errors from gcc")
            if param_remove_file_after_test:
                os.remove(output_err)

        return result_out + result_err

    @parameterized.expand(LanguageTests.generator_tests_to_run())
    def test(self, name, source_code):
        compiler = DeftPascalCompiler()
        #
        if "{{{0}}}" in source_code:
            source_code = source_code.replace("{{{0}}}", name)
        ast = compiler.check_syntax(source_code)
        self.assertIsNotNone(ast)
        #
        error_log = compiler.compile(ast, True, True)
        self.assertEqual(error_log, [])
        #
        output = self.compile_in_gcc("{0}.c".format(name))
        print(output)
        self.assertNotIn("error", output)
        self.assertNotIn("warning", output)
