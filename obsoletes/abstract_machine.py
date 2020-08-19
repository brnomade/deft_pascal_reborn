"""
PROJECT.......: Deft Pascal Reborn
COPYRIGHT.....: Copyright (C) 2020- Andre L Ballista
DESCRIPTION...: Pascal compiler for TRS80 color computer based on the original Deft Pascal compiler
HOME PAGE.....: https://github.com/brnomade/deft_pascal_reborn
"""


class RAM:

    def __init__(self, size_in_bytes=16000):
        self._size = size_in_bytes
        self._ram = [0]*size_in_bytes

    @property
    def size(self):
        return self._size

    def read(self, location):
        return self._ram[location]

    def write(self, location, value):
        self._ram[location] = value


class AbstractMachine:
    """
     This abstract machine has 3 registers:
     pc : program counter or instruction pointer - Points to the next instruction to be executed
     sp : stack pointer - points to the current address in the data memory
     base : points to the base address in the data memory

     The machine has 2 memory areas:
     - data_ram : where the data is stored. Top and Base registers relate to this structure
     - code_ram : where the instructions are stored. The pc register relates to this structure

     When initialised, top, base and pc are equal to 0
    """
    def __init__(self, memory_size_in_bytes=16000):
        self._data_ram = RAM(memory_size_in_bytes)
        self._code_ram = RAM(memory_size_in_bytes)
        self._pc = 0
        self._base = 0
        self._sp = 0
        self._code_ram.write(0, 26)

    @property
    def memory_size(self):
        return self._data_ram.size

    # methods to read the registers

    @property
    def sp(self):
        return self._sp

    @property
    def base(self):
        return self._base

    @property
    def pc(self):
        return self._pc

    # methods to set the registers

    @sp.setter
    def sp(self, value):
        if value < 0 or value > self.memory_size:
            raise ValueError
        self._sp = value

    @base.setter
    def base(self, value):
        if value < 0 or value > self.memory_size:
            raise ValueError
        self._base = value

    @pc.setter
    def pc(self, value):
        if value < 0 or value > self.memory_size:
            raise ValueError
        self._pc = value

    # methods to read from the memory

    def read(self, location):
        return self._data_ram.read(location)

    def iread(self, location):
        return self._code_ram.read(location)

    # methods to write to the memory

    def write(self, location, value):
        return self._data_ram.write(location, value)

    def iwrite(self, location, value):
        return self._code_ram.write(location, value)

    def inc_pc(self, offset ):
        self.pc = self.pc + offset

class Assembler:

    def __init__(self):
        self._am = AbstractMachine(16000)

