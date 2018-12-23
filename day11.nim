import strformat
import strutils
import sugar
import tables
from unittest import check
# import nimprof

import aoc
import coord

let input = 7400
type SumTable = array[0..300, array[0..300, int]]


template `[]`(sums: SumTable, coord: Coord): int =
    sums[coord.x][coord.y]


template `[]=`(sums: var SumTable, coord: Coord, value: int) =
    sums[coord.x][coord.y] = value


template powerLevel(cell: Coord, serialno: int): int =
    let rackID = cell.x + 10
    (((((rackID * cell.y) + serialno) * rackID) div 100) mod 10) - 5


proc sumTable(serialno: int): SumTable =
    for c in [1, 1]..[300, 300]:
        let prev = result[c - [0, 1]] + result[c - [1, 0]] - result[c - [1, 1]]
        result[c] = c.powerLevel(serialno) + prev


proc largestNSquare(n, serialno: int, sums: SumTable): tuple[size: int, coord: Coord] =
    for D in [n, n]..([301, 301] - [n, n]):
        let
            A = D.diag(-n)
            B = D.left(n)
            C = D.up(n)
            total = sums[D] + sums[A] - sums[B] - sums[C]
        if total > result.size:
            result.size = total
            result.coord = A.diag()


proc largestNSquare(n, serialno: int): string =
    return $largestNSquare(n, serialno, sumTable(serialno)).coord


proc largestSquare(serialno: int): string =
    let sums = sumTable(serialno)
    var
        biggest = 0
        biggestCoord: Coord
        biggestSize = 0
    for n in countdown(300, 1, 1):
        let square = largestNSquare(n, serialno, sums)
        if square.size > biggest:
            biggest = square.size
            biggestCoord = square.coord
            biggestSize = n
    return &"{biggestCoord},{biggestSize}"


check:
    [3, 5].powerLevel(8) == 4
    [122, 79].powerLevel(57) == -5
    [217, 196].powerLevel(39) == 0
    [101, 153].powerLevel(71) == 4

    largestNSquare(3, 18) == "33,45"
    largestNSquare(3, 42) == "21,61"

    largestSquare(18) == "90,269,16"
    largestSquare(42) == "232,251,12"

echo &"Part 1: {largestNSquare(3, input)}"
echo &"Part 2: {largestSquare(input)}"
