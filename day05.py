from aocd.models import Puzzle

from computer import Computer
from util import inspect


def part1(program):
    comp = Computer(program, input=1)
    while not comp.halted:
        comp.run()
    return comp.output


def part2(program):
    return Computer(program, input=5).run()


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2019, day=5)
    program = [int(val) for val in puzzle.input_data.split(',')]
    puzzle.answer_a = inspect(part1(program), prefix='Part 1: ')
    puzzle.answer_b = inspect(part2(program), prefix='Part 2: ')
