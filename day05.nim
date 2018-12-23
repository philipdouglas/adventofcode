import sequtils
import strformat
import strutils
from unittest import check

import aoc

let input = input(day=5, year=2018)


template reactsWith(a, b: char): bool =
    ord(a) == ord(b) + 32 or ord(a) == ord(b) - 32


template react(polymer: openArray[char]): int =
    var stack: seq[char]
    for unit in polymer:
        if stack.len > 0 and stack[stack.high].reactsWith(unit):
            discard stack.pop()
        else:
            stack.add(unit)
    stack.len


proc improve(polymer: string): int =
    result = polymer.len
    for ch in 'a'..'z':
        let CH = ch.toUpperAscii
        result = min(result, polymer.filterIt(it != ch and it != CH).react())


check:
    "aA".react() == 0
    "abBA".react() == 0
    "abAB".react() == 4
    "aabAAB".react() == 6
    "dabAcCaCBAcCcaDA".react() == 10

    "dabAcCaCBAcCcaDA".improve() == 4

echo &"Part 1: {input.react()}"
echo &"Part 2: {input.improve()}"
