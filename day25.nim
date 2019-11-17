import algorithm
import sequtils
import strformat
import strscans
import strutils
from unittest import check

import aoc
import coord


proc parse(line: string): Coord4 =
    var x, y, z, t: int
    discard line.scanf("$i,$i,$i,$i", x, y, z, t)
    return [x, y, z, t]


let input = input(day=25, year=2018).split("\n").map(parse)


proc constellations(stars: seq[Coord4]): int =
    var groups: seq[seq[Coord4]]
    for star in stars:
        var matches: seq[int]
        for i, group in groups:
            for other in group:
                if star.manhattenDist(other) <= 3:
                    matches.add(i)
                    break
        # if matches.len > 1:
        for match in matches[1..^1]:
            groups[matches[0]].add(groups[match])
            groups.delete(match)
        if matches.len == 0:
            groups.add(@[star])
            continue
        groups[matches[0]].add(star)
    return groups.len


check:
    @[
        [0,0,0,0],
        [3,0,0,0],
        [0,3,0,0],
        [0,0,3,0],
        [0,0,0,3],
        [0,0,0,6],
        [9,0,0,0],
        [12,0,0,0],
    ].constellations() == 2
    @[
        [-1,2,2,0],
        [0,0,2,-2],
        [0,0,0,-2],
        [-1,2,0,0],
        [-2,-2,-2,2],
        [3,0,2,-1],
        [-1,3,2,2],
        [-1,0,-1,0],
        [0,2,1,-2],
        [3,0,0,0],
    ].constellations() == 4
    @[
        [1,-1,0,1],
        [2,0,-1,0],
        [3,2,-1,0],
        [0,0,3,1],
        [0,0,-1,-1],
        [2,3,-2,0],
        [-2,2,0,0],
        [2,-2,0,-1],
        [1,-1,0,-1],
        [3,2,0,2],
    ].constellations() == 3
    @[
        [1,-1,-1,-2],
        [-2,-2,0,1],
        [0,2,1,3],
        [-2,3,-2,1],
        [0,2,3,-2],
        [-1,-1,1,-2],
        [0,-2,-1,0],
        [-2,2,3,-1],
        [1,2,2,0],
        [-1,-2,0,-2],
    ].constellations() == 8
    @[
        [0,0,0,0],
        [3,0,0,0],
        [0,3,0,0],
        [0,0,3,0],
        [0,0,0,3],
        [0,0,0,6],
        [9,0,0,0],
        [12,0,0,0],
        [6,0,0,0],
    ].constellations() == 1

echo &"Part 1: {input.constellations()}"