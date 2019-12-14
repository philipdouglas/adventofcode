from collections import Counter

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
    """
    >>> asteroids = parse_asteroids(["#.........", "...#......", "...#..#...", ".####....#", "..#.#.#...", ".....#....", "..###.#.##", ".......#..", "....#...#.", "...#..#..#"])
    >>> test_asteroid(Coord(9, 9), asteroids)
    6
    """
    count = 0
    for other in others:
        if other != asteroid and blocked_by(asteroid, other):
            count += 1
    # print(f"{asteroid + Coord(8, 3)}: {count}")
    return count


def part1(asteroids):
    """
    >>> part1([".#..#", ".....", "#####", "....#", "...##"])
    8
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
    print(results.most_common(1)[0])
    return results.most_common(1)[0][1]


def part2(asteroids, target=200, station=Coord(11, 13)):
    """
    >>> part2([".#....#####...#..", "##...##.#####..##", "##...#...#.#####.", "..#.....X...###..", "..#.#.....#....##"], 2, station=Coord(8, 3))
    900
    """
    asteroids = parse_asteroids(asteroids)
    destroyed = asteroids = [other - station for other in asteroids if other != station]
    destroyed = sorted(destroyed, key=lambda asteroid: (test_asteroid(asteroid, asteroids), (360 - asteroid.angle_to(Coord(0, -1))) % 360))
    print([(c + station, 360 - c.angle_to(Coord(0, -1)), ) for c in destroyed])
    result = destroyed[target - 1] + station
    return result.x * 100 + result.y


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2019, day=10)
    asteroids = puzzle.input_data.split('\n')
    print(asteroids)
    # puzzle.answer_a = inspect(part1(asteroids), prefix='Part 1: ')
    puzzle.answer_b = inspect(part2(asteroids, target=200), prefix='Part 2: ')
