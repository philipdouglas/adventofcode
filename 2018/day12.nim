import deques
import sequtils
import strformat
import strutils
import sugar
import tables
from unittest import check

import aoc

var inputRules = input(day=12, year=2018).split("\n")
let inputInitial = inputRules[0].split(":")[1].strip()
inputRules.delete(0)
inputRules.delete(0)


proc grow(initial: string, inirules: seq[string], gens: int64): int64 =
    var
        pots = initTable[int, bool]()
        rules = inirules.map((rule) => rule.split(" => "))
                        .map(proc (pair: seq[string]): tuple[a: seq[bool], b: bool] =
                            result.a = pair[0].mapIt(it == '#')
                            result.b = pair[1][0] == '#')
                        .toTable()
    for i, pot in initial.mapIt(it == '#'): pots[i] = pot

    for gen in 1..min(120, gens):
        if gen mod 10000 == 0:
            echo gen
        let
            lowPot = toSeq(pots.keys).min
            highPot = toSeq(pots.keys).max
        var
            frame = initDeque[bool]()
            newPots = initTable[int, bool]()
        for _ in 1..5: frame.addLast(false)
        for i in (lowPot - 2)..(highPot + 2):
            frame.popFirst()
            frame.addLast(pots.getOrDefault(i + 2, false))
            newPots[i] = rules.getOrDefault(toSeq(frame.items), false)
        pots = newPots

    for pot in pots.keys:
        if pots[pot]:
            result += pot

    if gens > 120:
       result += (gens - 120) * 22


let
    testInitial = "#..#.#..##......###...###"
    testRules = @[
        "...## => #",
        "..#.. => #",
        ".#... => #",
        ".#.#. => #",
        ".#.## => #",
        ".##.. => #",
        ".#### => #",
        "#.#.# => #",
        "#.### => #",
        "##.#. => #",
        "##.## => #",
        "###.. => #",
        "###.# => #",
        "####. => #",
    ]
check:
    testInitial.grow(testRules, 20) == 325

echo &"Part 1: {inputInitial.grow(inputRules, 20)}"
echo &"Part 2: {inputInitial.grow(inputRules, 50000000000)}"
