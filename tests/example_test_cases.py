"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""

import inspect


class PascalExamples:

    @classmethod
    def available_tests(cls):
        return [i for i in inspect.getmembers(cls, predicate=inspect.isfunction) if 'example_' in i[0]]

    @staticmethod
    def e_xample_program_definition_2():
        code = """
            program test;                          
            const                                 
              PI = 3.1415;                        

            var                                   
              a, b: real;                         
              c : MEUTIPO;                        
            procedure hello(s: string; n: real);  
            begin                                 
              writeln(s);                         
            end;                                  

            begin                                 
              a := PI;                            
              b := a * 10;                        
              hello("Hello World!", b);           
            end.                                 
        """
        return code


    @staticmethod
    def example_fahrenheit_to_celsius_converter():
        code = """
            program {{{0}}}(output);
            { Program to convert temperatures from
             Fahrenheit to Celsius. }
            const
                MIN = 0;
                MAX = 300;
                LOOP = 3;
            var
                fahren: integer;
                celsius: real;
                counter: integer;
                looper: integer;
            begin
                looper := LOOP;
                while looper < 10 DO begin
                    writeln('while loop');
                    looper := looper + 1;
                end;
                if LOOP > 10 then begin
                    writeln('if loop > 10');
                end
                else begin
                    writeln('loop <= 10');
                    if MAX > MIN then begin
                      writeln('if max is bigger than min');
                    end
                    else begin
                      writeln('not needed');
                    end;
                    writeln('loop is acceptable');
                end;
                counter := 0;
                repeat
                    writeln('Fahrenheit     Celsius');
                    writeln('----------     -------');
                    for fahren := MIN to MAX do begin
                        celsius := 5 * (fahren - 32) / 9;
                        writeln(fahren:5, celsius) ;
                    end ;
                    counter := counter + 1
                until counter > LOOP;               
            end.
        """
        return code


    @staticmethod
    def example_hello_world():
        code = """
            PROGRAM X; 
            BEGIN 
                WRITELN('HELLO WORLD'); 
            END.
        """
        return code
