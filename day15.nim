import algorithm
import math
import queues
import sequtils
import sets
import strformat
import strutils
import sugar
import tables
from unittest import check

import aoc
import coord

let input = input(day=15, year=2018).split("\n")

type
    Class = enum elf, goblin
    Unit = ref object
        attack: int
        hp: int
        class: Class
        position: Coord
    UnitTable = Table[Coord, Unit]


template `[]`(map: seq[string], coord: Coord): char =
    map[coord.y][coord.x]


proc contains(map: seq[string], coord: Coord): bool =
    coord.y >= 0 and coord.y < map.len and coord.x >= 0 and coord.x < map[0].len


proc `$`(unit: Unit): string =
    return &"<{unit.class} HP:{unit.hp} {unit.position}>"


proc `$`(units: UnitTable): string =
    return $cast[Table[Coord, Unit]](units)


proc cmp(a, b: Unit): int =
    result = cmp(a.hp, b.hp)
    if result == 0:
        result = cmp(a.position, b.position)


template pointsNear(pos: Coord): seq[Coord] =
    @[pos.up, pos.left, pos.right, pos.down]


proc isEmpty(pos: Coord, map: seq[string], units: UnitTable): bool =
    return pos in map and map[pos] != '#' and pos notin units


proc initUnit(class: Class, pos: Coord, attack: int = 3): Unit =
    new(result)
    result.attack = attack
    result.hp = 200
    result.class = class
    result.position = pos


proc initElf(pos: Coord, attack: int): Unit =
    return initUnit(elf, pos, attack)


proc initGoblin(pos: Coord): Unit =
    return initUnit(goblin, pos)


proc pathfind(start: Coord, targets: HashSet[Coord], map: seq[string], units: UnitTable): Coord =
    var
        open = initQueue[Coord]()
        shortest = -1
        depths = initTable[Coord, tuple[parent: Coord, depth: int]]()
        closestTargets: seq[Coord]
    open.enqueue(start)
    depths[start] = (start, 0)
    while open.len > 0:
        let
            current = open.dequeue()
            currentDepth = depths[current].depth
        if shortest > -1 and currentDepth > shortest:
            continue
        if current in targets:
            shortest = currentDepth
            # echo &"Close: {current} ({currentDepth})"
            closestTargets.add(current)
            continue
        for child in current.pointsNear:
            if child notin depths and child.isEmpty(map, units):
                depths[child] = (current, currentDepth + 1)
                open.enqueue(child)
    # echo closestTargets
    # echo depths
    if closestTargets.len == 0:
        return [-1, -1]
    let chosen = closestTargets.sorted(cmp)[0]
    # echo chosen
    var curr = chosen
    while depths[curr].depth != 1:
        curr = depths[curr].parent
    return curr


proc parseMap(map: seq[string], attack: int = 3): UnitTable =
    result = initTable[Coord, Unit]()
    for y in 0..<map.len:
    # for y, row in map:
        for x in 0..<map[0].len:
        # for x, square in row:
            let pos = [x, y]
            case map[pos]:
                of 'G': result[pos] = initGoblin(pos)
                of 'E': result[pos] = initElf(pos, attack)
                else: continue


proc outcome(map: seq[string]): int =
    var units = parseMap(map)
    while true:
        for unit in toSeq(units.values).sorted((a, b) => cmp(a.position, b.position)):
            # echo &"\nTurn: {unit}"
            if unit.hp <= 0:
                continue

            let moveTargets = toSeq(units.values).filterIt(it.class != unit.class)
            # echo &"moveTargets: {moveTargets}"
            if moveTargets.len == 0:
                # echo toSeq(units.values).sorted((a, b) => cmp(a.position, b.position))
                let hp = sum(toSeq(units.values).mapIt(it.hp))
                # echo &"{hp} * {result} = {hp * result}"
                return result * hp

            var targetSpaces = moveTargets
                .mapIt(it.position.pointsNear())
                .concat()
                .filterIt(it == unit.position or it.isEmpty(map, units))
                .sorted(cmp)
                .toSet()
            # echo &"targetSpaces: {targetSpaces}"
            if targetSpaces.len != 0 and unit.position notin targetSpaces:
                # Move
                let newPos = pathfind(unit.position, targetSpaces, map, units)
                # echo &"Move to: {newPos}"
                if newPos != [-1, -1]:
                    units.del(unit.position)
                    unit.position = newPos
                    units[unit.position] = unit
            # Attack
            var attackTargets = unit.position.pointsNear
                .filterIt(it in units)
                .mapIt(units[it])
            attackTargets = attackTargets.filterIt(it.class != unit.class)
            attackTargets.sort(cmp)
            if attackTargets.len > 0:
                # echo &"Attack targets: {attackTargets}"
                let attackTarget = attackTargets[0]
                attackTarget.hp -= unit.attack
                if attackTarget.hp <= 0:
                    units.del(attackTarget.position)
                # echo &"Attacked: {attackTarget}"
        result.inc
        # pause($units)


proc outcome2(map: seq[string], attack: int): int =
    var
        units = parseMap(map, attack)
        elves = toSeq(units.values).filterIt(it.class == elf)
    while true:
        for unit in toSeq(units.values).sorted((a, b) => cmp(a.position, b.position)):
            # echo &"\nTurn: {unit}"
            if unit.hp <= 0:
                continue

            let moveTargets = toSeq(units.values).filterIt(it.class != unit.class)
            # echo &"moveTargets: {moveTargets}"
            if moveTargets.len == 0:
                if elves.len == elves.filterIt(it.hp > 0).len:
                    let hp = sum(toSeq(units.values).mapIt(it.hp))
                    return result * hp
                else:
                    return -1


            var targetSpaces = moveTargets
                .mapIt(it.position.pointsNear())
                .concat()
                .filterIt(it == unit.position or it.isEmpty(map, units))
                .sorted(cmp)
                .toSet()
            # echo &"targetSpaces: {targetSpaces}"
            if targetSpaces.len != 0 and unit.position notin targetSpaces:
                # Move
                let newPos = pathfind(unit.position, targetSpaces, map, units)
                # echo &"Move to: {newPos}"
                if newPos != [-1, -1]:
                    units.del(unit.position)
                    unit.position = newPos
                    units[unit.position] = unit
            # Attack
            var attackTargets = unit.position.pointsNear
                .filterIt(it in units)
                .mapIt(units[it])
            attackTargets = attackTargets.filterIt(it.class != unit.class)
            attackTargets.sort(cmp)
            if attackTargets.len > 0:
                # echo &"Attack targets: {attackTargets}"
                let attackTarget = attackTargets[0]
                attackTarget.hp -= unit.attack
                if attackTarget.hp <= 0:
                    units.del(attackTarget.position)
                # echo &"Attacked: {attackTarget}"
        result.inc
        # pause($units)

proc part2(map: seq[string]): int =
    var attack = 4
    while true:
        result = map.outcome2(attack)
        if result != -1:
            return
        attack.inc


template moveTestTargets(units: UnitTable, map: seq[string], targetClass: Class): HashSet[Coord] =
    toSeq(units.values)
        .filterIt(it.class == targetClass)
        .mapIt(it.position.pointsNear)
        .concat()
        .filterIt(it.isEmpty(map, units))
        .sorted(cmp)
        .toSet()

# Minimal movement test from: https://www.reddit.com/r/adventofcode/comments/a6dp5v/2018_day_15_part1_cant_get_the_right_answer/ebtzw32/
let
    moveTest1 = @[
        "######",
        "#.G..#",
        "#...E#",
        "#E...#",
        "######",
    ]
    moveTestUnits1 = parseMap(moveTest1)
    moveTestTargets1 = moveTestTargets(moveTestUnits1, moveTest1, elf)
    moveTest2 = @[
        ".G...#.#",
        "....GGE.",
        ".......#",
        "........",
        "....E...",
        "...EGE.#",
        "E.......",
        "........",
        "E..E....",
        ".E....##",
    ]
    moveTestUnits2 = parseMap(moveTest2)
    moveTestTargets2 = moveTestTargets(moveTestUnits2, moveTest2, elf)
    moveTest3 = @[
        "#G#G..#",
        "#..#..#",
        "#.G.#G#",
        "#...E.#",
        "#######",
    ]
    moveTestUnits3 = parseMap(moveTest3)
    moveTestTargets3 = moveTestTargets(moveTestUnits3, moveTest3, goblin)
    moveTest4 = @[
        "#######",
        "#.E..G#",
        "#.#####",
        "#G#####",
        "#######",
    ]
    moveTestUnits4 = parseMap(moveTest4)
    moveTestTargets4 = moveTestTargets(moveTestUnits4, moveTest4, goblin)
check:
    pathfind([2, 1], moveTestTargets1, moveTest1, moveTestUnits1) == [3, 1]
    pathfind([1, 0], moveTestTargets2, moveTest2, moveTestUnits2) == [2, 0]
    pathfind([5, 1], moveTestTargets2, moveTest2, moveTestUnits2) == [5, 2]
    pathfind([4, 3], moveTestTargets3, moveTest3, moveTestUnits3) == [5, 3]
    pathfind([2, 1], moveTestTargets4, moveTest4, moveTestUnits4) == [3, 1]

    @[
        "#######",
        "#.G...#",
        "#...EG#",
        "#.#.#G#",
        "#..G#E#",
        "#.....#",
        "#######",
    ].outcome == 27730

    @[
        "#######",
        "#G..#E#",
        "#E#E.E#",
        "#G.##.#",
        "#...#E#",
        "#...E.#",
        "#######",
    ].outcome == 36334

    @[
        "#######",
        "#E..EG#",
        "#.#G.E#",
        "#E.##E#",
        "#G..#.#",
        "#..E#.#",
        "#######",
    ].outcome == 39514

    @[
        "#######",
        "#E.G#.#",
        "#.#G..#",
        "#G.#.G#",
        "#G..#.#",
        "#...E.#",
        "#######",
    ].outcome == 27755

    @[
        "#######",
        "#.E...#",
        "#.#..G#",
        "#.###.#",
        "#E#G#G#",
        "#...#G#",
        "#######",
    ].outcome == 28944

    @[
        "#########",
        "#G......#",
        "#.E.#...#",
        "#..##..G#",
        "#...##..#",
        "#...#...#",
        "#.G...G.#",
        "#.....G.#",
        "#########",
    ].outcome == 18740


    # Part 2
    @[
        "#######",
        "#.G...#",
        "#...EG#",
        "#.#.#G#",
        "#..G#E#",
        "#.....#",
        "#######",
    ].part2 == 4988

    @[
        "#######",
        "#E..EG#",
        "#.#G.E#",
        "#E.##E#",
        "#G..#.#",
        "#..E#.#",
        "#######",
    ].part2 == 31284

    @[
        "#######",
        "#E.G#.#",
        "#.#G..#",
        "#G.#.G#",
        "#G..#.#",
        "#...E.#",
        "#######",
    ].part2 == 3478

    @[
        "#######",
        "#.E...#",
        "#.#..G#",
        "#.###.#",
        "#E#G#G#",
        "#...#G#",
        "#######",
    ].part2 == 6474

    @[
        "#########",
        "#G......#",
        "#.E.#...#",
        "#..##..G#",
        "#...##..#",
        "#...#...#",
        "#.G...G.#",
        "#.....G.#",
        "#########",
    ].part2 == 1140

echo &"Part 1: {input.outcome()}"
echo &"Part 2: {input.part2()}"
