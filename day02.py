import itertools

from aocd.models import Puzzle

from computer import Computer
from util import inspect


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
