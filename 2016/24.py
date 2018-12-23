from collections import defaultdict
from itertools import permutations

from coord import BlockCoord

TEST_INPUT = [
    '###########',
    '#0.1.....2#',
    '#.#######.#',
    '#4.......3#',
    '###########',
]


class MapCoord(BlockCoord):
    def is_valid(self, map_):
        return map_[self.y][self.x] != '#'


STEPS = (MapCoord(-1, 0), MapCoord(1, 0), MapCoord(0, -1), MapCoord(0, 1))


def generate_steps(map_, location):
    for step in STEPS:
        maybe = location + step
        if maybe.is_valid(map_):
            yield maybe


def reconstruct_path(came_from, node):
    path = []
    while node in came_from:
        node = came_from[node]
        path.insert(0, node)
    return path


def shortest_route(map_, start, end):
    """
    >>> shortest_route(TEST_INPUT, MapCoord(1, 1), MapCoord(3, 1))
    2
    >>> shortest_route(TEST_INPUT, MapCoord(1, 1), MapCoord(9, 3))
    10
    """
    closed_set = set()
    open_set = set([start])
    came_from = {}
    gscores = {start: 0}
    fscores = defaultdict(lambda: float('inf'))
    fscores[start] = start.distance_blocks(end)

    while open_set:
        current = sorted(open_set, key=lambda node: fscores[node])[0]
        if current == end:
            path = reconstruct_path(came_from, current)
            return len(path)

        open_set.remove(current)
        closed_set.add(current)

        for neighbor in generate_steps(map_, current):
            if neighbor in closed_set:
                continue

            gscore = gscores[current] + 1
            if neighbor not in open_set:
                open_set.add(neighbor)
            elif gscore >= gscores[neighbor]:
                continue

            came_from[neighbor] = current
            gscores[neighbor] = gscore
            fscores[neighbor] = gscore + neighbor.distance_blocks(end)
    raise Exception()


def get_nodes(map_):
    """
    >>> get_nodes(TEST_INPUT)
    {0: (1, 1), 1: (3, 1), 2: (9, 1), 3: (9, 3), 4: (1, 3)}
    """
    nodes = {}
    for y in range(len(map_)):
        for x in range(len(map_[y])):
            if map_[y][x] not in ['#', '.']:
                nodes[int(map_[y][x])] = MapCoord(x=x, y=y)
    return nodes


def meta_shortest_route(map_, part2=False):
    """
    >>> meta_shortest_route(TEST_INPUT)
    14
    """
    nodes = get_nodes(map_)
    routes = {}
    for startnum, start in nodes.items():
        routes.setdefault(startnum, {})
        for endnum, end in nodes.items():
            routes.setdefault(endnum, {})

            if startnum == endnum or endnum == 0 or startnum > endnum:
                continue
            distance = shortest_route(map_, start, end)
            routes[startnum][endnum] = distance
            routes[endnum][startnum] = distance

    shortest = float('inf')
    nodenums = list(nodes.keys())
    for route in permutations(nodenums[1:], len(nodes) - 1):
        distance = 0
        prev = 0
        for nodenum in route:
            distance += routes[prev][nodenum]
            prev = nodenum
            if distance > shortest:
                break
        else:
            if part2:
                distance += routes[prev][0]
            if distance < shortest:
                shortest = distance
    return shortest


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    with open('24input.txt', 'r') as inputfile:
        map_ = inputfile.read().split('\n')[:-1]
        print("Part 1: {}".format(meta_shortest_route(map_)))
        print("Part 2: {}".format(meta_shortest_route(map_, part2=True)))
