from collections import Counter
from itertools import combinations

from aocd.models import Puzzle


def part1(boxes):
    """
    >>> part1(["abcdef", "bababc", "abbcde", "abcccd", "aabcdd", "abcdee", "ababab"])
    12
    """
    twos = 0
    threes = 0
    for box in boxes:
        counts = Counter(box).values()
        if 2 in counts:
            twos += 1
        if 3 in counts:
            threes += 1
    return twos * threes


def part2(boxes):
    """
    >>> part2(["abcde", "fghij", "klmno", "pqrst", "fguij", "axcye", "wvxyz"])
    'fgij'
    """
    for box1, box2 in combinations(boxes, 2):
        shared = [char1 for char1, char2 in zip(box1, box2) if char1 == char2]
        if len(shared) == len(box1) - 1:
            return ''.join(shared)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    puzzle = Puzzle(year=2018, day=2)
    boxes = puzzle.input_data.split('\n')
    puzzle.answer_a = part1(boxes)
    puzzle.answer_b = part2(boxes)
