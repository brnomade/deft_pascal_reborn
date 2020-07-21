from unittest import TestCase
from deft_pascal_compiler import DeftPascalCompiler
from parameterized import parameterized
from common_test_cases import LanguageTests


class TestDeftPascalCompiler(TestCase):

    @parameterized.expand(LanguageTests.compiler_tests_to_run())
    def test(self, name, source_code):
        compiler = DeftPascalCompiler()
        #
        ast = compiler.check_syntax(source_code)
        self.assertIsNotNone(ast)
        #
        error_log = compiler.compile(ast)
        self.assertEqual(error_log, [])



