import algorithm
import sequtils
import sets
import strformat
import strscans
import strutils
import sugar
import tables
from unittest import check
import rdstdin

import aoc

let input = input(day=7, year=2018).split("\n")
type Result = tuple[order: string, time: int]


proc build(stepStrs: seq[string], workers: int = 5, baseTime: int = 60): Result =
    var deps = initTable[char, seq[char]]()
    for stepStr in stepStrs:
        var name, dep: string
        discard stepStr.scanf(
            "Step $w must be finished before step $w can begin.", name, dep)
        deps.mgetOrPut(dep[0], @[]).add(name[0])
        discard deps.mgetOrPut(name[0], @[])

    var
        order: seq[char]
        steps = toSeq(deps.keys).toSet
    while steps.len > 0:
        for step in steps:  # Automatically alphabetical thanks to how Set stores chars
            if deps[step].filterIt(it in steps).len == 0:
                order.add(step)
                steps.excl(step)
                break
    result.order = order.join("")

    var
        workers = workers
        finishTimes = initTable[int, seq[char]]()
        inProgress = initSet[char]()
    result.time = -1
    steps = toSeq(deps.keys).toSet
    while steps.len > 0:
        result.time.inc
        for step in finishTimes.getOrDefault(result.time, @[]):
            steps.excl(step)
            workers.inc
        for step in steps - inProgress:
            if deps[step].filterIt(it in steps).len == 0:
                if workers == 0:
                    break
                workers.dec
                let stepTime = result.time + baseTime + (ord(step) - 64)
                finishTimes.mgetOrPut(stepTime, @[]).add(step)
                inProgress.incl(step)


let testInput = @[
    "Step C must be finished before step A can begin.",
    "Step C must be finished before step F can begin.",
    "Step A must be finished before step B can begin.",
    "Step A must be finished before step D can begin.",
    "Step B must be finished before step E can begin.",
    "Step D must be finished before step E can begin.",
    "Step F must be finished before step E can begin.",
]
check:
    testInput.build(2, 0) == ("CABDFE", 15)

let result = input.build()
echo &"Part 1: {result.order}"
echo &"Part 2: {result.time}"
