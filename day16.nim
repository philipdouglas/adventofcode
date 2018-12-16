import sequtils
import sets
import strscans
import strformat
import strutils
import sugar
from unittest import check

import aoc

type Opcode = enum
    addr, addi, mulr, muli, banr, bani, borr, bori,
    setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr


proc parseSample(line: string): array[4, int] =
    var one, two, three, four: int
    discard line.scanf("[$i, $i, $i, $i]", one, two, three, four)
    return [one, two, three, four]


proc parseOp(line: string): array[4, int] =
    var one, two, three, four: int
    discard line.scanf("$i $i $i $i", one, two, three, four)
    return [one, two, three, four]


let
    input = input(day=16, year=2018).split("\n\n\n\n")
    samples = input[0].split("\n\n").map((group) => group.split("\n"))
    program = input[1].split("\n").map(parseOp)


template opgen(leta, letb, operation: untyped): untyped =
    let
        a {.inject.} = leta
        b {.inject.} = letb
    result[command[3]] = operation


template oprr(operation: untyped): untyped =
    opgen(registers[command[1]], registers[command[2]], operation)


template opri(operation: untyped): untyped =
    opgen(registers[command[1]], command[2], operation)


template opir(operation: untyped): untyped =
    opgen(command[1], registers[command[2]], operation)


proc execute(opcode: Opcode, command: array[4, int],
             registers: array[4, int]): array[4, int] =
    result = registers
    case opcode:
        of addr: oprr(a + b)
        of addi: opri(a + b)
        of mulr: oprr(a * b)
        of muli: opri(a * b)
        of banr: oprr(a and b)
        of bani: opri(a and b)
        of borr: oprr(a or b)
        of bori: opri(a or b)
        of setr: oprr(a)
        of seti: opir(a)
        of gtir: opir(if a > b: 1 else: 0)
        of gtri: opri(if a > b: 1 else: 0)
        of gtrr: oprr(if a > b: 1 else: 0)
        of eqir: opir(if a == b: 1 else: 0)
        of eqri: opri(if a == b: 1 else: 0)
        of eqrr: oprr(if a == b: 1 else: 0)


proc analyze(sample: seq[string]): tuple[code: int, matches: seq[Opcode]] =
    let
        before = parseSample(sample[0][8..^1])
        op = parseOp(sample[1])
        after = parseSample(sample[2][8..^1])
    result.code = op[0]
    for opcode in Opcode.low..Opcode.high:
        if execute(opcode, op, before) == after:
            result.matches.add(opcode)


proc part1(samples: seq[seq[string]]): int =
    for sample in samples:
        if sample.analyze.matches.len >= 3:
            result.inc


proc analyzeSamples(samples: seq[seq[string]]): array[0..15, Opcode] =
    var
        ops = repeat(toSeq(Opcode.low..Opcode.high).toSet, 16)
        unresolved = toSeq(0..15).toSet()
    for sample in samples:
        let (code, matches) = analyze(sample)
        ops[code] = ops[code].intersection(matches.toSet())
    while unresolved.len > 0:
        for opid in unresolved.filterIt(ops[it].len == 1):
            unresolved.excl(opid)
            for otherid in unresolved:
                ops[otherid].excl(ops[opid])
            result[opid] = ops[opid].pop()


proc part2(samples: seq[seq[string]], program: seq[array[4, int]]): int =
    let opmap = analyzeSamples(samples)
    var registers: array[4, int]
    for command in program:
        registers = execute(opmap[command[0]], command, registers)
    return registers[0]


check:
    @[
        "Before: [3, 2, 1, 1]",
        "9 2 1 2",
        "After:  [3, 2, 2, 1]",
    ].analyze == (9, @[addi, mulr, seti])


echo &"Part 1: {samples.part1()}"
echo &"Part 2: {samples.part2(program)}"
