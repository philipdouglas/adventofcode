from collections import Counter
import difflib
from itertools import combinations
from functools import reduce
import operator

with open('.cache/input_2018_02.txt') as infile:
    ids = infile.read().strip().split('\n')

def check(id_string):
    """
    >>> check("abcdef")
    (0, 0)
    >>> check("bababc")
    (1, 1)
    >>> check("abbcde")
    (1, 0)
    >>> check("abcccd")
    (0, 1)
    >>> check("aabcdd")
    (1, 0)
    >>> check("abcdee")
    (1, 0)
    >>> check("ababab")
    (0, 1)
    """
    two, three = False, False
    for count in Counter(id_string).values():
        if count == 2:
            two = True
        elif count == 3:
            three = True
    return (1 if two else 0, 1 if three else 0)

def checksum(ids):
    """
    >>> checksum(["abcdef", "bababc", "abbcde", "abcccd", "aabcdd", "abcdee", "ababab"])
    12
    """
    return operator.mul(*reduce(
        lambda a, b: (a[0] + b[0], a[1] + b[1]),
        [check(id_string) for id_string in ids]))


def part2(ids):
    """
    >>> part2(["abcde", "fghij", "klmno", "pqrst", "fguij", "axcye", "wvxyz"])
    'fgij'
    """
    for a, b in combinations(ids, 2):
        diffchar = None
        for achar, bchar in zip(a, b):
            if achar != bchar:
                if diffchar is not None:
                    break
                diffchar = achar
        else:
            return a.replace(diff, '')


import doctest
doctest.testmod()
print(f"Part 1: {checksum(ids)}")
print(f"Part 2: {part2(ids)}")
