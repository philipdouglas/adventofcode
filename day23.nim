import algorithm
import math
import sequtils
import strformat
import strscans
import strutils
import sugar
import tables
from unittest import check

import itertools

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
    for bot in nanobots:
        if bot.pos.manhattenDist(biggest.pos) <= biggest.r:
            result.inc


iterator countup(a, b: Coord3, step: int): Coord3 =
    for x in countup(a.x, b.x, step):
        for y in countup(a.y, b.y, step):
            for z in countup(a.z, b.z, step):
                yield [x, y, z]


proc optimalPosition(nanobots: seq[Nanobot]): int =
    # var 
    #     smallest = -1
    #     smallestTrio: seq[Nanobot]
    # for trio in combinations(nanobots, 3):
    #     let perimeter = manhattenDist(trio[0].pos, trio[1].pos) + manhattenDist(trio[1].pos, trio[2].pos) + manhattenDist(trio[0].pos, trio[2].pos)
    #     if perimeter < smallest or smallest == -1:
    #         smallest = perimeter
    #         smallestTrio = trio
    # var strengths = initTable[Coord3, int]()
    # var allcoords = smallestTrio.mapIt(it.pos)
    # for pos in min(allcoords)..max(allcoords):
    #     strengths[pos] = 0
    #     for bot in nanobots:
    #         if bot.pos.manhattenDist(pos) <= bot.r:
    #             strengths[pos].inc
    # let biggest = toSeq(strengths.values).max
    # let ties = toSeq(strengths.keys).filterIt(strengths[it] == biggest)
    # return ties.sortedByIt(it.manhattenDist())[0].manhattenDist()
    let allcoords = nanobots.mapIt(it.pos)
    var 
        fromPoint = min(allcoords)
        toPoint = max(allcoords)
        sampleSize = nextPowerOfTwo(toPoint.x - fromPoint.x)
        bestResult = -1
        best: Coord3
        target = 0
    while true:
        for point in countup(fromPoint, toPoint, sampleSize):
            var count = 0
            for bot in nanobots:
                if ((bot.pos.manhattenDist(point) - bot.r) / sampleSize) <= 0:
                    count.inc
            if count > target:
                target = count
                bestResult = point.manhattenDist()
                best = point
            elif count == target and point.manhattenDist < bestResult:
                bestResult = point.manhattenDist()
                best = point
        if sampleSize == 1:
            return bestResult
        else:
            let modifier = [sampleSize, sampleSize, sampleSize]
            fromPoint = best - modifier
            toPoint = best + modifier
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