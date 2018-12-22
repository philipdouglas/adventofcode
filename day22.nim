import algorithm
import math
import queues
import sequtils
import strformat
import strutils
import sugar
import tables
from unittest import check

import aoc
import coord

const
    DEPTH = 5913
    TARGET = [8, 701]


type
    Area = enum rocky, wet, narrow
    Tool = enum none, torch, gear
    PosTool = tuple[pos: Coord, tool: Tool]


proc `$`(area: Area): string =
    case area:
        of rocky: return "."
        of wet: return "="
        of narrow: return "|"

proc `$`(tool: Tool): string =
    case tool:
        of none: return "N"
        of torch: return "T"
        of gear: return "G"


proc generate(target: Coord, depth: int, debug: bool = false): seq[seq[Area]] =
    var levelMap: seq[seq[int]]
    let extended = target + [target.y div 5, 5]
    for y in 0..extended.y:
        levelMap.add(@[])
        for x in 0..extended.x:
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
    result = levelMap.mapIt(it.mapIt(Area(it mod 3)))
    if debug: echo result.mapIt(it.join("")).join("\n")



proc riskLevel(map: seq[seq[Area]], target: Coord, debug: bool = false): int =
    let rectangle = map[0..target.y].map((row: seq[Area]) => row[0..target.x])
    return rectangle.concat().mapIt(it.int).sum()


iterator options(map: seq[seq[Area]], curr: PosTool): PosTool =
    for pos in [curr.pos.up, curr.pos.left, curr.pos.right, curr.pos.down]:
        if pos.x < 0 or pos.y < 0 or pos.y > map.high or pos.x > map[0].high:
            continue
        for tool in Tool.low..Tool.high:
            if tool == none and (map[pos] == rocky or map[curr.pos] == rocky):
                continue
            elif tool == torch and (map[pos] == wet or map[curr.pos] == wet):
                continue
            elif tool == gear and (map[pos] == narrow or map[curr.pos] == narrow):
                continue
            yield (pos, tool)


proc rescue(map: seq[seq[Area]], target: Coord, debug: bool = false): int =
    var
        open = initQueue[PosTool]()
        cameFrom = initTable[PosTool, PosTool]()
        gScore = initTable[PosTool, int]()
        target: PosTool = (target, torch)
        shortestRoute = -1
    open.enqueue(([0, 0], torch))
    gScore[([0, 0], torch)] = 0

    while open.len > 0:
        let curr = open.dequeue()

        if curr.pos == target.pos:
            if shortestRoute == -1 or gScore[curr] < shortestRoute:
                shortestRoute = gScore[curr]
            continue

        for option in options(map, curr):
            var tentativeGScore = gScore[curr] + 1
            if option.tool != curr.tool:
                tentativeGScore += 7
            if option.pos == target.pos and option.tool != torch:
                tentativeGScore += 7

            if shortestRoute > -1 and tentativeGScore > shortestRoute:
                continue

            if option in gScore and tentativeGScore >= gScore[option]:
                continue
            open.enqueue(option)

            if debug: cameFrom[option] = curr
            gScore[option] = tentativeGScore

    if debug:
        var
            rebuild = target
            route = initTable[Coord, Tool]()
        route[[0, 0]] = torch
        while rebuild.pos != [0, 0]:
            route[rebuild.pos] = rebuild.tool
            rebuild = cameFrom[rebuild]
        var debugOut: string
        for y in 0..map.high:
            if y > 0: debugOut.add("\n")
            for x in 0..map[0].high:
                if [x, y] in route:
                    debugOut.add($route[[x, y]])
                else:
                    debugOut.add($map[[x, y]])
        echo debugOut
    return shortestRoute


let testMap = generate([10, 10], 510, debug=false)
check:
    int(rocky) == 0
    int(wet) == 1
    int(narrow) == 2

    testMap.riskLevel([10, 10], debug=false) == 114
    testMap.rescue([10, 10], debug=false) == 45

let inputMap = generate(TARGET, DEPTH)
echo &"Part 1: {inputMap.riskLevel(TARGET)}"
echo &"Part 2: {inputMap.rescue(TARGET, debug=false)}"
