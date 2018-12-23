import macros
import re
import sequtils
import strformat
import strutils
import sugar
import tables
from unittest import check


let
    input = readFile("2017/.cache/input_2017_8").strip.split('\n')
    pattern = re"([a-z]+) (inc|dec) (-?\d+) if ([a-z]+) ([<>=!]+) (-?\d+)"


proc execute(program: seq[string]): auto =
    var
        registers = initTable[string, int]()
        highestValue = 0
    for line in program:
        var
            matches: array[6, string]
            runLine: bool
        discard line.find(pattern, matches)
        let
            condRegVal = registers.mgetOrPut(matches[3], 0)
            condVal = matches[5].parseInt
        case matches[4]
            of "==": runLine = condRegVal == condVal
            of "!=": runLine = condRegVal != condVal
            of ">": runLine = condRegVal > condVal
            of "<": runLine = condRegVal < condVal
            of ">=": runLine = condRegVal >= condVal
            of "<=": runLine = condRegVal <= condVal
        if runLine:
            let
                opValReg = registers.getOrDefault(matches[0], 0)
                opVal = matches[2].parseInt
            case matches[1]:
                of "inc": registers[matches[0]] = opValReg + opVal
                of "dec": registers[matches[0]] = opValReg - opVal
            if registers[matches[0]] > highestValue:
                highestValue = registers[matches[0]]

    var values: seq[int]
    for value in registers.values: values.add(value)
    return (values.max, highestValue)

check:
    @[
        "b inc 5 if a > 1",
        "a inc 1 if b < 5",
        "c dec -10 if a >= 1",
        "c inc -20 if c == 10",
    ].execute == (1, 10)

echo input.execute
