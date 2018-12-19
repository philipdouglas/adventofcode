import sequtils
import strformat
import strscans
import strutils
import sugar
import tables
from unittest import check

import aoc

let
    input = input(day=19, year=2018).split("\n")
    inputIp = ord(input[0][4]) - ord('0')
    inputProg = input[1..^1]

type
    Opcode = enum
        addr, addi, mulr, muli, banr, bani, borr, bori,
        setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr
    Inst = tuple[op: Opcode, a, b, c: int]

let opcodeMap = toSeq(Opcode.low..Opcode.high).mapIt(($it, it)).toTable()


proc parseInstructions(program: seq[string]): seq[Inst] =
    for line in program:
        var a, b, c: int
        discard line[4..^1].scanf(" $i $i $i", a, b, c)
        result.add((opcodeMap[line[0..3]], a, b, c))


template opgen(leta, letb, operation: untyped): untyped =
    let
        a {.inject.} = leta
        b {.inject.} = letb
    result[command.c] = operation


template oprr(operation: untyped): untyped =
    opgen(registers[command.a], registers[command.b], operation)


template opri(operation: untyped): untyped =
    opgen(registers[command.a], command.b, operation)


template opir(operation: untyped): untyped =
    opgen(command.a, registers[command.b], operation)


proc execute(command: Inst, registers: array[6, int]): array[6, int] =
    result = registers
    case command.op:
        of addr: oprr(a + b)
        of addi: opri(a + b)
        of mulr: oprr(a * b)
        of muli: opri(a * b)
        of banr: oprr(a and b)
        of bani: opri(a and b)
        of borr: oprr(a or b)
        of bori: opri(a or b)
        of setr: oprr(a)
        of seti: result[command.c] = command.a
        of gtir: opir(if a > b: 1 else: 0)
        of gtri: opri(if a > b: 1 else: 0)
        of gtrr: oprr(if a > b: 1 else: 0)
        of eqir: opir(if a == b: 1 else: 0)
        of eqri: opri(if a == b: 1 else: 0)
        of eqrr: oprr(if a == b: 1 else: 0)


proc run(program: seq[string], ip: int, init0: int = 0, debug: bool = false): int =
    var
        registers: array[6, int]
        pc: int
        program = parseInstructions(program)
    registers[0] = init0
    while pc >= 0 and pc <= program.high:
        registers[ip] = pc
        let inst = program[pc]
        # if debug: pause(&"pc={pc} {registers} {inst}")
        registers = execute(inst, registers)
        if debug: pause(&"Result: {registers}")
        if registers[2] > 10000000 and registers[5] < 100000:
            registers[5] = registers[2] - 3
        if registers[2] > 10000000 and registers[5] > registers[2] and registers[1] > 4:
            registers[1] = registers[2] - 3
        pc = registers[ip] + 1
    return registers[0]


check:
    @[
        "seti 5 0 1",
        "seti 6 0 2",
        "addi 0 1 0",
        "addr 1 2 3",
        "setr 1 0 0",
        "seti 8 0 4",
        "seti 9 0 5",
    ].run(0) == 6

echo &"Part 1: {inputProg.run(inputIp, debug=false)}"
echo &"Part 2: {inputProg.run(inputIp, 1, debug=true)}"
