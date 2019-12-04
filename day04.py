from collections import Counter

from aocd.models import Puzzle

from util import inspect


def check(password):
    """
    >>> check(111111)
    True
    >>> check(223450)
    False
    >>> check(123789)
    False
    """
    password = str(password)
    return password == ''.join(sorted(password)) and len(password) > len(set(password))


def part1(low, high):
    return len([password for password in range(low, high + 1) if check(password)])


def check2(password):
    """
    >>> check2(112233)
    True
    >>> check2(123444)
    False
    >>> check2(111122)
    True
    """
    password = str(password)
    return password == ''.join(sorted(password)) and 2 in Counter(password).values()


def part2(low, high):
    return len([password for password in range(low, high + 1) if check2(password)])


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2019, day=4)
    low, high = [int(bound) for bound in puzzle.input_data.split('-')]
    puzzle.answer_a = inspect(part1(low, high), prefix='Part 1: ')
    puzzle.answer_b = inspect(part2(low, high), prefix='Part 2: ')
