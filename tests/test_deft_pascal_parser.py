from unittest import TestCase
from deft_pascal_parser_3 import DeftPascalParser
from parameterized import parameterized
from common_test_cases import LanguageTests


class TestDeftPascalParser(TestCase):

    @parameterized.expand(LanguageTests.parser_tests_to_run())
    def test(self, name, source_code):
        deft_pascal_parser = DeftPascalParser()
        ast = deft_pascal_parser.parse(source_code)
        print(ast.pretty())
        self.assertIsNotNone(ast)


