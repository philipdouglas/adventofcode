import algorithm
import sequtils
import strformat
import strscans
import strutils
import tables
from unittest import check

import aoc
import coord

let input = input(day=17, year=2018).split("\p")

type
    Tile = enum clay, wet, dried, dry
    Ground = Table[Coord, Tile]


template `[]`(ground: Ground, pos: Coord): Tile =
    ground.getOrDefault(pos, dry)


proc parseCoords(input: seq[string]): Ground =
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


proc findClay(ground: Ground, start, direction: Coord): int =
    var
        curr = start + direction
    while true:
        if ground[curr] == clay:
            return
        if direction != [0, 1] and ground[curr.down] notin @[clay, wet]:
            break
        result.inc
        curr += direction
    return -1


proc spill(ground: var Ground, start, direction: Coord): Coord =
    result = start
    while ground[result] != clay and ground[result.down] in @[clay, wet]:
        ground[result] = dried
        result += direction


proc fill(ground: var Ground, start: Coord, left, right: int, tile: Tile) =
    for i in -left..right:
        ground[start + [i, 0]] = tile


proc `$`(tile: Tile): string =
    case tile:
        of clay: return "#"
        of dried: return "|"
        of dry: return " "
        of wet: return "~"
        else: return "!"


proc draw(ground: Ground, ylim: int = -1): string =
    let allcoord = toSeq(ground.keys)
    for y in allcoord.ymin..allcoord.ymax:
        if ylim > -1 and abs(y - ylim) > 20:
            continue
        result.add("\p")
        for x in allcoord.xmin..allcoord.xmax:
            result.add($ground.getOrDefault([x, y], dry))


proc followWater(input: seq[string], debug: bool = false): tuple[part1: int, part2: int] =
    var ground = parseCoords(input)
    let
        allcoords = toSeq(ground.keys)
        ylim = allcoords.ymax
    var moving: seq[Coord] = @[[500, allcoords.ymin]]
    while moving.len > 0:
        if debug: moving.sort(cmp)  # Makes it easier to follow
        let current = moving.pop()
        if current.y > ylim:
            continue
        if ground[current] in @[clay, wet]:
            continue
        if ground[current.down] == dry:
            moving.add(current.down)
            ground[current] = dried
        elif ground[current.down] in @[wet, clay]:
            let
                leftClay = ground.findClay(current, left)
                rightClay = ground.findClay(current, right)
            if leftClay > -1 and rightClay > -1:
                ground.fill(current, leftClay, rightClay, wet)
                moving.add(current.up)
            else:
                moving.add(ground.spill(current, left))
                moving.add(ground.spill(current, right))
        if debug: pause(ground.draw(current.y))
    result.part1 = toSeq(ground.values).filterIt(it in @[wet, dried]).len
    result.part2 = toSeq(ground.values).filterIt(it == wet).len


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
    testInput.followWater() == (57, 29)

let answer = input.followWater(debug=false)
echo &"Part 1: {answer.part1}"
echo &"Part 2: {answer.part2}"
