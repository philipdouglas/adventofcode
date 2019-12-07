import itertools

from aocd.models import Puzzle

from computer import Computer
from util import inspect


def part1(program):
    """
    >>> part1([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0])
    43210
    >>> part1([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0])
    54321
    >>> part1([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0])
    65210
    """
    max_signal = 0
    for permutation in itertools.permutations(range(0, 5)):
        out_signal = 0
        for in_signal in permutation:
            out_signal = Computer(program).run(
                inp=[in_signal, out_signal]
            ).output
        if out_signal > max_signal:
            max_signal = out_signal
    return max_signal

# def part2(program):
#     """
#     >>> part2()
#
#     """


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2019, day=7)
    program = [int(val) for val in puzzle.input_data.split(',')]
    puzzle.answer_a = inspect(part1(program), prefix='Part 1: ')
    # puzzle.answer_b = inspect(part2(program), prefix='Part 2: ')
