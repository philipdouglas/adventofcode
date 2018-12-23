import algorithm
import math
import sequtils
import strformat
import strutils
import sugar
from unittest import check

import aoc

const input = 286051


proc digits(number: int): seq[int] =
    if number == 0:
        return @[0]
    var tens = 1
    while tens <= number:
        result.insert((number div tens) mod 10)
        tens *= 10


proc part1(target: int): string =
    var
        recipes = @[3, 7]
        elves = [0, 1]
    while recipes.len < target + 10:
        recipes.add(elves.mapIt(recipes[it]).sum.digits)
        for i, elf in elves:
            elves[i] = (elf + 1 + recipes[elf]) mod recipes.len
    return recipes[target..<target + 10].join("")


proc part2(target: string): int =
    let target = target.mapIt(parseInt($it))
    var
        recipes = @[3, 7]
        elves = [0, 1]
    while true:
        for score in elves.mapIt(recipes[it]).sum.digits:
            recipes.add(score)
            if recipes.len >= target.len and target == recipes[^target.len..^1]:
                return recipes.len - target.len
        for i, elf in elves:
            elves[i] = (elf + 1 + recipes[elf]) mod recipes.len


check:
    1.digits == @[1]
    12.digits == @[1, 2]
    305.digits == @[3, 0, 5]

    @[1, 2] == @[3, 1, 2, 4][^3..^2]

    part1(9) == "5158916779"
    part1(5) == "0124515891"
    part1(18) == "9251071085"
    part1(2018) == "5941429882"

    part2("51589") == 9
    part2("01245") == 5
    part2("92510") == 18
    part2("59414") == 2018


echo &"Part 1: {part1(input)}"
echo &"Part 2: {part2($input)}"
