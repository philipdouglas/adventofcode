from math import ceil
from collections import deque

def part1(numofelves):
    """
    >>> part1(6)
    5
    >>> part1(5)
    3
    >>> part1(10)
    5
    """
    elves = list(range(1, numofelves + 1))
    while len(elves) > 1:
        odd = len(elves) % 2
        elves = elves[::2]
        if odd:
            elves = elves[1:]
    return elves[0]


def part2(numofelves):
    """
    >>> part2(6)
    3
    >>> part2(5)
    2
    """
    elves = list(range(1, numofelves + 1))
    elf_index = -1
    while len(elves) > 1:
        if len(elves) % 10000 == 0:
            print(len(elves))

        elf_index += 1
        if elf_index >= len(elves):
            elf_index = 0

        opposite = (ceil(len(elves) / 2) + elf_index) % len(elves)
        if len(elves) % 2:
            opposite -= 1
        del elves[opposite]

        if opposite < elf_index:
            elf_index -= 1
    return elves[0]



if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("Part 1: {}".format(part1(3012210)))
    print("Part 2: {}".format(part2(3012210)))
