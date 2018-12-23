import sequtils
import strformat
import strutils
import sugar
import tables
from unittest import check

import aoc
import coord

let input = input(day=6, year=2018).split("\n").map(parseCoord)


proc findLargestFiniteArea(coords: seq[Coord]): int =
    let
        xbounds = [coords.xmin, coords.xmax]
        ybounds = [coords.ymin, coords.ymax]
    var areas = coords.mapIt((it, 0)).toTable
    for loc in min(coords)..max(coords):
        let
            distances = coords.mapIt(manhattenDist(loc, it))
            shortest = distances.min
            closest = zip(coords, distances).filterIt(it.b == shortest)
        if closest.len == 1:
            if loc.x in xbounds or loc.y in ybounds:
                areas.del(closest[0].a)
            elif closest[0].a in areas:
                areas[closest[0].a] += 1
    return toSeq(areas.values).max


proc findMiddleRegion(coords: seq[Coord], target: int): int =
    for loc in min(coords)..max(coords):
        if coords.foldl(a + loc.manhattenDist(b), 0) < target:
            result += 1


let testInput = @[[1, 1], [1, 6], [8, 3], [3, 4], [5, 5], [8, 9]]
check:
    testInput.findLargestFiniteArea() == 17
    testInput.findMiddleRegion(32) == 16

echo &"Part 1: {input.findLargestFiniteArea()}"
echo &"Part 2: {input.findMiddleRegion(10000)}"
