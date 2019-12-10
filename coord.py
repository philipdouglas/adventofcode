"""
2019 refactor of my coord library from 2016
"""
from dataclasses import dataclass
from math import atan2, degrees, acos, sqrt


@dataclass(order=False, repr=False, frozen=True)
class Coord:
    """
    >>> Coord(1, 1) == Coord(1, 1)
    True
    >>> Coord(1, 0) == Coord(-1, 0)
    False
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
    x: int = 0
    y: int = 0

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

    def __sub__(self, other):
        return self.__class__(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        """
        >>> c1 = Coord(1, 4)
        >>> c1 * 3
        (3, 12)
        """
        return self.__class__(self.x * other, self.y * other)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.x < other.x and self.y < other.y

    def __str__(self):
        """
        >>> Coord(0, 0)
        (0, 0)
        >>> Coord(1, 4)
        (1, 4)
        """
        return f'({self.x}, {self.y})'

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

    def up(self):
        return self.__class__(self.x, self.y + 1)

    def down(self):
        return self.__class__(self.x, self.y - 1)

    def left(self):
        return self.__class__(self.x - 1, self.y)

    def right(self):
        return self.__class__(self.x + 1, self.y)

    def manhatten_dist(self, start=None):
        """
        >>> c = Coord(2, 3)
        >>> c.manhatten_dist()
        5
        >>> c = Coord(0, -2)
        >>> c.manhatten_dist()
        2
        >>> c = Coord(0, -2)
        >>> c.manhatten_dist(Coord(1, 2))
        5
        """
        start = start or Coord(0, 0)
        return abs(self.x - start.x) + abs(self.y - start.y)

    @property
    def angle(self):
        return atan2(self.y, self.x)

    def dotproduct(self, other):
        return self.x * other.x + self.y * other.y

    def vector_length(self):
        return sqrt(self.dotproduct(self))

    def angle_to(self, other=None):
        """
        >>> Coord(1, 0).angle_to()
        90
        >>> Coord(-1, 0).angle_to()
        270
        >>> Coord(0, -1).angle_to()
        180
        """
        if other is None:
            other = Coord(0, 1)
        return int(degrees(
            acos(self.dotproduct(other) / self.vector_length() * other.vector_length())))



@dataclass(order=False, repr=False, frozen=True)
class Coord3(Coord):
    z: int = 0

    def __add__(self, other):
        """
        >>> Coord3(1, 2, 3) + Coord3(-1, 2, 0)
        (0, 4, 3)
        """
        return self.__class__(self.x + other.x, self.y + other.y, self.z + other.z)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __repr__(self):
        return str(self)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
