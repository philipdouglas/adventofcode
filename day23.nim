import algorithm
import sequtils
import strformat
import strscans
import strutils
import sugar
from unittest import check

import aoc
import coord

type Signal = tuple[pos: Coord3, r: int]


proc parseInput(signals: seq[string]): seq[Signal] =
    for line in signals:
        var x, y, z, r: int
        discard line.scanf("pos=<$i,$i,$i>, r=$i", x, y, z, r)
        result.add(([x, y, z], r))


let input = input(day=23, year=2018).split("\n").parseInput()


proc locateSignal(signals: seq[Signal]): int =
    let biggest = signals.sortedByIt(it.r)[^1]
    echo biggest
    for signal in signals:
        if signal.pos.manhattenDist(biggest.pos) <= biggest.r:
            result.inc

check:
    @[
        ([0, 0, 0], 4),
        ([1, 0, 0], 1),
        ([4, 0, 0], 3),
        ([0, 2, 0], 1),
        ([0, 5, 0], 3),
        ([0, 0, 3], 1),
        ([1, 1, 1], 1),
        ([1, 1, 2], 1),
        ([1, 3, 1], 1),
    ].locateSignal() == 7

echo &"Part 1: {input.locateSignal()}"