import math
import re
import sequtils
import strformat
import strutils
import sugar
import tables
from unittest import check

let
    input = readFile("2017/.cache/input_2017_7").strip.split('\n')
    pattern = re"([a-z]+) \((\d+)\)(?: -> ([a-z, ]+))?"

type
    Program = ref object
        name: string
        weight: int
        childrenStr: seq[string]
        children: seq[Program]


proc `$`(prog: Program): string =
    return &"{prog.name} ({prog.weight}) -> {prog.childrenStr}"


proc newProgram(name: string, weight: int, children: seq[string]): Program =
    new(result)
    result.name = name
    result.weight = weight
    result.childrenStr = children.filter((child) => child.len != 0)


proc totalWeight(node: Program): int =
    result += node.weight
    for child in node.children:
        result += child.totalWeight


proc buildTree(programs: seq[string]): Program =
    var
        programsTable = initTable[string, Program]()
        programsList: seq[Program] = @[]
    for programStr in programs:
        var matches: array[3, string]
        discard programStr.find(pattern, matches)
        let program = newProgram(matches[0], matches[1].parseInt, matches[2].split(", "))
        programsTable[matches[0]] = program
        programsList.add(program)

    for program in programsList:
        if program.childrenStr.len == 0:
            continue
        for child in program.childrenStr:
            program.children.add(programsTable[child])
            programsTable.del(child)

    for program in programsTable.values: return program


proc fix(root: Program): int =
    var
        current = root
        currentTargetWeight = 0
    while true:
        var
            childWeights = current.children.map(totalWeight)
            uniqueWeights = childWeights.deduplicate
        if uniqueWeights.len == 1:
            return currentTargetWeight - childWeights.sum
        else:
            for index, unique in uniqueWeights:
                if childWeights.count(unique) == 1:
                    current = current.children[childWeights.find(unique)]
                else:
                    currentTargetWeight = unique


let testTree = @[
        "pbga (66)",
        "xhth (57)",
        "ebii (61)",
        "havc (66)",
        "ktlj (57)",
        "fwft (72) -> ktlj, cntj, xhth",
        "qoyq (66)",
        "padx (45) -> pbga, havc, qoyq",
        "tknk (41) -> ugml, padx, fwft",
        "jptl (61)",
        "ugml (68) -> gyxo, ebii, jptl",
        "gyxo (61)",
        "cntj (57)",
    ].buildTree
check:
    testTree.name == "tknk"
    testTree.fix == 60

let root = input.buildTree
echo root
echo &"Part 1: {root.name}"
echo &"Part 2: {root.fix}"
