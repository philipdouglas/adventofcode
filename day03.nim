import intsets
import math
import strscans
import strformat
import strutils
import sugar
import tables
from unittest import check

import aoc
import coord

let input = input(day=3, year=2018).split("\n")


proc only(a: IntSet): int =
    for i in a: return i


proc overlaps(claims: seq[string]): tuple[part1: int, part2: int] =
    var
        fabric = initTable[Coord, seq[int]](nextPowerOfTwo(400 * claims.len))
        ids = initIntSet()
    for claim in claims:
        var id, startx, starty, width, height: int
        discard claim.scanf("#$i @ $i,$i: $ix$i", id, startx, starty, width, height)
        ids.incl(id)
        let
            start = [startx, starty]
            finish = start + [width, height]
        for pos in start..<finish:
            fabric.mgetOrPut(pos, @[]).add(id)
            if fabric[pos].len > 1:
                if fabric[pos].len == 2:
                    result.part1.inc
                for clash in fabric[pos]:
                    ids.excl(clash)
    result.part2 = ids.only()


check:
    @["#1 @ 1,3: 4x4", "#2 @ 3,1: 4x4", "#3 @ 5,5: 2x2"].overlaps == (4, 3)
    @["#1 @ 1,3: 4x4", "#2 @ 2,1: 4x4", "#3 @ 5,5: 2x2"].overlaps == (6, 3)
    @["#1 @ 1,3: 4x4", "#2 @ 2,1: 4x4", "#3 @ 5,5: 2x2", "#4 @ 1,3: 1x1"].overlaps == (7, 3)

let answer = input.overlaps
echo &"Part 1: {answer.part1}"
echo &"Part 2: {answer.part2}"
