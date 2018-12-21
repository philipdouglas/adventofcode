import strformat
import strutils
import sugar
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


echo &"Part 1: {inputProg.run(inputIp, debug=false)}"

# var a, b, d, e, f: int
# while f == 0:
#     b = f or 65536
#     f = 10678677
#     e = b and 255
#     f = f + e
#     f = f and 16777215
#     f = f * 65899
#     f = f and 16777215
#     e = int(256 > b)
#     while e == 0:
#         e = 0
#         d = e + 1
#         d = d * 256
#         d = int(d > b)

# r = [1, 65536, 18, 0, 0, 10587719]
# while True:

#     if r[1] > 256:
