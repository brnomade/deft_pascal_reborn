"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

import inspect


class TDD:

    @classmethod
    def available_tests(cls):
        return [i for i in inspect.getmembers(cls, predicate=inspect.isfunction) if 'tdd_' in i[0]]

    @staticmethod
    def tdd_1():
        code = """
            PROGRAM {{{0}}};                 
            VAR                                      
            V1 : INTEGER;                            
            BEGIN                                    
            V1 := 1;                                    
            END.                                   
        """
        return code


    @staticmethod
    def tdd_2():
        code = """
            PROGRAM my_test_program( A1, A2, A3);    
            LABEL 100, 200, 300, 400;                
            CONST                                    
            C1 = 0.5;  B = 1;                                
            VAR V1, V3 : INTEGER;                        
            V2 : BOOLEAN;                            
            BEGIN                                    
               REPEAT                                
                 V1 := V1 + 1                      
               UNTIL (V1 + V3) > (10 + 1)         
            END.                                   
        """
        return code

