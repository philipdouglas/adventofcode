import algorithm
import sequtils
import strformat
import strscans
import strutils
import sugar
from unittest import check

import aoc
import coord


proc parse(line: string): Coord4 =
    var x, y, z, t: int
    discard line.scanf("$i,$i,$i,$i", x, y, z, t)
    return [x, y, z, t]


let input = input(day=25, year=2018).split("\n").map(parse)


proc constellations(stars: seq[Coord4], debug: bool=false): int =
    var 
        stars = stars
        groups: seq[seq[Coord4]]
    while stars.len > 0:
        let star = stars.pop()
        # if groups.len == 0:
        #     groups.add(@[star])
        #     continue
        var matches: seq[int]
        for i, group in groups:
            for other in group:
                if star.manhattenDist(other) <= 3:
                    matches.add(i)
                    break
        if matches.len > 1:
            for match in matches.reversed():
                if match == matches[0]:
                    break
                groups[matches[0]].add(groups[match])
                groups.delete(match)
        elif matches.len == 0:
            groups.add(@[star])
            if debug: pause($groups)
            continue
        groups[matches[0]].add(star)
        if debug: pause($groups)
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