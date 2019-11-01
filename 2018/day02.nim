import math
import sequtils
import strformat
import strutils
import sugar
import tables
from unittest import check

import aoc
import itertools

type Result = array[2, int]

let input = input(day=2, year=2018).split("\n")


proc checkId(id: string): Result =
    var
        two = 0
        three = 0
    for key, count in id.toCountTable:
        case count:
        of 2: two = 1
        of 3: three = 1
        else: continue
    return [two, three]


proc checksum(ids: seq[string]): int =
    return ids.map(checkId).foldl([a[0] + b[0], a[1] + b[1]]).prod


proc findFabric(ids: seq[string]): string =
    for combo in combinations(ids, 2):
        if editDistance(combo[0], combo[1]) == 1:
            var chas: seq[char]
            for pair in zip(combo[0], combo[1]):
                if pair[0] == pair[1]:
                    chas.add(pair[0])
            return chas.join()


check:
    "abcdef".checkId == [0, 0]
    "bababc".checkId == [1, 1]
    "abbcde".checkId == [1, 0]
    "abcccd".checkId == [0, 1]
    "aabcdd".checkId == [1, 0]
    "abcdee".checkId == [1, 0]
    "ababab".checkId == [0, 1]

    @["abcdef", "bababc", "abbcde", "abcccd", "aabcdd", "abcdee", "ababab"].checksum == 12

    @["abcde", "fghij", "klmno", "pqrst", "fguij", "axcye", "wvxyz"].findFabric == "fgij"


echo &"Part 1: {input.checksum}"
echo &"Part 2: {input.findFabric}"
