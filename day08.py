from collections import Counter

from aocd.models import Puzzle

from util import inspect

HEIGHT = 6
WIDTH = 25
LAYER_LENGTH = HEIGHT * WIDTH


def part1(pixels):
    layers = []
    for start in range(0, len(pixels), LAYER_LENGTH):
        layers.append(pixels[start:start + LAYER_LENGTH])
    counts = sorted((Counter(layer) for layer in layers), key=lambda count: count[0])
    fewest_zeroes = counts[0]
    return fewest_zeroes[1] * fewest_zeroes[2]


# def part2(pixels):
#     """
#     >>> part2()
#
#     """


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2019, day=8)
    pixels = [int(pixel) for pixel in puzzle.input_data]
    puzzle.answer_a = inspect(part1(pixels), prefix='Part 1: ')
    # puzzle.answer_b = inspect(part2(pixels), prefix='Part 2: ')