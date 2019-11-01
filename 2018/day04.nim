import algorithm
import math
import strformat
import strscans
import strutils
import sugar
import tables
import times
from unittest import check

import aoc
import itertools

let input = input(day=4, year=2018).split("\n")

const
    ASLEEP = -1
    WAKEUP = -2
    DATELEN = "[1970-01-01 00:00]".len
    OBSSTART = DATELEN + 1


template mins(str: string): int =
    str[15..16].parseInt


proc doit(lines: seq[string]): tuple[part1, part2: int] =
    var observations: seq[tuple[time: string, obs: int]]
    for line in lines:
        var mode: int
        if "asleep" in line:
            mode = ASLEEP
        elif "wakes" in line:
            mode = WAKEUP
        else:
            discard line[OBSSTART..line.high].scanf("Guard #$i begins shift", mode)
        observations.add((line[0..DATELEN], mode))

    observations.sort do (x, y: tuple[time: string, obs: int]) -> int:
        result = cmp(x.time, y.time)
        if result == 0:
            result = cmp(-(x.obs), -(y.obs))

    var
        guards = initTable[int, array[60, int]]()
        guardIds: seq[int]
        currentGuard: int
        asleep: int
    for event in observations:
        case event.obs:
            of ASLEEP:
                asleep = event.time.mins
            of WAKEUP:
                let wake = event.time.mins
                for minute in asleep..<wake:
                    guards[currentGuard][minute].inc
            else:
                currentGuard = event.obs
                guardIds.add(currentGuard)
                if currentGuard notin guards:
                    guards[currentGuard] = guards.getOrDefault(currentGuard)

    guardIds.sort((g1, g2) => cmp(guards[g1].sum, guards[g2].sum))

    var top: int
    for minute, days in guards[guardIds[guardIds.high]]:
        if days > top:
            top = days
            result.part1 = guardIds[guardIds.high] * minute

    for minute in 0..<60:
        for guard in guardIds:
            if guards[guard][minute] > top:
                top = guards[guard][minute]
                result.part2 = guard * minute


check:
    @[
        "[1518-11-01 00:00] Guard #10 begins shift",
        "[1518-11-01 00:05] falls asleep",
        "[1518-11-01 00:25] wakes up",
        "[1518-11-01 00:30] falls asleep",
        "[1518-11-01 00:55] wakes up",
        "[1518-11-01 23:58] Guard #99 begins shift",
        "[1518-11-02 00:40] falls asleep",
        "[1518-11-02 00:50] wakes up",
        "[1518-11-03 00:05] Guard #10 begins shift",
        "[1518-11-03 00:24] falls asleep",
        "[1518-11-03 00:29] wakes up",
        "[1518-11-04 00:02] Guard #99 begins shift",
        "[1518-11-04 00:36] falls asleep",
        "[1518-11-04 00:46] wakes up",
        "[1518-11-05 00:03] Guard #99 begins shift",
        "[1518-11-05 00:45] falls asleep",
        "[1518-11-05 00:55] wakes up",
    ].doit == (240, 4455)

let answer = input.doit
echo &"Part 1: {answer.part1}"
echo &"Part 2: {answer.part2}"
