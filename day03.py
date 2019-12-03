from aocd.models import Puzzle

from coord import Coord
from util import inspect


def follow_line(instructions):
    pos = Coord(0, 0)
    for inst in instructions.split(','):
        direction = inst[0]
        distance = int(inst[1:])
        for _ in range(distance):
            if direction == 'U':
                pos = pos.up()
            elif direction == 'R':
                pos = pos.right()
            elif direction == 'D':
                pos = pos.down()
            elif direction == 'L':
                pos = pos.left()
            yield pos


def part1(line1, line2):
    """
    >>> part1('R8,U5,L5,D3', 'U7,R6,D4,L4')
    6
    >>> part1('R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83')
    159
    >>> part1('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7')
    135
    """
    points = set(follow_line(line1))
    return min(pos.manhatten_dist() for pos in follow_line(line2) if pos in points)


def part2(line1, line2):
    """
    >>> part2('R8,U5,L5,D3', 'U7,R6,D4,L4')
    30
    >>> part2('R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83')
    610
    >>> part2('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7')
    410
    """
    points = {pos: steps + 1 for steps, pos in enumerate(follow_line(line1))}
    return min(steps + 1 + points[pos] for steps, pos in enumerate(follow_line(line2))
               if pos in points)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2019, day=3)
    lines = puzzle.input_data.split('\n')
    puzzle.answer_a = inspect(part1(*lines), prefix='Part 1: ')
    puzzle.answer_b = inspect(part2(*lines), prefix='Part 2: ')
