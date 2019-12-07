import dataclasses
from functools import lru_cache
from inspect import signature
from typing import List


class Pause(Exception):
    pass


@dataclasses.dataclass()
class Computer:
    """
    >>> Computer([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]).run().mem
    [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
    >>> Computer([1, 0, 0, 0, 99]).run().mem
    [2, 0, 0, 0, 99]
    >>> Computer([2, 3, 0, 3, 99]).run().mem
    [2, 3, 0, 6, 99]
    >>> Computer([2, 4, 4, 5, 99, 0]).run().mem
    [2, 4, 4, 5, 99, 9801]
    >>> Computer([1, 1, 1, 4, 99, 5, 6, 0, 99]).run().mem
    [30, 1, 1, 4, 2, 5, 6, 0, 99]
    >>> Computer([3,0,4,0,99]).run().output
    1
    >>> Computer([3,9,8,9,10,9,4,9,99,-1,8]).run(inp=8).output
    1
    >>> Computer([3,9,8,9,10,9,4,9,99,-1,8]).run(inp=5).output
    0
    >>> Computer([3,9,7,9,10,9,4,9,99,-1,8]).run(inp=7).output
    1
    >>> Computer([3,9,7,9,10,9,4,9,99,-1,8]).run(inp=8).output
    0
    >>> Computer([3,3,1108,-1,8,3,4,3,99]).run(inp=8).output
    1
    >>> Computer([3,3,1108,-1,8,3,4,3,99]).run(inp=1).output
    0
    >>> Computer([3,3,1107,-1,8,3,4,3,99]).run(inp=7).output
    1
    >>> Computer([3,3,1107,-1,8,3,4,3,99]).run(inp=9).output
    0
    >>> Computer([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]).run(inp=0).output
    0
    >>> Computer([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]).run(inp=1).output
    1
    >>> Computer([3,3,1105,-1,9,1101,0,0,12,4,12,99,1]).run(inp=0).output
    0
    >>> Computer([3,3,1105,-1,9,1101,0,0,12,4,12,99,1]).run(inp=1).output
    1
    >>> Computer([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]).run(inp=7).output
    999
    >>> Computer([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]).run(inp=8).output
    1000
    >>> Computer([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]).run(inp=9).output
    1001
    """
    HALT = 99

    mem: List[int]
    pc: int = 0

    def add(self, param1, param2, dest):
        dest.write(param1.read() + param2.read())

    def mul(self, param1, param2, dest):
        dest.write(param1.read() * param2.read())

    def store(self, dest):
        if self.pause:
            dest.write(self._input.pop(0))
        else:
            if len(self._input) > 1:
                dest.write(self._input.pop(0))
            else:
                dest.write(self._input[0])

    def out(self, param):
        self._output = param.read()
        if self.pause:
            raise Pause()

    def jump_if_true(self, param1, param2):
        if param1.read() != 0:
            self.pc = param2.read()

    def jump_if_false(self, param1, param2):
        if param1.read() == 0:
            self.pc = param2.read()

    def less_than(self, param1, param2, dest):
        dest.write(1 if param1.read() < param2.read() else 0)

    def equals(self, param1, param2, dest):
        dest.write(1 if param1.read() == param2.read() else 0)

    _input = [1]
    _output = None
    halted = False

    _opcode_functions = (
        add,
        mul,
        store,
        out,
        jump_if_true,
        jump_if_false,
        less_than,
        equals,
    )
    _opcodes = {index + 1: (func, len(signature(func).parameters))
                for index, func in enumerate(_opcode_functions)}

    def __post_init__(self):
        self.mem = self.mem.copy()

    @staticmethod
    @lru_cache
    def parse_op(opcode):
        """
        >>> Computer.parse_op(1002)
        (2, (0, 1, 0))
        """
        bits = str(opcode).rjust(5, '0')
        op = int(bits[-2:])
        return (op, tuple(int(mode) for mode in reversed(bits[0:3])))

    def run(self, noun=None, verb=None, inp=None, pause=False):
        if self.halted:
            raise Exception("This computer has already halted!")
        if noun is not None:
            self.mem[1] = noun
        if verb is not None:
            self.mem[2] = verb
        if inp is not None:
            try:
                self._input = list(inp)
            except TypeError:
                self._input = [inp]
        self.pause = pause

        while (opcode := self.mem[self.pc]) != Computer.HALT:
            op, modes = self.parse_op(opcode)
            try:
                op, param_num = self._opcodes[op]
            except KeyError:
                raise Exception(f"Unknown opcode {opcode} at pc {self.pc}")
            params = zip(self.mem[self.pc + 1:self.pc + param_num], modes)
            params = [Param(self, value, mode) for value, mode in params]
            pc_before = self.pc
            try:
                op(self, *params)
            finally:
                if pc_before == self.pc:
                    self.pc += param_num
        self.halted = True
        return self

    @property
    def output(self):
        if self._output is not None:
            return self._output
        return self.mem[0]


@dataclasses.dataclass()
class Param:
    computer: Computer
    value: int
    mode: int = 0

    def read(self):
        if self.mode == 0:
            return self.computer.mem[self.value]
        elif self.mode == 1:
            return self.value
        else:
            raise Exception(f"Unknown mode: {self.mode}")

    def write(self, value):
        self.computer.mem[self.value] = value


if __name__ == "__main__":
    import doctest
    doctest.testmod()
