from aocd.models import Puzzle

from coord import Coord
from computer import Computer
from util import inspect


def compute_intersections(rows):
    """
    >>> compute_intersections(["..#..........","..#..........","##O####...###","#.#...#...#.#","##O###O###O##","..#...#...#..","..#####...^.."])
    76
    """
    scaffold = set()
    for y, row in enumerate(rows):
        for x, char in enumerate(row):
            if char != '.':
                scaffold.add(Coord(x, y))
    intersections = (scaf for scaf in scaffold if set(scaf.neighbours) <= scaffold)
    return sum(scaf.x * scaf.y for scaf in intersections)


def part1(program):
    computer = Computer(program)
    chars = []
    while not computer.halted:
        next_char = computer.run()
        chars.append(chr(next_char))
    rows = ''.join(chars).split('\n')

    return compute_intersections(rows)

# def part2(program):
#     """
#     >>> part2()
#
#     """


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2019, day=17)
    program = [int(val) for val in puzzle.input_data.split(',')]
    puzzle.answer_a = inspect(part1(program), prefix='Part 1: ')
    # puzzle.answer_b = inspect(part2(program), prefix='Part 2: ')
