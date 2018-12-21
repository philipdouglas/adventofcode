import strformat
import strutils
import sugar
import intsets
from unittest import check

import aoc
from day19 import execute, parseInstructions, Inst

let
    input = input(day=21, year=2018).split("\n")
    inputIp = ord(input[0][4]) - ord('0')
    inputProg = input[1..^1]


proc run(program: seq[string], ip: int, init0: int=0, debug: bool=false): int =
    var
        program = parseInstructions(program)
        registers: array[6, int]
        pc: int
    registers[0] = init0
    while pc >= 0 and pc <= program.high and pc != 28:
        registers[ip] = pc
        let inst = program[pc]
        if debug: pause(&"pc={pc} {registers} {inst}")
        registers = execute(inst, registers)
        if debug: pause(&"Result: {registers}")
        pc = registers[ip] + 1
    return registers[5]


proc part2(program: seq[string], ip: int, init0: int=0, debug: bool=false): int =
    var
        program = parseInstructions(program)
        registers: array[6, int]
        pc: int
        zeroes = initIntSet()
        prevZero: int
    registers[0] = init0
    while pc >= 0 and pc <= program.high:
        registers[ip] = pc
        let inst = program[pc]
        if debug: pause(&"pc={pc} {registers} {inst}")
        registers = execute(inst, registers)
        if debug: pause(&"Result: {registers}")
        pc = registers[ip] + 1
        if pc == 28:
            if registers[5] in zeroes:
                return prevZero
            zeroes.incl(registers[5])
            prevZero = registers[5]


echo &"Part 1: {inputProg.run(inputIp, debug=false)}"
echo &"Part 2: {inputProg.part2(inputIp, debug=false)}"
