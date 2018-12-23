import sequtils
import strutils
import sugar
from unittest import check

let input = readFile("2017/.cache/input_2017_5").strip.split('\n').map(parseInt)


proc run(program: seq[int], part: int = 1): int =
    var
        pos = 0
        program = program
    while pos < len(program):
        let jump = program[pos]
        if part == 1:
            program[pos] = jump + 1
        else:
            if jump >= 3:
                program[pos] = jump - 1
            else:
                program[pos] = jump + 1
        pos += jump
        result += 1

check:
    run(@[0, 3, 0, 1, -3], 1) == 5
    run(@[0, 3, 0, 1, -3], 2) == 10

echo run(input, 1)
echo run(input, 2)
