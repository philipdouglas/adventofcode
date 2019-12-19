from collections import defaultdict
from itertools import combinations
from string import ascii_lowercase, ascii_uppercase

from aocd.models import Puzzle

from coord import Coord
from util import inspect


def keys_required(camefrom, pos, key_map):
    path = []
    while pos in camefrom:
        pos = camefrom[pos]
        path.insert(0, pos)
    return {key_map[cell] for cell in path if cell in key_map}


def path_to_target(pos, target, space, doors):
    key_map = {loc: door.lower() for door, loc in doors.items()}
    openset = {pos}
    camefrom = {}
    gscore = defaultdict(lambda: float('inf'))
    gscore[pos] = 0

    while openset:
        current = openset.pop()
        if current == target:
            return gscore[target], keys_required(camefrom, current, key_map)

        for neighbour in current.neighbours:
            if neighbour in space:
                new_gscore = gscore[current] + 1
                if new_gscore < gscore[neighbour]:
                    camefrom[neighbour] = current
                    gscore[neighbour] = new_gscore
                    openset.add(neighbour)


def part1(lines):
    """
    Based on https://www.reddit.com/r/adventofcode/comments/ec8090/2019_day_18_solutions/fbd8y0b

    >>> part1(["#########","#b.A.@.a#","#########"])
    8
    >>> part1(["########################","#f.D.E.e.C.b.A.@.a.B.c.#","######################.#","#d.....................#","########################"])
    86
    >>> part1(["########################","#...............b.C.D.f#","#.######################","#.....@.a.B.c.d.A.e.F.g#","########################"])
    132
    >>> part1(["########################","#@..............ac.GI.b#","###d#e#f################","###A#B#C################","###g#h#i################","########################"])
    81
    >>> part1(["#################","#i.G..c...e..H.p#","########.########","#j.A..b...f..D.o#","########@########","#k.E..a...g..B.n#","########.########","#l.F..d...h..C.m#","#################"])
    136
    """
    open_space = set()
    all_space = set()
    start = None
    all_keys = {}
    doors = {}
    for y, row in enumerate(lines):
        for x, cell in enumerate(row):
            current = Coord(x, y)
            if cell != '#':
                all_space.add(current)
                if cell not in ascii_uppercase:
                    open_space.add(current)
            if cell == '@':
                start = current
            elif cell in ascii_lowercase:
                all_keys[cell] = current
            elif cell in ascii_uppercase:
                doors[cell] = current

    all_points = list(all_keys.values()) + [start]
    routes = {}
    for point_a, point_b in combinations(all_points, 2):
        distance, keys_needed = path_to_target(point_a, point_b, all_space, doors)
        if point_a != start:
            routes.setdefault(point_b, []).append((point_a, distance, set(keys_needed)))
        if point_b != start:
            routes.setdefault(point_a, []).append((point_b, distance, set(keys_needed)))

    key_locs = {loc: key for key, loc in all_keys.items()}

    cache = {}

    def reachable(current, keys):
        for dest, dist, required in routes[current]:
            if required.isdisjoint(keys) and key_locs[dest] in keys:
                yield key_locs[dest], dist

    def distance_to_collect(current, keys):
        if not keys:
            return 0

        cache_key = f"{current} {repr(keys)}"
        if cache_key in cache:
            return cache[cache_key]

        result = float('inf')
        for key, dist in reachable(current, keys):
            new_dist = dist + distance_to_collect(all_keys[key], keys - {key})
            result = min(result, new_dist)

        cache[cache_key] = result
        return result

    return distance_to_collect(start, set(all_keys.keys()))


# def part2(lines):
#     """
#     >>> part2()
#
#     """


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2019, day=18)
    lines = puzzle.input_data.split('\n')
    puzzle.answer_a = inspect(part1(lines), prefix='Part 1: ')
    # puzzle.answer_b = inspect(part2(lines), prefix='Part 2: ')
