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


proc execute(opcode: Opcode, command: array[4, int],
             registers: array[4, int]): array[4, int] =
    let
        a = command[1]
        b = command[2]
        c = command[3]
    result = registers
    case opcode:
        of addr: result[c] = registers[a] + registers[b]
        of addi: result[c] = registers[a] + b
        of mulr: result[c] = registers[a] * registers[b]
        of muli: result[c] = registers[a] * b
        of banr: result[c] = registers[a] and registers[b]
        of bani: result[c] = registers[a] and b
        of borr: result[c] = registers[a] or registers[b]
        of bori: result[c] = registers[a] or b
        of setr: result[c] = registers[a]
        of seti: result[c] = a
        of gtir: result[c] = if a > registers[b]: 1 else: 0
        of gtri: result[c] = if registers[a] > b: 1 else: 0
        of gtrr: result[c] = if registers[a] > registers[b]: 1 else: 0
        of eqir: result[c] = if a == registers[b]: 1 else: 0
        of eqri: result[c] = if registers[a] == b: 1 else: 0
        of eqrr: result[c] = if registers[a] == registers[b]: 1 else: 0


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
