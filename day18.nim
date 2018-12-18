import sequtils
import strformat
import strutils
import tables
from unittest import check

import aoc
import coord

let input = input(day=18, year=2018).split("\n")
type
    Tile = enum open, trees, lumberyard
    Map = Table[Coord, Tile]


template `[]`(map: Map, pos: Coord): Tile =
    map.getOrDefault(pos, open)


proc `$`(tile: Tile): string =
    case tile:
        of trees: return "|"
        of lumberyard: return "#"
        of open: return " "
        else: return "!"


proc draw(map: Map, ylim: int = -1): string =
    let (xmin, xmax, ymin, ymax) = toSeq(map.keys).minmax
    for y in ymin..ymax:
        if ylim > -1 and abs(y - ylim) > 20:
            continue
        result.add("\p")
        for x in xmin..xmax:
            result.add($map[[x, y]])


proc parseMap(map: seq[string]): Map =
    result = initTable[Coord, Tile]()
    for y, line in map:
        for x, cha in line:
            case cha:
                of '|': result[[x, y]] = trees
                of '#': result[[x, y]] = lumberyard
                else: discard


iterator adjacent(pos: Coord): Coord =
    for adj in [-1, -1]..[1, 1]:
        if adj != [0, 0]:
            yield pos + adj


proc grow(map: seq[string], mins: int, debug: bool = false): int =
    var
        map = parseMap(map)
        seen = @[map]
        elapsed, period, index: int
    let
        allcoords = toSeq(map.keys)
        start = allcoords.min
        finish = allcoords.max
    if debug: echo map.draw()
    while elapsed < mins:
        elapsed.inc
        var newMap = initTable[Coord, Tile]()
        for pos in start..finish:
            let surrounds = toSeq(pos.adjacent).mapIt(map[it]).toCountTable()
            case map[pos]:
                of open:
                    if surrounds.getOrDefault(trees, 0) >= 3:
                        newMap[pos] = trees
                of trees:
                    if surrounds.getOrDefault(lumberyard, 0) >= 3:
                        newMap[pos] = lumberyard
                    else:
                        newMap[pos] = trees
                of lumberyard:
                    if surrounds.getOrDefault(lumberyard, 0) >= 1 and surrounds.getOrDefault(trees) >= 1:
                        newMap[pos] = lumberyard
        map = newMap
        if debug: pause(map.draw)

        index = seen.find(map)
        if index > -1:
            map = seen[index + ((mins - elapsed) mod (elapsed - index))]
            break
        seen.add(map)

    let counts = toSeq(map.values).toCountTable()
    return counts[trees] * counts[lumberyard]


check:
    @[
        ".#.#...|#.",
        ".....#|##|",
        ".|..|...#.",
        "..|#.....#",
        "#.#|||#|#|",
        "...#.||...",
        ".|....|...",
        "||...#|.#|",
        "|.||||..|.",
        "...#.|..|.",
    ].grow(10) == 1147

echo &"Part 1: {input.grow(10, debug=false)}"
echo &"Part 2: {input.grow(1000000000)}"
