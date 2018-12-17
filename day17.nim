import algorithm
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


proc findClay(ground: Table[Coord, Tile], start, direction: Coord): int =
    var
        curr = start + direction
    while true:
        if ground.getOrDefault(curr, dry) == clay:
            return
        if direction != [0, 1] and ground.getOrDefault(curr.down, dry) notin @[clay, wet]:
            break
        result.inc
        curr += direction
    return -1

proc spill(ground: var Table[Coord, Tile], start, direction: Coord): Coord =
    result = start + direction
    while ground.getOrDefault(result.down, dry) in @[clay, wet]:
        ground[result] = dried
        result += direction


proc `$`(tile: Tile): string =
    case tile:
        of clay: return "#"
        of dried: return "|"
        of dry: return " "
        of wet: return "~"
        else: return "!"


proc draw(ground: Table[Coord, Tile], ylim: int = -1): string =
    let allcoord = toSeq(ground.keys)
    for y in allcoord.ymin..allcoord.ymax:
        if ylim > -1 and abs(y - ylim) > 20:
            continue
        result.add("\p")
        for x in allcoord.xmin..allcoord.xmax:
            result.add($ground.getOrDefault([x, y], dry))


proc followWater(input: seq[string]): int =
    var ground = parseCoords(input)
    let
        allcoords = toSeq(ground.keys)
        ylim = allcoords.ymax
    var moving: seq[Coord] = @[[500, allcoords.ymin]]
    while moving.len > 0:
        moving.sort(cmp)
        let current = moving.pop()
        if current.y > ylim:
            continue
        if ground.getOrDefault(current, dry) in @[clay, wet]:
            continue
        let below = ground.getOrDefault(current.down, dry)
        if below == dry:
            moving.add(current.down)
            ground[current] = dried
        elif below == dried:
            ground[current] = dried
        elif below == wet or below == clay:
            let
                leftClay = ground.findClay(current, [-1, 0])
                rightClay = ground.findClay(current, [1, 0])
            if leftClay > -1 and rightClay > -1:
                ground[current] = wet
                for i in 0..leftClay:
                    ground[current - [i, 0]] = wet
                for i in 0..rightClay:
                    ground[current + [i, 0]] = wet
                moving.add(current.up)
            elif leftClay > -1:
                ground[current] = dried
                for i in 0..leftClay:
                    ground[current - [i, 0]] = dried
                moving.add(ground.spill(current, right))
            elif rightClay > -1:
                ground[current] = dried
                for i in 0..rightClay:
                    ground[current + [i, 0]] = dried
                moving.add(ground.spill(current, left))
            else:
                ground[current] = dried
                moving.add(ground.spill(current, left))
                moving.add(ground.spill(current, right))
        # echo moving
        # pause(ground.draw(current.y))
    # echo ground.draw
    return toSeq(ground.values).filterIt(it in @[wet, dried]).len


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

# echo input.parseCoords.draw
echo &"Part 1: {input.followWater()}"
