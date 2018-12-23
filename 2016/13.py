from collections import defaultdict

from coord import BlockCoord, Coord


FAVE = 1364
STEPS = (Coord(-1, 0), Coord(1, 0), Coord(0, -1), Coord(0, 1))


class CubeCoord(BlockCoord):
    def is_wall(self, fave=FAVE):
        """
        >>> CubeCoord(0, 0).is_wall(10)
        False
        >>> CubeCoord(1, 0).is_wall(10)
        True
        >>> CubeCoord(0, 1).is_wall(10)
        False
        """
        value = ((self.x * self.x) + (3 * self.x) + (2 * self.x * self.y) +
                 self.y + (self.y * self.y))
        value += fave
        binary = '{0:20b}'.format(value)
        ones = binary.count('1')
        if ones % 2:
            return True
        return False

    def is_open(self, fave=FAVE):
        return not self.is_wall


def reconstruct_path(came_from, node):
    path = []
    while node in came_from:
        node = came_from[node]
        path.insert(0, node)
    return path


def navigate(startx, starty, targetx, targety, fave=FAVE):
    """
    >>> navigate(1, 1, 7, 4, 10)
    11
    """
    start = CubeCoord(x=startx, y=starty)
    target = CubeCoord(x=targetx, y=targety)

    closed_set = set()
    open_set = set([start])
    came_from = {}
    gscores = {start: 0}
    fscores = defaultdict(lambda: float('inf'))
    fscores[start] = start.distance_blocks(target)

    while open_set:
        current = sorted(open_set, key=lambda node: fscores[node])[0]
        if current == target:
            path = reconstruct_path(came_from, current)
            return len(path)

        open_set.remove(current)
        closed_set.add(current)

        for step in STEPS:
            neighbor = current + step
            if neighbor.x < 0 or neighbor.y < 0:
                continue
            if neighbor.is_wall(fave):
                continue
            if neighbor in closed_set:
                continue

            gscore = gscores[current] + 1
            if neighbor not in open_set:
                open_set.add(neighbor)
            elif gscore >= gscores[neighbor]:
                continue

            came_from[neighbor] = current
            gscores[neighbor] = gscore
            fscores[neighbor] = gscore + neighbor.distance_blocks(target)
    raise Exception()


def explore(startx, starty, fave=FAVE):
    start = CubeCoord(x=startx, y=starty)

    closed_set = set()
    open_set = [start]
    gscores = {start: 0}

    unique_nodes = set()

    while open_set:
        current = open_set.pop(0)
        if gscores[current] <= 50:
            unique_nodes.add(current)
        else:
            continue

        closed_set.add(current)

        for step in STEPS:
            neighbor = current + step
            if neighbor.x < 0 or neighbor.y < 0:
                continue
            if neighbor.is_wall(fave):
                continue
            if neighbor in closed_set:
                continue

            gscore = gscores[current] + 1
            if neighbor not in open_set:
                open_set.append(neighbor)
            elif gscore >= gscores[neighbor]:
                continue

            gscores[neighbor] = gscore
    return len(unique_nodes)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("Part 1: {}".format(navigate(1, 1, 31, 39, FAVE)))
    print("Part 2: {}".format(explore(1, 1, FAVE)))
