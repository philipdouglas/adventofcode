
from collections import defaultdict
from os.path import realpath

from aocd.models import Puzzle

from computer import Computer, Pause
from coord import Coord
from util import inspect


def paint(program, start):
    hull = defaultdict(int)
    position = Coord(0, 0)
    direction = Coord(0, 1)
    computer = Computer(program)
    computer._input = []
    hull[position] = start

    while True:
        computer._input.append(hull[position])
        try:
            computer.run(pause=True)
            break
        except Pause:
            hull[position] = computer.output
            try:
                computer.run(pause=True)
                break
            except Pause:
                turn = computer.output
                if turn == 0:
                    direction = direction.rotate_left()
                else:
                    direction = direction.rotate_right()
                position = position + direction
    return hull


def part1(program):
    return len(paint(program, start=0))


def part2(program):
    hull = paint(program, start=1)
    minx_coord = min(c.x for c in hull.keys())
    miny_coord = min(c.y for c in hull.keys())
    maxx_coord = max(c.x for c in hull.keys())
    maxy_coord = max(c.y for c in hull.keys())

    visualisation = []
    for y in range(maxy_coord, miny_coord - 1, -1):
        row = []
        for x in range(minx_coord, maxx_coord + 1):
            if hull[Coord(x, y)] == 1:
                row.append('█')
            else:
                row.append(' ')
        visualisation.append(''.join(row))
    return input('Hull:\n' + '\n'.join(visualisation))



if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2019, day=11)
    program = [int(val) for val in puzzle.input_data.split(',')]
    puzzle.answer_a = inspect(part1(program), prefix='Part 1: ')
    puzzle.answer_b = inspect(part2(program), prefix='Part 2: ')
