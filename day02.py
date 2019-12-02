import copy
import dataclasses
from operator import add, mul

from aocd.models import Puzzle

from util import inspect


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
    state: list
    pc: int = 0

    def run(self):
        while (last := self.execute()) != 99:
            self.pc += 4
        return self.state

    def execute(self):
        opcode = self.state[self.pc]
        if opcode != 99:
            if opcode == 1:
                op = add
            elif opcode == 2:
                op = mul
            else:
                raise Exception(f"Unrecognised opcode {opcode} at pc {self.pc}")
            input1, input2, output = self.state[self.pc + 1:self.pc + 4]
            val1 = self.state[input1]
            val2 = self.state[input2]
            self.state[output] = op(val1, val2)
        return opcode


def part1(state):
    comp = Computer(state)
    comp.run()
    return comp.state[0]


# def part2(lines):
#     """
#     >>> part2()
#
#     """


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2019, day=2)
    start_state = [int(val) for val in puzzle.input_data.split(',')]
    state_1 = copy.copy(start_state)
    state_1[1] = 12
    state_1[2] = 2
    puzzle.answer_a = inspect(part1(state_1), prefix='Part 1: ')
    # puzzle.answer_b = inspect(part2(start_state), prefix='Part 2: ')
