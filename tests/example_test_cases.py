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
    def example_program_definition_2():
        code = """
            program example_program_definition_2;                          
            const             
              ZZ = 1 + 2 + 3 + 4;  
              INT_1 = 1;
              BOO_1 = True;
              CHA_1 = 'C';    
              STR_1 = 'ABCDEFG';                
              PI = 3.1415;  
            var                                   
              a : real;
              b : integer;    
              c : BOOLEAN;
              d : CHAR;
              e : ^CHAR;      
              z : integer;

            function multiply_and_print(i, v: integer; r: real): integer; forward;
            function divide_and_print(i: integer; r: real): integer; forward;
            function sum_and_print(i: integer; r: real): integer; forward;
            function subtract_and_print(i: integer; r: real): integer; forward;
              
            function multiply_and_print(i, v: integer; r: real): integer;  
            begin                                 
              v := i * i;
              b := v;
              b := INT_1 + v;
              writeln(i * v, i, v);   
              multiply_and_print := b;                      
            end;                                  

            begin                                 
              a := PI;                            
              b := 20;  
              FOR z := 1 to b do BEGIN
                  z := multiply_and_print(b, b, a);                                
                  writeln(z);
                  if z > 10 then
                    writeln('maior');
              end;
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

    @staticmethod
    def example_two_for_with_hello_world():
        code = """
            program hello_world;
            var
                x, y : integer;
            begin
                x := 1;
                for x := 1 to 10 DO BEGIN
                    writeln('Hello World!', x)
                end;
                for y := 10 downto 1 DO BEGIN
                    writeln('World, Hello!', y)
                end;               
            end.
        """
        return code

    @staticmethod
    def example_divisors():
        code = """
            program divisors;
                VAR NUMBER, DIVISOR : INTEGER;
            BEGIN
                FOR NUMBER := 100 DOWNTO 0 DO
                BEGIN
                    IF NUMBER > 0 THEN
                    BEGIN
                        WRITELN('THE DIVISORS OF', NUMBER, 'ARE:');
                        FOR DIVISOR := 2 TO NUMBER DO
                            IF NUMBER MOD DIVISOR = 0 THEN
                                WRITELN(DIVISOR);
                    END;
                END;
            END.
        """
        return code

    @staticmethod
    def not_ready_primes():
        code = """
            program primes;
                CONST 
                    N = 1229;
                    N1 = 35; (* N1 is SQRT OF N *)
                VAR
                    I, K, X, INC, LIM, SQUARE, L : INTEGER
                    PRIM : BOOLEAN;
                    P, V : ARRAY[1..N] of INTEGER;
                BEGIN
                    WRITE(2:6, 3:6); 
                    L := -2;            
                    X := 1;
                    INC := 4;
                    LIM := 1;
                    SQUARE := 9;
                    FOR I := 3 TO N DO
                    BEGIN (* FIND NEXT PRIME *)
                        REPEAT 
                            X := X + INC;
                            INC := 6 - INC;
                            IF SQUARE <= X THEN
                                BEGIN
                                    LIM := LIM + 1;
                                    V[LIM] := SQUARE;
                                    SQUARE := (P[LIM + 1]) * (P[LIM + 1))
                                END;
                            K := 2;
                            PRIM := TRUE;
                            WHILE PRIM AND (K < LIM) DO
                                BEGIN
                                    K := K + 1;
                                    IF V[K] < X THEN 
                                        V[K] := V[K] + 2 * P[K];
                                    PRIM := X <> V[K]
                                END
                        UNTIL PRIM;
                        IF I <= N1 THEN 
                            P[I] := X;
                        WRITE(X:6);
                        L := L + 1;
                        IF L = 10 THEN
                            BEGIN
                                WRITELN;
                                L := 0;
                            END
                    END;
                    WRITELN;
                END.                
        """
        return code
