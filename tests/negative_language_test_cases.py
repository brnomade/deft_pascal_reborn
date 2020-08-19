"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""
import inspect

class NegativeLanguageTests:

    @classmethod
    def available_tests(cls):
        return [i for i in inspect.getmembers(cls, predicate=inspect.isfunction) if 'scenario_' in i[0]]

    @staticmethod
    def scenario_syntax_error():
        code = """
            PROGRAM {{{0}}}        
            BEGIN                               
            END.                                
        """
        return code
