import dataclasses
import itertools
import operator
from typing import List

from aocd.models import Puzzle

from util import inspect


class Halt(Exception):
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
    """
    mem: List[int]
    pc: int = 0

    _opcodes = {
        1: operator.add,
        2: operator.mul,
    }

    def __post_init__(self):
        self.mem = self.mem.copy()

    def run(self, noun=None, verb=None):
        if noun is not None:
            self[1] = noun
        if verb is not None:
            self[2] = verb

        while (opcode := self.mem[self.pc]) != 99:
            try:
                op = self._opcodes[opcode]
            except KeyError:
                raise Exception(f"Unknown opcode {opcode} at pc {self.pc}")
            input1, input2, output = self.mem[self.pc + 1:self.pc + 4]
            self[output] = op(self[input1], self[input2])
            self.pc += 4
        return self

    def __getitem__(self, key):
        return self.mem[key]

    def __setitem__(self, key, value):
        self.mem[key] = value

    @property
    def output(self):
        return self[0]


def part1(state):
    return Computer(state).run(12, 2).output


def part2(state):
    TARGET = 19690720
    for noun, verb in itertools.product(range(100), repeat=2):
        if Computer(state).run(noun, verb).output == TARGET:
            return 100 * noun + verb


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2019, day=2)
    state = [int(val) for val in puzzle.input_data.split(',')]
    puzzle.answer_a = inspect(part1(state), prefix='Part 1: ')
    puzzle.answer_b = inspect(part2(state), prefix='Part 2: ')
