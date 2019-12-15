from collections import defaultdict
from os.path import realpath

from aocd.models import Puzzle

from computer import Computer
from coord import Coord
from util import inspect


def find_goal(program, debug=True):
    bot = Computer(program, input=[])
    pos = Coord(0, 0)
    known = {pos: 1}
    explored = defaultdict(int)
    last_visited = {pos: 0}
    steps = 0

    while True:
        if debug:
            draw(known, pos)
            input()
        backtrack = []
        for inst, target in zip([1, 3, 2, 4], list(pos.neighbours)):
            if target in known:
                if known[target] == 1:
                    backtrack.append((target, inst))
                continue
            break
        else:
            backtrack.sort(key=lambda pair: last_visited[pair[0]])
            backtrack.sort(key=lambda pair: explored[pair[0]])
            target, inst = backtrack[0]

        bot.add_input(inst)
        result = bot.run()

        if target not in known:
            known[target] = result
            for adjacent in target.neighbours:
                explored[adjacent] += 1

        if result == 0:
            continue

        steps += 1
        pos = target
        if result == 2:
            break
        elif result == 1:
            last_visited[pos] = steps
    return target, known


def reconstruct_path(cameform, pos):
    path = []
    while pos in cameform:
        pos = cameform[pos]
        path.insert(0, pos)
    return len(path)


def shortest_route(known, target):
    start = Coord(0, 0)
    openset = {start}
    camefrom = {}
    gscore = defaultdict(lambda: float('inf'))
    gscore[start] = 0

    while openset:
        current = openset.pop()
        if current not in known or known[current] == 0:
            continue
        elif known[current] == 2:
            return reconstruct_path(camefrom, current)

        for neighbour in current.neighbours:
            new_gscore = gscore[current] + 1
            if new_gscore < gscore[neighbour]:
                camefrom[neighbour] = current
                gscore[neighbour] = new_gscore
                openset.add(neighbour)


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


def part1(goal, known):
    return shortest_route(known, goal)


def part2(goal, known):
    vacuum = {pos for pos, value in known.items() if value == 1}
    oxygenated = {goal}
    minutes = 0
    while vacuum:
        spread_to = {neighbour for oxy in oxygenated for neighbour in oxy.neighbours}
        spread_to &= vacuum
        vacuum -= spread_to
        oxygenated |= spread_to
        minutes += 1
    return minutes


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2019, day=15)
    program = [int(val) for val in puzzle.input_data.split(',')]
    goal, known = find_goal(program, debug=False)
    puzzle.answer_a = inspect(part1(goal, known), prefix='Part 1: ')
    puzzle.answer_b = inspect(part2(goal, known), prefix='Part 2: ')
