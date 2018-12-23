import algorithm
import math
import sequtils
import strformat
import strscans
import strutils
import tables
from unittest import check

import aoc
import coord

type Nanobot = tuple[pos: Coord3, r: int]


proc parseInput(nanobots: seq[string]): seq[Nanobot] =
    for line in nanobots:
        var x, y, z, r: int
        discard line.scanf("pos=<$i,$i,$i>, r=$i", x, y, z, r)
        result.add(([x, y, z], r))


let input = input(day=23, year=2018).split("\n").parseInput()


proc strongestSignal(nanobots: seq[Nanobot]): int =
    let biggest = nanobots.sortedByIt(it.r)[^1]
    return nanobots.filterIt(it.pos.manhattenDist(biggest.pos) <= biggest.r).len


proc optimalPosition(nanobots: seq[Nanobot]): int =
    let allcoords = nanobots.mapIt(it.pos)
    var
        fromPoint = min(allcoords)
        toPoint = max(allcoords)
        sampleSize = nextPowerOfTwo(toPoint.x - fromPoint.x)
        best: Coord3
        target = 0
    while sampleSize >= 1:
        for point in countup(fromPoint, toPoint, sampleSize):
            let
                count = nanobots.filterIt(it.pos.manhattenDist(point) <= it.r).len
                newResult = point.manhattenDist()
            if count > target or (count == target and newResult < result):
                target = count
                result = newResult
                best = point

        fromPoint = best - sampleSize
        toPoint = best + sampleSize
        sampleSize = sampleSize div 2


check:
    @[
        ([0, 0, 0], 4),
        ([1, 0, 0], 1),
        ([4, 0, 0], 3),
        ([0, 2, 0], 1),
        ([0, 5, 0], 3),
        ([0, 0, 3], 1),
        ([1, 1, 1], 1),
        ([1, 1, 2], 1),
        ([1, 3, 1], 1),
    ].strongestSignal() == 7
    @[
        ([10, 12, 12], 2),
        ([12, 14, 12], 2),
        ([16, 12, 12], 4),
        ([14, 14, 14], 6),
        ([50, 50, 50], 200),
        ([10, 10, 10], 5),
    ].optimalPosition() == 36

echo &"Part 1: {input.strongestSignal()}"
echo &"Part 2: {input.optimalPosition()}"
