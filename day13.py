from aocd.models import Puzzle

from computer import Computer, Pause
from coord import Coord
from util import inspect


def part1(program):
    screen = {}
    computer = Computer(program)
    while not computer.halted:
        try:
            computer.run(pause=True)
        except Pause:
            pass
        else:
            break
        x = computer.output
        try:
            computer.run(pause=True)
        except Pause:
            pass
        else:
            break
        y = computer.output
        pos = Coord(x, y)
        try:
            computer.run(pause=True)
        except Pause:
            pass
        else:
            break
        tile_id = computer.output
        screen[pos] = tile_id
    return len([tile for tile in screen.values() if tile == 2])

# def part2(program):
#     """
#     >>> part2()
#
#     """


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2019, day=13)
    program = [int(val) for val in puzzle.input_data.split(',')]
    puzzle.answer_a = inspect(part1(program), prefix='Part 1: ')
    # puzzle.answer_b = inspect(part2(program), prefix='Part 2: ')
