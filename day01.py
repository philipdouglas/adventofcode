from aocd.models import Puzzle

from util import inspect


def fuel_required(mass):
    """
    >>> fuel_required(12)
    2
    >>> fuel_required(14)
    2
    >>> fuel_required(1969)
    654
    >>> fuel_required(100756)
    33583
    """
    return (mass // 3) - 2


def part1(modules):
    return sum(fuel_required(module) for module in modules)


def fuel_gen(mass):
    """
    >>> sum(list(fuel_gen(14)))
    2
    >>> sum(list(fuel_gen(1969)))
    966
    >>> sum(list(fuel_gen(100756)))
    50346
    """
    while (mass := fuel_required(mass)) > 0:
        yield mass


def part2(modules):
    return sum(sum(fuel_gen(module)) for module in modules)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2019, day=1)
    modules = [int(module) for module in puzzle.input_data.split('\n')]
    puzzle.answer_a = inspect(part1(modules), prefix='Part 1: ')
    puzzle.answer_b = inspect(part2(modules), prefix='Part 2: ')
