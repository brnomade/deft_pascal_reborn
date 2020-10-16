"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

from components.deft_pascal_compiler import DeftPascalCompiler

import argparse
import logging
import os
import subprocess
import sys

_MAIN_LOGGER = logging.getLogger(__name__)


class DeftPascalReborn:

    _glb_app_version = "0.1.0"


    def __init__(self):
        self._arguments = self._initialise_arguments_parser()
        self._splash_screen()
        self._present_script_settings()
        if not self._validate_arguments():
            print("\nConfiguration error. Terminating execution.\n")
            sys.exit(1)
        self._compiler = None

    def _initialise_arguments_parser(self):
        parser = argparse.ArgumentParser(description="DEFT PASCAL REBORN. Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler. Copyright (C) 2020- Andre L Ballista. More details at https://github.com/brnomade/deft_pascal_reborn")
        parser.add_argument("input_file", help="file name of the input file. file extension expected. a full file path can be provided with the file name")
        parser.add_argument("compiler_executable", help="file name of the compiler executable. file extension expected. a full file path can be provided with the file name")
        parser.add_argument("-output_path", help="filepath for the output files. if not provided, the path from the input file is used.")
        parser.add_argument("-compiler", choices=['GCC', 'CMOC'], default='GCC', help="compiler to transform the intermediate code into an executable")
        parser.add_argument("-v", "--verbosity", action="count", help="verbosity levels")
        parser.add_argument("-overwrite", choices=['Yes', 'No'], default='Yes', help="overwrite any output file if they already exist")
        parser.add_argument("-steps", choices=['SYNTAX', 'SEMANTIC', 'INTERMEDIATE', 'BUILD'], default='BUILD', help="compilation steps to perform")
        parser.add_argument("-save_steps", choices=['Yes', 'No'], default='Yes', help="save the result AST to a file in the same location as the output_file")
        parser.add_argument("-q", "--quiet", action="count", help="quietness levels")
        parser.add_argument('--version', action='version', version='%(prog)s '+self._glb_app_version)
        return parser.parse_args()

    def _splash_screen(self):
        print("")
        print("Deft Pascal Reborn - PASCAL COMPILER FOR THE TRS80 COLOR COMPUTER")
        print("Created by Andre Ballista (2020)")
        print("Version {0}".format(self._glb_app_version))

    @staticmethod
    def _present_script_section(a_section_name):
        print("")
        print("------------------------")
        print(a_section_name.upper())
        print("------------------------")

    def _present_script_settings(self):
        # present the settings
        self._present_script_section("SETTINGS")
        print("input file:", self._arguments.input_file)
        print("compiler executable:", self._arguments.compiler_executable)
        print("output path:", self._arguments.output_path)
        print("backend compiler:", self._arguments.compiler)
        print("verbosity level:", self._adjust_verbosity())
        print("overwrite flag:", self._arguments.overwrite)
        print("steps to perform:", self._arguments.steps)
        print("save intermediate files:", self._arguments.save_steps)
        print("------------------------")
        print("")


    def _validate_arguments(self):
        msg = "{0} does not exist or cannot be found at {1}"
        if not os.path.isfile(self._arguments.input_file):
            print(msg.format("Input file", self._arguments.input_file))
            return False

        if not os.path.isfile(self._arguments.compiler_executable):
            print(msg.format("Compiler executable", self._arguments.compiler_executable))
            return False

        if self._arguments.output_path:
            if not os.path.isdir(self._arguments.output_path):
                print(msg.format("Output folder", self._arguments.output_path))
                return False
        return True

    def _adjust_verbosity(self):
        default_level = 4
        raw_log_level = default_level + (self._arguments.verbosity or 0) - (self._arguments.quiet or 0)
        if raw_log_level <= 0:
            log_level = logging.CRITICAL
        elif raw_log_level == 1:
            log_level = logging.ERROR
        elif raw_log_level == 2:  # default
            log_level = logging.WARNING
        elif raw_log_level == 3:
            log_level = logging.INFO
        else:
            log_level = logging.DEBUG
        return log_level


    def _save_to_file(self, in_memory_buffer, extension):
        #
        if not self._arguments.output_path:
            output_path = os.path.dirname(self._arguments.input_file)
        else:
            output_path = self._arguments.output_path
        #
        filename = os.path.basename(self._arguments.input_file)
        filename = filename.split(".")[0] + "." + extension
        #
        output_file = os.path.join(output_path, filename)
        #
        if os.path.isfile(output_file) and not self._arguments.overwrite:
            msg = "file {0} already exists. will not overwrite it."
            print(msg.format(output_file))
        else:
            file = open(output_file, "w")
            file.write(in_memory_buffer)
            file.close()
        return output_file


    def _execute_syntax_chek(self, pascal_source):
        log = self._compiler.check_syntax(pascal_source)
        if log["ERROR"]:
            print(log["ERROR"])
        #
        if not log["ERROR"] and self._arguments.save_steps:
            self._save_to_file(self._compiler.ast.pretty(), "ast")
        #
        return log


    def _execute_compilation(self):
        log = self._compiler.compile()
        if log["ERROR"]:
            print(log["ERROR"])
        #
        if not log["ERROR"] and self._arguments.save_steps:
            self._save_to_file(self._compiler.intermediate_code, "ic")
        #
        return log


    def _execute_generate(self):
        output_code = self._compiler.generate()
        #
        if output_code:
            return self._save_to_file(output_code, "c")
        else:
            return None


    def _compile_in_gcc(self, path_to_c_code):

        home_dir = os.getcwd()
        gcc_dir = os.path.dirname(self._arguments.compiler_executable)
        gcc_exe = os.path.basename(self._arguments.compiler_executable)

        print(gcc_dir, gcc_exe)

        output_err = path_to_c_code.split(".")[0] + ".err"
        output_out = path_to_c_code.split(".")[0] + ".out"
        output_exe = path_to_c_code.split(".")[0] + ".exe"

        # c_compiler = "{0} -v -print-search-dirs -print-libgcc-file-name -print-multi-directory -print-multi-lib -print-sysroot-headers-suffix -print-multi-os-directory -print-sysroot -o {1}".format(gcc_exe, output_exe)
        c_compiler = "{0} -o {1}".format(self._arguments.compiler_executable, output_exe)
        c_env = "{0} {1} > {2} 2> {3}".format(c_compiler, path_to_c_code, output_out, output_err)
        _MAIN_LOGGER.info(c_env)

        os.chdir(gcc_dir)
        subprocess.run(c_env, shell=True)
        os.chdir(home_dir)

        result_out = "error"
        if os.path.exists(os.path.join(home_dir, output_out)):
            file = open(output_out)
            result_out = file.read()
            file.close()

        result_err = "error"
        if os.path.exists(os.path.join(home_dir, output_err)):
            file = open(output_err)
            result_err = file.read()
            file.close()

        return result_out + result_err

    def _compile_in_c_compiler(self, path_to_c_code):

        home_dir = os.getcwd()
        compiler_dir = os.path.dirname(self._arguments.compiler_executable)
        compiler_exe = os.path.basename(self._arguments.compiler_executable)

        output_err = path_to_c_code.split(".")[0] + ".err"
        output_out = path_to_c_code.split(".")[0] + ".out"

        if self._arguments.compiler == "CMOC":
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

            c_compiler = "{0} --verbose -o{1} {2}".format(self._arguments.compiler_executable, output_exe, path_to_c_code)
        else:
            """
            gcc is run via MinGW, so paths are as in windows
            """
            # c_compiler = "{0} -v -print-search-dirs -print-libgcc-file-name -print-multi-directory -print-multi-lib -print-sysroot-headers-suffix -print-multi-os-directory -print-sysroot -o {1}".format(gcc_exe, output_exe)
            output_exe = path_to_c_code.split(".")[0] + ".exe"

            c_compiler = "{0} -o {1} {2}".format(self._arguments.compiler_executable, output_exe, path_to_c_code)

        c_env = "{0} > {1} 2> {2}".format(c_compiler, output_out, output_err)
        _MAIN_LOGGER.info(c_env)

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


    def execute(self):
        #
        self._compiler = DeftPascalCompiler(cmoc=self._arguments.compiler == "CMOC")
        #
        pascal_source = open(self._arguments.input_file, "r").read()
        #
        log = self._execute_syntax_chek(pascal_source)
        if log["ERROR"]:
            return None
        #
        if self._arguments.steps in ["SEMANTIC", "INTERMEDIATE", "BUILD"]:
            log = self._execute_compilation()
            #
            if log["ERROR"]:
                return None
            #
            if self._arguments.steps in ["INTERMEDIATE", "BUILD"]:
                path_to_c_code = self._execute_generate()
                if not path_to_c_code:
                    return None
                #
                if self._arguments.steps in ["BUILD"]:
                    #log = self._compile_in_gcc(path_to_c_code)
                    log = self._compile_in_c_compiler(path_to_c_code)
                    if log:
                        print(log)
                        return None
                #
        return True


def main():
    dpr = DeftPascalReborn()
    if dpr.execute():
        print("Compilation successful.")
    else:
        print("Compilation failed.")


def setup_logging():
    msg_format = '%(asctime)s [%(levelname)8s] [%(name)s - %(filename)s:%(lineno)s] %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(fmt=msg_format, datefmt=date_format)
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    _MAIN_LOGGER.addHandler(console_handler)
    _MAIN_LOGGER.setLevel(logging.DEBUG)
    _MAIN_LOGGER.propagate = False


if __name__ == "__main__":
    # execute only if run as a script
    setup_logging()
    main()
