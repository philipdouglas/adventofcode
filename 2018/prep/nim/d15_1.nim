import strutils
import sugar
from unittest import check

let input = readFile("2015/1input.txt").strip

proc whatFloor(instructions: string): int =
    for instruction in instructions:
        if instruction == '(':
            result += 1
        elif instruction == ')':
            result -= 1

proc whenBasement(instructions: string): int =
    for position, instruction in instructions:
        if instruction == '(':
            result += 1
        elif instruction == ')':
            result -= 1
        if result < 0:
            return position + 1

check:
    whatFloor("(())") == 0
    whatFloor("()()") == 0
    whatFloor("(((") == 3
    whatFloor("(()(()(") == 3
    whatFloor("))(((((") == 3
    whatFloor("())") == -1
    whatFloor("))(") == -1
    whatFloor(")))") == -3
    whatFloor(")())())") == -3

    whenBasement(")") == 1
    whenBasement("()())") == 5

echo whatFloor(input)
echo whenBasement(input)
