import math
import sequtils
import intsets
import strformat
import strutils
from unittest import check

import aoc
import itertools

let input = input(day=1, year=2018).split('\n').map(parseInt)

proc part2(changes: seq[int]): int =
    var seen = initIntSet()
    for change in changes.cycle:
        if result in seen:
            return
        seen.incl(result)
        result += change

check:
    @[1, -2, 3, 1].sum == 3

    @[1, -2, 3, 1].part2 == 2
    @[+1, -1].part2 == 0
    @[+3, +3, +4, -2, -4].part2 == 10
    @[-6, +3, +8, +5, -6].part2 == 5
    @[+7, +7, -2, -7, -4].part2 == 14

echo &"Part 1: {input.sum}"
echo &"Part 1: {input.part2}"
