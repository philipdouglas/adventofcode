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
            out_signal = Computer(program, input=[in_signal, out_signal]).run()
        if out_signal > max_signal:
            max_signal = out_signal
    return max_signal


def part2(program):
    """
    >>> part2([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5])
    139629729
    >>> part2([3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10])
    18216
    """
    max_signal = 0
    for permutation in itertools.permutations(range(5, 10)):
        amplifiers = [Computer(program, input=[phase]) for phase in permutation]
        prev_output = 0
        for amp in itertools.cycle(amplifiers):
            if amp.halted:
                max_signal = max(max_signal, prev_output)
                break
            amp.add_input(prev_output)
            prev_output = amp.run()
    return max_signal


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2019, day=7)
    program = [int(val) for val in puzzle.input_data.split(',')]
    puzzle.answer_a = inspect(part1(program), prefix='Part 1: ')
    puzzle.answer_b = inspect(part2(program), prefix='Part 2: ')
