import algorithm
import math
import re
import sequtils
import strformat
import strutils
import tables
from unittest import check

import aoc

let pattern = re"(\d+) units each with (\d+) hit points (?:\(([a-z, ;]+)?\))? ?with an attack that does (\d+) ([a-z]+) damage at initiative (\d+)"

type
    Type = enum fire, cold, slashing, bludgeoning, radiation
    Side = enum immune, infection, tie
    Group = ref object
        units: int
        hp: int
        weaknesses: seq[Type]
        immunities: seq[Type]
        attackDamage: int
        attackType: Type
        initiative: int
        side: Side
        id: int
let types = toSeq(Type.low..Type.high).mapIt($it)


template effectivePower(group: Group): int =
    max(group.units, 0) * group.attackDamage


proc clone(groups: seq[Group]): seq[Group] =
    deepCopy(result, groups)


proc parse(line: string, side: Side): Group =
    var matches: array[6, string]
    discard line.find(pattern, matches)
    var weaknesses, immunities: seq[Type]
    for chunk in matches[2].split("; "):
        if chunk.startsWith("weak to"):
            for attackType in chunk[8..^1].split(", "):
                weaknesses.add(types.find(attackType).Type)
        elif chunk.startsWith("immune to"):
            for attackType in chunk[10..^1].split(", "):
                immunities.add(types.find(attackType).Type)
    new(result)
    result.units = parseInt(matches[0])
    result.hp = parseInt(matches[1])
    result.weaknesses = weaknesses
    result.immunities = immunities
    result.attackDamage = parseInt(matches[3])
    result.attackType = types.find(matches[4]).Type
    result.initiative = parseInt(matches[5])
    result.side = side
    result.id = 0


proc `$`(group: Group): string =
    let
        weak = group.weaknesses.join("|")
        immun = group.immunities.join("|")
    return &"{group.side} Group {group.id} Units:{group.units} HP:{group.hp} Atk:{group.attackDamage}[{group.attackType}] Ini:{group.initiative} Weak:{weak} Imm:{immun}"


proc parse(lines: seq[string]): tuple[immuneSys: seq[Group], infection: seq[Group]] =
    var mode = 0
    for line in lines:
        if line in @["", "Immune System:"]:
            continue
        elif line == "Infection:":
            mode = 1
        elif mode == 0:
            result.immuneSys.add(line.parse(immune))
        elif mode == 1:
            result.infection.add(line.parse(infection))


let
    (inputImmune, inputInfection) = input(day=24, year=2018).split("\n").parse()
    (testInputImmune, testInputInfection) = @[
        "Immune System:",
        "17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2",
        "989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3",
        "",
        "Infection:",
        "801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1",
        "4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4",
    ].parse

proc cmp(a, b: Group): int =
    result = cmp(a.effectivePower, b.effectivePower)
    if result == 0:
        result = cmp(a.initiative, b.initiative)


proc calcDamage(a, b: Group): int =
    result = a.effectivePower
    if a.attackType in b.immunities:
        return 0
    elif a.attackType in b.weaknesses:
        result *= 2


proc pickTarget(attacker: Group, targets: seq[Group], picked: var OrderedTable[int, int]) =
    var
        mostDamage = 0
        bestTarget: Group
    for target in targets:
        if target.id in picked: continue
        let damage = attacker.calcDamage(target)
        if damage > mostDamage:
            mostDamage = damage
            bestTarget = target
        elif damage == mostDamage and damage != 0:
            if bestTarget.effectivePower < target.effectivePower:
                bestTarget = target
            elif bestTarget.effectivePower == target.effectivePower and bestTarget.initiative < target.initiative:
                bestTarget = target
    if mostDamage > 0:
        picked[bestTarget.id] = attacker.id


proc combat(immuneSys: seq[Group], infections: seq[Group], boost: int = 0,
            debug: bool = false): tuple[survivors: int, winners: Side] =
    var
        immuneSys = clone(immuneSys)
        infections = clone(infections)
        lookupTable = concat(immuneSys, infections)
    for group in immuneSys:
        group.attackDamage += boost
    for i, group in lookupTable.mpairs:
        group.id = i
    if debug: pause(&"{immuneSys}\n{infections}")
    while true:
        var picks = initOrderedTable[int, int]()
        for group in concat(immuneSys, infections).sorted(cmp).reversed():
            if group.side == immune:
                pickTarget(group, infections, picks)
            else:
                pickTarget(group, immuneSys, picks)
        let attacks = toSeq(picks.pairs).mapIt(
            (a: lookupTable[it[1]], v: lookupTable[it[0]]))
        var stalemate = true
        for attack in attacks.sortedByIt(it.a.initiative).reversed:
            var victim = attack.v
            let
                attacker = attack.a
                damage = attacker.calcDamage(victim)
                kills = min(damage div victim.hp, victim.units)
            if debug: echo &"Group {attacker.id} kills {kills} ({damage} / {victim.hp}) from Group {victim.id}"
            victim.units -= kills
            if kills > 0:
                stalemate = false
        if stalemate:
            return (concat(immuneSys, infections).mapIt(it.units).sum(), tie)
        immuneSys = immuneSys.filterIt(it.units > 0)
        infections = infections.filterIt(it.units > 0)
        if debug: pause(&"{immuneSys}\n{infections}")
        if immuneSys.len == 0:
            return (infections.mapIt(it.units).sum(), infection)
        if infections.len == 0:
            return (immuneSys.mapIt(it.units).sum(), immune)


proc optimise(immuneSys: seq[Group], infections: seq[Group], debug: bool = false): int =
    var
        winner = infection
        boost = 0
    while winner != immune:
        boost.inc
        (result, winner) = combat(immuneSys, infections, boost)
        if debug: pause(&"{boost}: {winner} {result}")


check:
    combat(testInputImmune, testInputInfection, debug=false) == (5216, infection)
    combat(testInputImmune, testInputInfection, 1570, debug=false) == (51, immune)


let part1 = combat(inputImmune, inputInfection)
echo &"Part 1: {part1.survivors}"
echo &"Part 2: {optimise(inputImmune, inputInfection, false)}"
