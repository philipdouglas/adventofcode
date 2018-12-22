import math
import sequtils
import strformat
import strutils
import sugar
from unittest import check

import aoc
import coord

const
    DEPTH = 5913
    TARGET = [8, 701]


type Area = enum rocky, wet, narrow


proc `$`(area: Area): string =
    case area:
        of rocky: return "."
        of wet: return "="
        of narrow: return "|"


proc riskLevel(target: Coord, depth: int, debug: bool = false): int =
    var levelMap: seq[seq[int]]
    for y in 0..target.y:
        levelMap.add(@[])
        for x in 0..target.x:
            let curr = [x, y]
            if debug: echo [x, y]
            var geologicIndex = 0
            if curr == [0, 0] or curr == target:
                geologicIndex = 0
            elif y == 0 and x != 0:
                geologicIndex = x * 16807
            elif x == 0 and y != 0:
                geologicIndex = y * 48271
            else:
                geologicIndex = levelMap[curr.left] * levelMap[curr.up]

            let erosionLevel = (geologicIndex + depth) mod 20183
            levelMap[^1].add(erosionLevel)
    let map = levelMap.mapIt(it.mapIt(Area(it mod 3)))

    if debug: echo map.mapIt(it.join("")).join("\n")

    return map.concat().mapIt(it.int).sum()


check:
    int(rocky) == 0
    int(wet) == 1
    int(narrow) == 2

    [10, 10].riskLevel(510, debug=false) == 114

echo &"Part 1: {TARGET.riskLevel(DEPTH)}"
