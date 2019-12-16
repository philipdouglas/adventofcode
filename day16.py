from itertools import chain, cycle

from aocd.models import Puzzle

from util import inspect


BASE_PATTERN = [0, 1, 0, -1]


def part1(number, phases=100, elements=8):
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
    while phases > 0:
        phases -= 1
        next_digits = []
        for index in range(len(digits)):
            pattern = cycle(chain.from_iterable(
                [digit] * (index + 1) for digit in BASE_PATTERN))
            # skip the very first value exactly once
            next(pattern)
            result = sum(a * b for a, b in zip(digits, pattern))
            next_digits.append(int(str(result)[-1]))
        digits = next_digits
    return ''.join(map(str, digits[:elements]))


# def part2(number):
#     """
#     >>> part2()
#
#     """


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2019, day=16)
    number = puzzle.input_data
    puzzle.answer_a = inspect(part1(number), prefix='Part 1: ')
    # puzzle.answer_b = inspect(part2(number), prefix='Part 2: ')
