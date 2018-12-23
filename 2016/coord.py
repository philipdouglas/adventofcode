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
        return self.__class__(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        """
        >>> Coord(1, 1) == Coord(1, 1)
        True
        >>> Coord(1, 0) == Coord(-1, 0)
        False
        """
        return self.x == other.x and self.y == other.y

    def __mul__(self, other):
        """
        >>> c1 = Coord(1, 4)
        >>> c1 * 3
        (3, 12)
        """
        return self.__class__(self.x * other, self.y * other)

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

    def rotate_left(self):
        """
        >>> c = Coord(0, 1)
        >>> c.rotate_left()
        (-1, 0)
        """
        return self.__class__(-self.y, self.x)

    def rotate_right(self):
        """
        >>> c = Coord(0, 1)
        >>> c.rotate_right()
        (1, 0)
        """
        return self.__class__(self.y, -self.x)


class BlockCoord(Coord):
    def distance_blocks(self, start=Coord(0, 0)):
        """
        >>> c = BlockCoord(2, 3)
        >>> c.distance_blocks()
        5
        >>> c = BlockCoord(0, -2)
        >>> c.distance_blocks()
        2
        >>> c = BlockCoord(0, -2)
        >>> c.distance_blocks(Coord(1, 2))
        5
        """
        return abs(self.x - start.x) + abs(self.y - start.y)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
