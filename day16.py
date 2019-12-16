from itertools import accumulate, chain, cycle
from operator import add

from aocd.models import Puzzle

from util import inspect

BASE_PATTERN = [0, 1, 0, -1]


def compute_digit(digits, multiplier):
    pattern = cycle(chain.from_iterable(
        [digit] * multiplier for digit in BASE_PATTERN))
    # skip the very first value exactly once
    next(pattern)
    result = sum(a * b for a, b in zip(digits, pattern))
    return abs(result) % 10


def part1(number, phases=100):
    """
    >>> part1('12345678', 1)
    '48226158'
    >>> part1('12345678', 2)
    '34040438'
    >>> part1('12345678', 3)
    '03415518'
    >>> part1('12345678', 4)
    '01029498'
    >>> part1('80871224585914546619083218645595')
    '24176176'
    >>> part1('19617804207202209144916044189917')
    '73745418'
    >>> part1('69317163492948606335995924319873')
    '52432133'
    """
    digits = [int(digit) for digit in number]
    for _ in range(phases):
        digits = [compute_digit(digits, index + 1) for index in range(len(digits))]
    return ''.join(map(str, digits[:8]))


def part2(number, phases=100):
    """
    >>> part2('03036732577212944063491565474664')
    '84462026'
    >>> part2('02935109699940807407585447034323')
    '78725270'
    >>> part2('03081770884921959731165446850517')
    '53553731'
    """
    offset = int(number[:7])
    digits = [int(digit) for digit in number] * 10000
    digits = reversed(digits[offset:])
    for _ in range(phases):
        digits = [value % 10 for value in accumulate(digits, func=add)]
    return ''.join(map(str, reversed(digits[-8:])))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("Tests complete!")

    puzzle = Puzzle(year=2019, day=16)
    number = puzzle.input_data
    puzzle.answer_a = inspect(part1(number), prefix='Part 1: ')
    puzzle.answer_b = inspect(part2(number), prefix='Part 2: ')
