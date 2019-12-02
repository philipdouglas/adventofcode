import copy
import dataclasses
import itertools
from operator import add, mul

from aocd.models import Puzzle

from util import inspect


class Halt(Exception):
    pass


@dataclasses.dataclass()
class Computer:
    """
    >>> Computer([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]).run()
    [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
    >>> Computer([1, 0, 0, 0, 99]).run()
    [2, 0, 0, 0, 99]
    >>> Computer([2, 3, 0, 3, 99]).run()
    [2, 3, 0, 6, 99]
    >>> Computer([2, 4, 4, 5, 99, 0]).run()
    [2, 4, 4, 5, 99, 9801]
    >>> Computer([1, 1, 1, 4, 99, 5, 6, 0, 99]).run()
    [30, 1, 1, 4, 2, 5, 6, 0, 99]
    """
    mem: list
    pc: int = 0

    def run(self):
        try:
            while True:
                self.execute()
        except Halt:
            return self.mem

    def execute(self):
        opcode = self.mem[self.pc]
        if opcode == 99:
            raise Halt()
        elif opcode == 1:
            op = add
        elif opcode == 2:
            op = mul
        else:
            raise Exception(f"Unrecognised opcode {opcode} at pc {self.pc}")
        input1, input2, output = self.mem[self.pc + 1:self.pc + 4]
        val1 = self.mem[input1]
        val2 = self.mem[input2]
        self.mem[output] = op(val1, val2)
        self.pc += 4


def part1(state):
    comp = Computer(state)
    comp.run()
    return comp.mem[0]


def part2(state):
    TARGET = 19690720
    for noun, verb in itertools.product(range(100), range(100)):
        new_state = copy.copy(state)
        new_state[1] = noun
        new_state[2] = verb
        comp = Computer(new_state)
        comp.run()
        # print(f"{noun}, {verb}: {comp.mem[0]}")
        if comp.mem[0] == TARGET:
            return 100 * noun + verb


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2019, day=2)
    start_state = [int(val) for val in puzzle.input_data.split(',')]
    state_1 = copy.copy(start_state)
    state_1[1] = 12
    state_1[2] = 2
    puzzle.answer_a = inspect(part1(state_1), prefix='Part 1: ')
    puzzle.answer_b = inspect(part2(start_state), prefix='Part 2: ')
