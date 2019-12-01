from aocd.models import Puzzle


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
    return sum(map(fuel_required, modules))


def fuel_required_extended(mass):
    """
    >>> fuel_required_extended(14)
    2
    >>> fuel_required_extended(1969)
    966
    >>> fuel_required_extended(100756)
    50346
    """
    total = 0
    while (fuel := fuel_required(mass)) >= 0:
        total += fuel
        mass = fuel
    return total


def part2(modules):
    return sum(map(fuel_required_extended, modules))


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2019, day=1)
    modules = [int(module) for module in puzzle.input_data.split('\n')]
    puzzle.answer_a = part1(modules)
    puzzle.answer_b = part2(modules)
