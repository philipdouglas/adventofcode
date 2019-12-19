import collections
import dataclasses
from functools import lru_cache
from inspect import signature
from typing import List


class Pause(Exception):
    pass


class Halted(Exception):
    pass


@dataclasses.dataclass()
class Computer:
    """
    >>> c1 = Computer([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50])
    >>> c1.run()
    >>> c1.get_mem()
    [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
    >>> c2 = Computer([1, 0, 0, 0, 99])
    >>> c2.run()
    >>> c2.get_mem()
    [2, 0, 0, 0, 99]
    >>> c3 = Computer([2, 3, 0, 3, 99])
    >>> c3.run()
    >>> c3.get_mem()
    [2, 3, 0, 6, 99]
    >>> c4 = Computer([2, 4, 4, 5, 99, 0])
    >>> c4.run()
    >>> c4.get_mem()
    [2, 4, 4, 5, 99, 9801]
    >>> c5 = Computer([1, 1, 1, 4, 99, 5, 6, 0, 99])
    >>> c5.run()
    >>> c5.get_mem()
    [30, 1, 1, 4, 2, 5, 6, 0, 99]
    >>> Computer([3,0,4,0,99], input=7).run()
    7
    >>> Computer([3,9,8,9,10,9,4,9,99,-1,8], input=8).run()
    1
    >>> Computer([3,9,8,9,10,9,4,9,99,-1,8], input=5).run()
    0
    >>> Computer([3,9,7,9,10,9,4,9,99,-1,8], input=7).run()
    1
    >>> Computer([3,9,7,9,10,9,4,9,99,-1,8], input=8).run()
    0
    >>> Computer([3,3,1108,-1,8,3,4,3,99], input=8).run()
    1
    >>> Computer([3,3,1108,-1,8,3,4,3,99], input=1).run()
    0
    >>> Computer([3,3,1107,-1,8,3,4,3,99], input=7).run()
    1
    >>> Computer([3,3,1107,-1,8,3,4,3,99], input=9).run()
    0
    >>> Computer([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], input=0).run()
    0
    >>> Computer([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], input=1).run()
    1
    >>> Computer([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], input=0).run()
    0
    >>> Computer([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], input=1).run()
    1
    >>> Computer([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], input=7).run()
    999
    >>> Computer([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], input=8).run()
    1000
    >>> Computer([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], input=9).run()
    1001
    >>> c = Computer([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99])
    >>> c.run()
    109
    >>> c.get_mem()
    [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    >>> Computer([1102,34915192,34915192,7,4,7,99,0]).run()
    1219070632396864
    >>> Computer([104,1125899906842624,99]).run()
    1125899906842624
    >>> c6 = Computer([9, 1, 203, 1, 99], input=5)
    >>> c6.run()
    >>> c6.get_mem()
    [9, 1, 5, 1, 99]
    """
    HALT = 99

    def add(self, param1, param2, dest):
        dest.write(param1.read() + param2.read())

    def mul(self, param1, param2, dest):
        dest.write(param1.read() * param2.read())

    def store(self, dest):
        if self._input is None:
            raise Exception("Input needed but none was provided")

        try:
            dest.write(self._input())
        except TypeError:
            try:
                dest.write(self._input.pop(0))
            except IndexError:
                raise Exception("Input list empty")
            except AttributeError:
                dest.write(self._input)

    def out(self, param):
        self._output = param.read()
        raise Pause()

    def jump_if_true(self, param1, param2):
        if param1.read() != 0:
            self._pc = param2.read()

    def jump_if_false(self, param1, param2):
        if param1.read() == 0:
            self._pc = param2.read()

    def less_than(self, param1, param2, dest):
        dest.write(1 if param1.read() < param2.read() else 0)

    def equals(self, param1, param2, dest):
        dest.write(1 if param1.read() == param2.read() else 0)

    def base(self, param):
        self._relative_base += param.read()

    _pc = 0
    _mem = None
    _relative_base = 0
    _input = None
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
        base,
    )
    _opcodes = {index + 1: (func, len(signature(func).parameters))
                for index, func in enumerate(_opcode_functions)}

    def __init__(self, program, mem_override=None, input=None):
        self._mem = collections.defaultdict(int)
        self._mem.update({index: val for index, val in enumerate(program)})

        if mem_override:
            self._mem.update(mem_override)

        self._input = input

    @staticmethod
    @lru_cache(maxsize=32)
    def parse_op(opcode):
        """
        >>> Computer.parse_op(1002)
        (2, (0, 1, 0))
        >>> Computer.parse_op(1202)
        (2, (2, 1, 0))
        """
        bits = str(opcode).rjust(5, '0')
        op = int(bits[-2:])
        return (op, tuple(int(mode) for mode in reversed(bits[0:3])))

    def get_params(self, param_num, modes):
        params = list(self._mem.values())[self._pc + 1:self._pc + param_num]
        params = zip(params, modes)
        return [Param(self, value, mode) for value, mode in params]

    def run(self):
        if self.halted:
            raise Halted()

        while (opcode := self._mem[self._pc]) != Computer.HALT:
            op, modes = self.parse_op(opcode)
            try:
                op, param_num = self._opcodes[op]
            except KeyError:
                raise Exception(f"Unknown opcode {opcode} at pc {self._pc}")
            params = self.get_params(param_num, modes)
            pc_before = self._pc
            try:
                op(self, *params)
            except Pause:
                return self.output
            finally:
                if pc_before == self._pc:
                    self._pc += param_num
        self.halted = True
        return self.output

    @property
    def output(self):
        return self._output

    def get_mem(self):
        return list(self._mem.values())

    @property
    def mem0(self):
        """
        Used by early puzzles before output was added
        """
        return self._mem[0]

    def add_input(self, value):
        try:
            self._input += value
        except ValueError:
            self._input.append(value)


@dataclasses.dataclass()
class Param:
    computer: Computer
    value: int
    mode: int = 0

    def read(self):
        if self.mode == 0:
            return self.computer._mem[self.value]
        elif self.mode == 1:
            return self.value
        elif self.mode == 2:
            return self.computer._mem[self.computer._relative_base + self.value]
        else:
            raise Exception(f"Unknown mode: {self.mode}")

    def write(self, value):
        if self.mode == 0:
            self.computer._mem[self.value] = value
        elif self.mode == 1:
            raise Exception("Cannot write to immediate mode parameter!")
        elif self.mode == 2:
            self.computer._mem[self.computer._relative_base + self.value] = value
        else:
            raise Exception(f"Unknown mode: {self.mode}")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
