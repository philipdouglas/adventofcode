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



# def part2(boxes):
#     """
#     >>> part2()
#     """


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2019, day=1)
    modules = map(int, puzzle.input_data.split('\n'))
    puzzle.answer_a = part1(modules)
    # puzzle.answer_b = part2(modules)
