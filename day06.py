from aocd.models import Puzzle

from util import inspect


def part1(orbits):
    """
    >>> part1(["COM)B", "B)C", "C)D", "D)E", "E)F", "B)G", "G)H", "D)I", "E)J", "J)K", "K)L"])
    42
    """
    orbit_map = {}
    for orbit in orbits:
        left, right = orbit.split(')')
        orbit_map.setdefault(left, []).append(right)

    stack = [('COM', 0)]
    total = 0
    while stack:
        current, depth = stack.pop()
        total += depth
        for child in orbit_map.get(current, []):
            stack.append((child, depth + 1))
    return total


# def part2(orbits):
#     """
#     >>> part2()
#
#     """


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2019, day=6)
    orbits = puzzle.input_data.split('\n')
    puzzle.answer_a = inspect(part1(orbits), prefix='Part 1: ')
    # puzzle.answer_b = inspect(part2(orbits), prefix='Part 2: ')
