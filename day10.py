from collections import Counter
from math import radians

from aocd.models import Puzzle

from coord import Coord
from util import inspect


def blocked_by(asteroid1, asteroid2):
    """
    >>> blocked_by(Coord(1, 1), Coord(1, 1))
    True
    >>> blocked_by(Coord(1, 1), Coord(2, 2))
    False
    >>> blocked_by(Coord(2, 2), Coord(1, 1))
    True
    >>> blocked_by(Coord(2, 1), Coord(1, 1))
    False
    >>> blocked_by(Coord(1, 1), Coord(2, 1))
    False
    >>> blocked_by(Coord(2, 2), Coord(-1, -1))
    False
    >>> blocked_by(Coord(-4, -2), Coord(-2, -1))
    True
    >>> blocked_by(Coord(4, -2), Coord(-2, -1))
    False
    >>> blocked_by(Coord(4, -2), Coord(2, -1))
    True
    >>> blocked_by(Coord(0, 4), Coord(0, 2))
    True
    >>> blocked_by(Coord(0, 2), Coord(0, 4))
    False
    >>> blocked_by(Coord(0, -4), Coord(0, 2))
    False
    """
    if asteroid1 == asteroid2:
        return True
    angle = asteroid1.angle == asteroid2.angle
    direction = abs(asteroid1.x) >= abs(asteroid2.x) and abs(asteroid1.y) >= abs(asteroid2.y)
    return angle and direction


def parse_asteroids(asteroids):
    """
    >>> parse_asteroids(['.#', '#.'])
    [(1, 0), (0, 1)]
    """
    result = []
    for y, row in enumerate(asteroids):
        for x, space in enumerate(row):
            if space == '#':
                result.append(Coord(x, y))
    return result


def test_asteroid(asteroid, others):
    count = 0
    for other in others:
        if other != asteroid and blocked_by(asteroid, other):
            count += 1
    return count


def part1(asteroids):
    """
    >>> part1([".#..#", ".....", "#####", "....#", "...##"])
    ((3, 4), 8)
    """
    asteroids = parse_asteroids(asteroids)
    results = Counter()
    for asteroid in asteroids:
        relative_positions = [other - asteroid for other in asteroids if other != asteroid]
        can_see = 0
        for checking in relative_positions:
            if test_asteroid(checking, relative_positions) == 0:
                can_see += 1
        results[asteroid] = can_see
    return results.most_common(1)[0]

def part2(asteroids):
    ninety_degs = radians(90)
    asteroids = parse_asteroids(asteroids)
    station = Coord(11, 13)
    asteroids = [other - station for other in asteroids if other != station]
    asteroids.sort(key=lambda asteroid: test_asteroid(asteroid, asteroids))
    asteroids.sort(key=lambda asteroid: asteroid.angle - ninety_degs)
    result = asteroids[200]
    return result.x * 100 + result.y


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2019, day=10)
    asteroids = puzzle.input_data.split('\n')
    # puzzle.answer_a = inspect(part1(asteroids), prefix='Part 1: ')
    puzzle.answer_b = inspect(part2(asteroids), prefix='Part 2: ')
