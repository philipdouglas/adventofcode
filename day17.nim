import sequtils
import strformat
import strscans
import strutils
import sugar
import tables
from unittest import check

import aoc
import coord

let input = input(day=17, year=2018).split("\p")

type
    Tile = enum clay, wet, dried, dry


proc parseCoords(input: seq[string]): Table[Coord, Tile] =
    result = initTable[Coord, Tile]()
    for line in input:
        if line[0] == 'x':
            var x, ylow, yhigh: int
            discard line.scanf("x=$i, y=$i..$i", x, ylow, yhigh)
            for y in ylow..yhigh:
                result[[x, y]] = clay
        elif line[0] == 'y':
            var y, xlow, xhigh: int
            discard line.scanf("y=$i, x=$i..$i", y, xlow, xhigh)
            for x in xlow..xhigh:
                result[[x, y]] = clay
    let allcoord = toSeq(result.keys)
    for coord in (allcoord.min - [1, 0])..(allcoord.max + [1, 0]):
        if coord notin result:
            result[coord] = dry


proc findClay(start, direction: Coord, ground: Table[Coord, Tile]): int =
    var curr = start + direction
    while curr in ground:
        if ground[curr] == clay:
            return
        result.inc
        curr += direction
    return -1


proc `$`(tile: Tile): string =
    case tile:
        of clay: return "#"
        of dried: return "|"
        of dry: return "."
        of wet: return "~"
        else: return "!"


proc draw(ground: Table[Coord, Tile]): string =
    let
        allcoord = toSeq(ground.keys)
    for y in allcoord.ymin..allcoord.ymax:
        result.add("\p")
        for x in allcoord.xmin..allcoord.xmax:
            result.add($ground[[x, y]])


proc followWater(input: seq[string]): int =
    var
        ground = parseCoords(input)
        moving: seq[Coord] = @[[500, 0]]
    while moving.len > 0:
        let current = moving.pop()
        if current notin ground:
            continue
        let below = ground[current.down]
        if below == dry:
            moving.add(current.down)
            ground[current] = dried
        elif below == dried:
            ground[current] = dried
        elif below == wet or below == clay:
            let
                leftClay = findClay(current, [-1, 0], ground)
                rightClay = findClay(current, [1, 0], ground)
            if leftClay > -1 and rightClay > -1:
                ground[current] = wet
                if leftClay == 1:
                    moving.add(current.up)
                if rightClay == 1:
                    moving.add(current.up)
            else:
                ground[current] = dried
            moving.add(current.left)
            moving.add(current.right)
    echo ground.draw

let testInput = @[
    "x=495, y=2..7",
    "y=7, x=495..501",
    "x=501, y=3..7",
    "x=498, y=2..4",
    "x=506, y=1..2",
    "x=498, y=10..13",
    "x=504, y=10..13",
    "y=13, x=498..504",
]
check:
    testInput.followWater() == 57

