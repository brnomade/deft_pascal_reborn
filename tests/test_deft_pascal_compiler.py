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
param_remove_file_after_test = False


def safe_path( in_str ):
    # function to handle windows path names with empty spaces
    # in linux or ios this function is neutral
    if sys.platform.startswith('win'):
        out_str = '"' + in_str + '"'
    else:
        out_str = in_str
    return out_str


class TestDeftPascalCompiler(TestCase):

    def setUp(self):
        available_tests = [i[0] for i in inspect.getmembers(LanguageTests, predicate=inspect.isfunction) if
                           'scenario_' in i[0]]
        selected_tests = [i[0] for i in TestSuit().compiler_tests_to_run() if 'scenario_' in i[0]]
        if not set(available_tests).issubset(set(selected_tests)):
            msg = "\n\nWARNING!\nNot all test scenarios are being run. Review TestSuit class.\n\nDifferences:\n{0}\n\n\n"
            logger.warning(msg.format(set(available_tests)-set(selected_tests)))
            # print("\n\nWARNING!\nNot all test scenarios are being run. Review TestSuit class\n\n")

    def tearDown(self):
        if os.path.exists(glb_output_filename):
            if param_remove_file_after_test:
                os.remove(glb_output_filename)
        else:
            print("can't find file", glb_output_filename, ". will not delete it.")

    @staticmethod
    def compile_in_clang():
        clang_path = os.path.join("C:\\", "Program Files", "LLVM", "bin", "clang.exe")
        oscmd = safe_path(clang_path)
        oscmd = oscmd + " -fsyntax-only --analyzer-output text -E -x c"
        oscmd = oscmd + " " + glb_output_filename
        oscmd = oscmd + " " + "> out.txt 2> out2.txt"
        print(oscmd)
        subprocess.run(oscmd, shell=True)

        file = open("out.txt")
        result = file.read()
        file.close()

        file = open("out2.txt")
        result = result + file.read()
        file.close()
        return result

    @parameterized.expand(LanguageTests.compiler_tests_to_run())
    def test(self, name, source_code):
        compiler = DeftPascalCompiler()
        #
        ast = compiler.check_syntax(source_code)
        self.assertIsNotNone(ast)
        #
        error_log = compiler.compile(ast)
        self.assertEqual(error_log, [])
        #
        output = self.compile_in_clang()
        print(output)
        self.assertNotIn("error", output)




