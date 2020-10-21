"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from unittest import TestCase
from components.deft_pascal_compiler import DeftPascalCompiler
from parameterized import parameterized
from tests.declarations_test_suit import TestSuit
import os
import subprocess
import platform


param_remove_file_after_test = True


# def compile_in_gcc(input_c):
#     home_dir = os.getcwd()
#
#     mig_dir = "C:\\MinGW\\bin"
#
#     if platform.system() == "Windows":
#         sources_path = "output\\sources"
#         bin_path = "output\\bin"
#         logs_path = "output\\logs"
#     else:
#         sources_path = ""
#         bin_path = ""
#         logs_path = ""
#
#     input_source = os.path.join(home_dir, sources_path, input_c)
#     output_err = os.path.join(home_dir, logs_path, input_c.split(".")[0] + ".err")
#     output_out = os.path.join(home_dir, logs_path, input_c.split(".")[0] + ".out")
#     output_exe = os.path.join(home_dir, bin_path, input_c.split(".")[0] + ".exe")
#     #
#     if platform.system() == "Windows":
#         gcc_name = "gcc.exe"
#     else:
#         gcc_name = "gcc"
#     #
#     # c_compiler = "{0} -S -c -o {1}".format(gcc_name, output_exe)
#     # c_env = "{0} {1} > {2} 2> {3}".format(c_compiler, input_source, output_out, output_err)
#     c_compiler = "{0} -S -c".format(gcc_name)
#     c_env = "{0} {1} > {2} 2> {3}".format(c_compiler, input_source, output_out, output_err)
#
#     print(c_env)
#     #
#     if platform.system() == "Windows":
#         os.chdir(mig_dir)
#     #
#     subprocess.run(c_env, shell=True)
#     #
#     if platform.system() == "Windows":
#         os.chdir(home_dir)
#     #
#     result_out = "error"
#     if os.path.exists(os.path.join(home_dir, output_out)):
#         file = open(output_out)
#         result_out = file.read()
#         file.close()
#         if result_out:
#             print(result_out)
#         if param_remove_file_after_test:
#             os.remove(output_out)
#
#     result_err = "error"
#     if os.path.exists(os.path.join(home_dir, output_err)):
#         file = open(output_err)
#         result_err = file.read()
#         file.close()
#         if result_err:
#             print(result_err)
#         if param_remove_file_after_test:
#             os.remove(output_err)
#
#     if param_remove_file_after_test:
#         os.remove(input_c)
#
#     return result_out + result_err


def compile_in_c_compiler(compiler_executable, path_to_c_code, compiler="CMOC"):

    if platform.system() == "Windows":
        home_dir = os.getcwd()
        compiler_dir = os.path.dirname(compiler_executable)
        compiler_exe = os.path.basename(compiler_executable)
    else:
        home_dir = os.getcwd()
        compiler_dir = ""
        compiler_exe = compiler_executable.split("\\")[-1]

    output_err = path_to_c_code.split(".")[0] + ".err"
    output_out = path_to_c_code.split(".")[0] + ".out"

    if (compiler == "CMOC") and (platform.system() == "Windows"):
        """
        cmoc is run via cygwin, so path_to_c_code needs to be adjusted
        """
        output_exe = path_to_c_code.split(".")[0] + ".bin"

        if "c:\\" in path_to_c_code:
            path_to_c_code = path_to_c_code.replace("c:\\", "/cygdrive/c/")
        else:
            path_to_c_code = path_to_c_code.replace("C:\\", "/cygdrive/c/")
        path_to_c_code = path_to_c_code.replace("\\", "/")

        if "c:\\" in path_to_c_code:
            path_to_c_code = path_to_c_code.replace("c:\\", "/cygdrive/c/")
        else:
            path_to_c_code = path_to_c_code.replace("C:\\", "/cygdrive/c/")
        path_to_c_code = path_to_c_code.replace("\\", "/")

        c_compiler = "{0} --verbose -o{1} {2}".format(compiler_executable, output_exe, path_to_c_code)
    else:
        """
        gcc is run via MinGW, so paths are as in windows
        """
        # c_compiler = "{0} -v -print-search-dirs -print-libgcc-file-name -print-multi-directory -print-multi-lib -print-sysroot-headers-suffix -print-multi-os-directory -print-sysroot -o {1}".format(gcc_exe, output_exe)
        output_exe = path_to_c_code.split(".")[0] + ".exe"

        c_compiler = "{0} -o {1} {2}".format(compiler_executable, output_exe, path_to_c_code)

    c_env = "{0} > {1} 2> {2}".format(c_compiler, output_out, output_err)
    print(c_env)

    os.chdir(compiler_dir)
    subprocess.run(c_env, shell=True)
    os.chdir(home_dir)

    if os.path.exists(os.path.join(home_dir, output_out)):
        file = open(output_out)
        result_out = file.read()
        file.close()
        print(result_out)

    result_err = "error"
    if os.path.exists(os.path.join(home_dir, output_err)):
        file = open(output_err)
        result_err = file.read()
        file.close()

    return result_err


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


class ConfigurationForTestCodeGenerator:

    @classmethod
    def positive_tests_to_run(cls):
        return TestSuit.positive_tests_to_run()

    @classmethod
    def example_tests_to_run(cls):
        return TestSuit.example_tests_to_run()


class TestGeneratorPositiveScenarios(TestCase):

    def setUp(self):
        available_tests = TestSuit.available_positive_tests()
        selected_tests = ConfigurationForTestCodeGenerator.positive_tests_to_run()
        if not set(available_tests).issubset(set(selected_tests)):
            msg = "\n\nNot all test scenarios are being run. Review TestSuit class.\n\nDifferences:\n{0}\n\n"
            print(msg.format(set(available_tests)-set(selected_tests)))


    @parameterized.expand(ConfigurationForTestCodeGenerator.positive_tests_to_run())
    def test_positive(self, name, function_callable):
        source_code = function_callable()
        if "{{{0}}}" in source_code:
            source_code = source_code.replace("{{{0}}}", name)

        compiler = DeftPascalCompiler(cmoc=False)
        log = compiler.check_syntax(source_code)
        if log["ERROR"]:
            print(log["ERROR"])
        self.assertEqual([], log["ERROR"])

        log = compiler.compile()
        if log["ERROR"]:
            print(log["ERROR"])
        self.assertEqual([], log["ERROR"])

        ic = compiler.intermediate_code
        print(ic)
        #
        output_code = compiler.generate()
        #
        home_dir = os.getcwd()
        filepath = os.path.join(home_dir, "output", "sources")
        if not os.path.isdir(filepath):
            filepath = home_dir
        filename = os.path.join(filepath, "{0}.c".format(name))

        if output_code:
            print(output_code)
            print(filename)
            file = open(filename, "w")
            file.write(output_code)
            file.close()

        output = compile_in_c_compiler("C:\\MinGW\\bin\\gcc.exe", filename, compiler="GCC")

        self.assertNotIn("error", output)
        self.assertNotIn("warning", output)


class TestGeneratorExampleScenarios(TestCase):

    @classmethod
    def setUpClass(cls):
        available_tests = TestSuit.available_example_tests()
        selected_tests = ConfigurationForTestCodeGenerator.example_tests_to_run()
        if not set(available_tests).issubset(set(selected_tests)):
            msg = "\n\nNot all example test scenarios are being run. Review TestSuit class.\n\nDifferences:\n{0}\n\n"
            print(msg.format(set(available_tests)-set(selected_tests)))


    @parameterized.expand(ConfigurationForTestCodeGenerator.example_tests_to_run())
    def test_examples(self, name, function_callable):
        source_code = function_callable()
        if "{{{0}}}" in source_code:
            source_code = source_code.replace("{{{0}}}", name)

        compiler = DeftPascalCompiler()
        log = compiler.check_syntax(source_code)
        if log["ERROR"]:
            print(log["ERROR"])
        self.assertEqual([], log["ERROR"])

        log = compiler.compile()
        if log["ERROR"]:
            print(log["ERROR"])
        self.assertEqual([], log["ERROR"])

        ic = compiler.intermediate_code
        print(ic)
        #
        output_code = compiler.generate()
        #
        home_dir = os.getcwd()
        filepath = os.path.join(home_dir, "output", "sources")
        if not os.path.isdir(filepath):
            filepath = home_dir
        filename = os.path.join(filepath, "{0}.c".format(name))

        if output_code:
            print(output_code)
            print(filename)
            file = open(filename, "w")
            file.write(output_code)
            file.close()

        output = compile_in_c_compiler("C:\\MinGW\\bin\\gcc.exe", filename, compiler="GCC")

        self.assertNotIn("error", output)
        self.assertNotIn("warning", output)
