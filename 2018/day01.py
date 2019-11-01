from itertools import accumulate, cycle

with open('.cache/input_2018_01.txt') as infile:
    changes = infile.read().strip().split('\n')
changes = [int(change) for change in changes]

def part2(changes):
    """
    >>> part2([1, -2, 3, 1])
    2
    >>> part2([+1, -1])
    0
    >>> part2([+3, +3, +4, -2, -4])
    10
    >>> part2([-6, +3, +8, +5, -6])
    5
    >>> part2([+7, +7, -2, -7, -4])
    14
    """
    seen = {0}
    for freq in accumulate(cycle(changes)):
        if freq in seen:
            return freq
        seen.add(freq)

import doctest
doctest.testmod()
print(f"Part 1: {sum(changes)}")
print(f"Part 2: {part2(changes)}")
