import strformat
import strutils
import sugar
from unittest import check

let input = readFile("2017/.cache/input_2017_9").strip

type
    Mode = enum group, garbage, skip

proc score(stream: string, clean = false): int =
    var
        group = 0
        mode = Mode.group
    for cha in stream:
        if mode == Mode.group:
            case cha:
            of '{': group += 1
            of '}':
                if not clean: result += group
                group -= 1
            of '<': mode = Mode.garbage
            of ',': continue
            else: echo &"Unhandled char: {cha}"
        elif mode == Mode.garbage:
            case cha:
            of '>': mode = Mode.group
            of '!': mode = Mode.skip
            else:
                if clean: result += 1
        elif mode == Mode.skip:
            mode = Mode.garbage

check:
    "<>".score == 0
    "{}".score == 1
    "{{{}}}".score == 6
    "{{},{}}".score == 5
    "{{{},{},{{}}}}".score == 16
    "{<a>,<a>,<a>,<a>}".score == 1
    "{{<ab>},{<ab>},{<ab>},{<ab>}}".score == 9
    "{{<!!>},{<!!>},{<!!>},{<!!>}}".score == 9
    "{{<a!>},{<a!>},{<a!>},{<ab>}}".score == 3

    "<>,".score(true) == 0
    "<random characters>,".score(true) == 17
    "<<<<>,".score(true) == 3
    "<{!>}>,".score(true) == 2
    "<!!>,".score(true) == 0
    "<!!!>>,".score(true) == 0
    "<{o\"i!a,<{i<a>,".score(true) == 10

echo &"Part 1: {input.score}"
echo &"Part 2: {input.score(true)}"
