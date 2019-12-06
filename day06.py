from itertools import zip_longest

from aocd.models import Puzzle

from util import inspect


def build_routes(orbits):
    orbit_map = {}
    for orbit in orbits:
        left, right = orbit.split(')')
        orbit_map.setdefault(left, []).append(right)

    stack = ['COM']
    routes = {'COM': []}
    while stack:
        current = stack.pop()
        for child in orbit_map.get(current, []):
            routes[child] = routes[current] + [current]
            stack.append(child)
    return routes


def part1(orbits):
    """
    >>> part1(["COM)B", "B)C", "C)D", "D)E", "E)F", "B)G", "G)H", "D)I", "E)J", "J)K", "K)L"])
    42
    """
    routes = build_routes(orbits)
    return sum([len(route) for route in routes.values()])


def part2(orbits):
    """
    >>> part2(["COM)B", "B)C", "C)D", "D)E", "E)F", "B)G", "G)H", "D)I", "E)J", "J)K", "K)L", "K)YOU", "I)SAN"])
    4
    """
    routes = build_routes(orbits)
    return len(set(routes['YOU']) ^ set(routes['SAN']))


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2019, day=6)
    orbits = puzzle.input_data.split('\n')
    puzzle.answer_a = inspect(part1(orbits), prefix='Part 1: ')
    puzzle.answer_b = inspect(part2(orbits), prefix='Part 2: ')
