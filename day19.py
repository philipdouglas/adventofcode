from aocd.models import Puzzle

from computer import Computer
from util import inspect


def part1(program):
    count = 0
    for y in range(50):
        for x in range(50):
            bot = Computer(program, input=[x, y])
            value = bot.run()
            count += value
            # print('#' if value == 1 else '.', end='')
        # print()
    return count


def check_coord(program, x, y):
    bot = Computer(program, input=[x, y])
    value = bot.run()
    return bool(value)


def part2(program):
    """
    Basically stolen from https://www.reddit.com/r/adventofcode/comments/ecogl3/2019_day_19_solutions/fbdmn5n?utm_source=share&utm_medium=web2x
    I got stuck.
    """
    x = y = 0
    while not check_coord(program, x + 99, y):
        y += 1
        if not check_coord(program, x, y + 99):
            x += 1
    return (x * 10000) + y



if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2019, day=19)
    program = [int(val) for val in puzzle.input_data.split(',')]
    puzzle.answer_a = inspect(part1(program), prefix='Part 1: ')
    puzzle.answer_b = inspect(part2(program), prefix='Part 2: ')
