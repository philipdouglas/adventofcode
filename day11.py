
from collections import defaultdict
from os.path import realpath

from aocd.models import Puzzle

from computer import Computer, Pause
from coord import Coord
from util import inspect


def part1(program):
    hull = defaultdict(int)
    position = Coord(0, 0)
    direction = Coord(0, 1)
    computer = Computer(program)
    computer._input = []

    while True:
        computer._input.append(hull[position])
        try:
            computer.run(pause=True)
            print("break1")
            break
        except Pause:
            hull[position] = computer.output
            try:
                computer.run(pause=True)
                print("break2")
                break
            except Pause:
                turn = computer.output
                if turn == 0:
                    direction = direction.rotate_left()
                else:
                    direction = direction.rotate_right()
                position = position + direction
    return len(hull)


# def part2(program):
#     """
#     >>> part2()
#
#     """


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2019, day=11)
    program = [int(val) for val in puzzle.input_data.split(',')]
    puzzle.answer_a = inspect(part1(program), prefix='Part 1: ')
    # puzzle.answer_b = inspect(part2(program), prefix='Part 2: ')
