# -1,-1   0,-1  1,-1
# -1, 0   0, 0  1, 0
# -1, 1   0, 1  1, 1


class Coord:
    def __init__(self, x=0, y=0):
        """
        >>> Coord(0, 0)
        (0, 0)
        >>> Coord(1, 4)
        (1, 4)
        """
        self.x = x
        self.y = y

    def __add__(self, other):
        """
        >>> c = Coord()
        >>> c + Coord(1, 4)
        (1, 4)
        >>> c
        (0, 0)
        >>> Coord(-4, 3) + Coord(6, 2)
        (2, 5)
        """
        return Coord(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        """
        >>> Coord(1, 1) == Coord(1, 1)
        True
        >>> Coord(1, 0) == Coord(-1, 0)
        False
        """
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        """
        >>> c1 = Coord()
        >>> c2 = Coord()
        >>> c3 = Coord(1, 0)
        >>> hash(c1) == hash(c2)
        True
        >>> hash(c1) == hash(c3)
        False
        >>> hash(c2) == hash(c3)
        False
        """
        return hash((self.x, self.y))

    def __str__(self):
        return('({}, {})'.format(self.x, self.y))

    def __repr__(self):
        return str(self)

lookup = {
    '^': Coord(0, -1),
    '<': Coord(-1, 0),
    '>': Coord(1, 0),
    'v': Coord(0, 1),
}


def follow(instructions):
    """
    >>> follow('>')
    2
    >>> follow('^>v<')
    4
    >>> follow('^v^v^v^v^v')
    2
    """
    current = Coord(0, 0)
    visited = {current}
    for instruction in instructions:
        current += lookup[instruction]
        visited.add(current)
    return len(visited)


def robofollow(instructions):
    """
    >>> robofollow('^v')
    3
    >>> robofollow('^>v<')
    3
    >>> robofollow('^v^v^v^v^v')
    11
    """
    santa = robo = Coord(0, 0)
    visited = {santa}
    iterstructions = iter(instructions)
    for instruction in iterstructions:
        santa += lookup[instruction]
        robo += lookup[next(iterstructions)]
        visited |= {santa, robo}
    return len(visited)


def adventofcode():
    with open('3.txt') as input_file:
        instructions = input_file.read().strip()

    return follow(instructions), robofollow(instructions)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print(adventofcode())
