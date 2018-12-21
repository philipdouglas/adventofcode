import strformat
import strutils
import sugar
import intsets
from unittest import check
import nimprof

import aoc
from day19 import execute, parseInstructions, Inst

let
    input = input(day=21, year=2018).split("\n")
    inputIp = ord(input[0][4]) - ord('0')
    inputProg = input[1..^1]


proc step(program: seq[Inst], ip: int, regs: var array[6, int], debug: bool=false) =
    let inst = program[regs[ip]]
    if debug: pause(&"pc={regs[ip]} {regs} {inst}")
    regs = execute(inst, regs)
    if debug: pause(&"Result: {regs}")
    regs[ip] += 1


proc analyse(program: seq[string], ip: int, debug: bool=false): tuple[p1: int, p2: int] =
    var
        program = parseInstructions(program)
        regs: array[6, int]
        zeroes = initIntSet()
        prevZero: int
    while regs[ip] >= 0 and regs[ip] <= program.high:
        step(program, ip, regs, debug)
        if regs[ip] == 28:
            if result.p1 == 0:
                result.p1 = regs[5]
            if regs[5] in zeroes:
                result.p2 = prevZero
                break
            zeroes.incl(regs[5])
            prevZero = regs[5]


let (p1, p2) = inputProg.analyse(inputIp, debug=false)
echo &"Part 1: {p1}"
echo &"Part 2: {p2}"
