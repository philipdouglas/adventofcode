from collections import defaultdict
from os.path import realpath

from aocd.models import Puzzle

from computer import Computer
from coord import Coord
from util import inspect


def find_goal(known, program):
    bot = Computer(program, input=[])
    pos = Coord(0, 0)
    known[pos] = 1
    explored = defaultdict(int)
    last_explored = {pos: 0}
    steps = 0

    while True:
        # draw(known, pos)
        # command = input()
        backtrack = []
        for inst, target in [(1, pos.up()), (3, pos.left()), (2, pos.down()), (4, pos.right())]:
            if target in known:
                if known[target] == 1:
                    backtrack.append((target, inst))
                continue
            break
        else:
            backtrack.sort(key=lambda pair: last_explored[pair[0]])
            backtrack.sort(key=lambda pair: explored[pair[0]])
            target, inst = backtrack[0]

        bot.add_input(inst)
        result = bot.run()

        if target in known:
            assert result == known[target]
        else:
            known[target] = result
            for adjacent in [target.up(), target.down(), target.left(), target.right()]:
                explored[adjacent] += 1

        steps += 1

        if result == 2:
            pos = target
            break
        elif result == 0:
            continue
        elif result == 1:
            pos = target
            last_explored[pos] = steps
    return target


def reconstruct_path(cameform, pos):
    path = []
    while pos in cameform:
        pos = cameform[pos]
        path.insert(0, pos)
    return len(path)


def shortest_route(known, target):
    start = Coord(0, 0)
    openset = [start]
    camefrom = {}
    gscore = defaultdict(lambda: float('inf'))
    gscore[start] = 0
    fscore = defaultdict(lambda: float('inf'))
    fscore[start] = start.manhatten_dist()

    while openset:
        openset.sort(key=lambda c: fscore[c])
        current = openset.pop(0)
        if current not in known:
            # print(f"Unknown {current}, skipping...")
            continue
        elif known[current] == 2:
            return reconstruct_path(camefrom, current)
        elif known[current] == 0:
            continue

        for neighbour in current.neighbours:
            new_gscore = gscore[current] + 1
            if new_gscore < gscore[neighbour]:
                camefrom[neighbour] = current
                gscore[neighbour] = new_gscore
                fscore[neighbour] = new_gscore + neighbour.manhatten_dist()
                if neighbour not in openset:
                    openset.append(neighbour)


TILES = {
    -1: '?',
    0: '#',
    1: ' ',
    2: 'O',
}


def draw(known, bot_pos):
    minx_coord = min(c.x for c in known.keys()) - 1
    miny_coord = min(c.y for c in known.keys()) - 1
    maxx_coord = max(c.x for c in known.keys()) + 1
    maxy_coord = max(c.y for c in known.keys()) + 1

    rows = []
    for y in range(maxy_coord, miny_coord - 1, -1):
        row = []
        for x in range(minx_coord, maxx_coord + 1):
            current = Coord(x, y)
            if current == bot_pos:
                row.append('B')
            else:
                tile = known.get(current, -1)
                row.append(TILES[tile])
        rows.append(''.join(row))
    print('\n'.join(rows))


def part1(program):
    known = {}
    goal = find_goal(known, program)
    return shortest_route(known, goal)


def part2(program):
    known = {}
    start = find_goal(known, program)
    vacuum = {pos for pos, value in known.items() if value == 1}
    oxygenated = {start}
    minutes = 0
    while vacuum:
        spread_to = set()
        for pos in oxygenated:
            for neighbour in pos.neighbours:
                if neighbour in vacuum:
                    spread_to.add(neighbour)
        minutes += 1
        vacuum -= spread_to
        oxygenated |= spread_to
    return minutes


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2019, day=15)
    program = [int(val) for val in puzzle.input_data.split(',')]
    puzzle.answer_a = inspect(part1(program), prefix='Part 1: ')
    puzzle.answer_b = inspect(part2(program), prefix='Part 2: ')
