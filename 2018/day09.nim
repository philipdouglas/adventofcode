import deques
import lists
import math
import rdstdin
import sequtils
import strformat
import strutils
import sugar
import tables
from unittest import check

import aoc

let
    players = 424
    lastMarble = 71482


proc rotate(circle: var Deque, steps: int = 1) =
    if steps > 0:
        for _ in 0..<steps:
            circle.addLast(circle.popFirst())
    elif steps < 0:
        for _ in 0..<(-steps):
            circle.addFirst(circle.popLast())


proc play(players, lastMarble: int): int =
    var
        nextMarble = 1
        circle = initDeque[int](lastMarble.nextPowerOfTwo)
        scores = zip(toSeq(0..<players), repeat(0, players)).toTable
    circle.addLast(0)
    while nextMarble <= lastMarble:
        if nextMarble mod 23 == 0:
            let currentPlayer = (nextMarble - 1) mod players
            scores[currentPlayer] += nextMarble
            circle.rotate(-7)
            scores[currentPlayer] += circle.popLast()
            circle.rotate()
        else:
            circle.rotate()
            circle.addLast(nextMarble)
        nextMarble.inc()
        # discard readLineFromStdin(&"[{(nextMarble - 1) mod players}] {circle}")
    return toSeq(scores.values).max


check:
    play(9, 25) == 32
    play(10, 1618) == 8317
    play(13, 7999) == 146373
    play(17, 1104) == 2764
    play(21, 6111) == 54718
    play(30, 5807) == 37305

echo &"Part 1: {play(players, lastMarble)}"
echo &"Part 2: {play(players, lastMarble * 100)}"
