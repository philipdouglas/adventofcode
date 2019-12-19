from aocd.models import Puzzle

from computer import Computer
from util import inspect


def part1(program):
    count = 0
    for y in range(50):
        for x in range(50):
            bot = Computer(program, input=[x, y])
            count += bot.run()
    return count


# def part2(program):
#     """
#     >>> part2()
#
#     """


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2019, day=19)
    program = [int(val) for val in puzzle.input_data.split(',')]
    puzzle.answer_a = inspect(part1(program), prefix='Part 1: ')
    # puzzle.answer_b = inspect(part2(program), prefix='Part 2: ')
