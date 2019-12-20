from collections import defaultdict
from itertools import islice
from re import findall

from aocd.models import Puzzle

from coord import Coord
from util import inspect

example_1 = [
    "         A           ",
    "         A           ",
    "  #######.#########  ",
    "  #######.........#  ",
    "  #######.#######.#  ",
    "  #######.#######.#  ",
    "  #######.#######.#  ",
    "  #####  B    ###.#  ",
    "BC...##  C    ###.#  ",
    "  ##.##       ###.#  ",
    "  ##...DE  F  ###.#  ",
    "  #####    G  ###.#  ",
    "  #########.#####.#  ",
    "DE..#######...###.#  ",
    "  #.#########.###.#  ",
    "FG..#########.....#  ",
    "  ###########.#####  ",
    "             Z       ",
    "             Z       ",
]
example_2 = [
    "                   A               ",
    "                   A               ",
    "  #################.#############  ",
    "  #.#...#...................#.#.#  ",
    "  #.#.#.###.###.###.#########.#.#  ",
    "  #.#.#.......#...#.....#.#.#...#  ",
    "  #.#########.###.#####.#.#.###.#  ",
    "  #.............#.#.....#.......#  ",
    "  ###.###########.###.#####.#.#.#  ",
    "  #.....#        A   C    #.#.#.#  ",
    "  #######        S   P    #####.#  ",
    "  #.#...#                 #......VT",
    "  #.#.#.#                 #.#####  ",
    "  #...#.#               YN....#.#  ",
    "  #.###.#                 #####.#  ",
    "DI....#.#                 #.....#  ",
    "  #####.#                 #.###.#  ",
    "ZZ......#               QG....#..AS",
    "  ###.###                 #######  ",
    "JO..#.#.#                 #.....#  ",
    "  #.#.#.#                 ###.#.#  ",
    "  #...#..DI             BU....#..LF",
    "  #####.#                 #.#####  ",
    "YN......#               VT..#....QG",
    "  #.###.#                 #.###.#  ",
    "  #.#...#                 #.....#  ",
    "  ###.###    J L     J    #.#.###  ",
    "  #.....#    O F     P    #.#...#  ",
    "  #.###.#####.#.#####.#####.###.#  ",
    "  #...#.#.#...#.....#.....#.#...#  ",
    "  #.#####.###.###.#.#.#########.#  ",
    "  #...#.#.....#...#.#.#.#.....#.#  ",
    "  #.###.#####.###.###.#.#.#######  ",
    "  #.#.........#...#.............#  ",
    "  #########.###.###.#############  ",
    "           B   J   C               ",
    "           U   P   P               ",
]


def process_line(line, coord_builder, portals, unmatched):
    if found := findall(r'([A-Z]{2})', line):
        for portal in found:
            pos = line.find(portal)
            if pos > 0 and line[pos - 1] == '.':
                var = pos - 1
            elif pos < (len(line) - 2) and line[pos + 2] == '.':
                var = pos + 2
            else:
                raise Exception("can't find portal space")
            coordinates = coord_builder(var)
            if portal in unmatched:
                portals[coordinates] = unmatched[portal]
                portals[unmatched[portal]] = coordinates
            else:
                unmatched[portal] = coordinates


def reconstruct_path(camefrom, pos):
    path = []
    while pos in camefrom:
        pos = camefrom[pos]
        path.insert(0, pos)
    return path


def pathfind(donut, portals, start, finish):
    openset = {start}
    camefrom = {}
    gscore = defaultdict(lambda: float('inf'))
    gscore[start] = 0
    # shortest = float('inf')

    while openset:
        current = openset.pop()

        if current == finish:
            length = len(reconstruct_path(camefrom, current))
            return length
            # if length < shortest:
            #     shortest = length

        options = [nbor for nbor in current.neighbours if donut[nbor.y][nbor.x] == '.']
        if current in portals:
            options.append(portals[current])

        for option in options:
            new_gscore = gscore[current] + 1
            if new_gscore < gscore[option]:
                camefrom[option] = current
                gscore[option] = new_gscore
                openset.add(option)
    # return shortest


def part1(donut):
    """
    >>> part1(example_1)
    23
    >>> part1(example_2)
    58
    """
    portals = {}
    unmatched = {}
    for y, row in enumerate(donut):
        process_line(row, lambda x: Coord(x, y), portals, unmatched)
    for x in range(len(donut[0])):
        column = ''.join([row[x] for row in donut])
        process_line(column, lambda y: Coord(x, y), portals, unmatched)
    begin = unmatched['AA']
    end = unmatched['ZZ']

    return pathfind(donut, portals, begin, end)


# def part2(donut):
#     """
#     >>> part2()
#
#     """


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2019, day=20)
    donut = puzzle.input_data.split('\n')
    puzzle.answer_a = inspect(part1(donut), prefix='Part 1: ')
    # puzzle.answer_b = inspect(part2(donut), prefix='Part 2: ')
