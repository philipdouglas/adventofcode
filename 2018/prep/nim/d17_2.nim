import algorithm
import sequtils
import strutils
import sugar
from unittest import check

let input = strip(readFile("2017/.cache/input_2017_2"))
var rows: seq[seq[int]] = map(
    split(input, '\n'), (line) => map(split(line, '\t'), parseInt))

proc rowScore1(row: seq[int]): int =
    var row: seq[int] = sorted(row, system.cmp[int])
    return row[high(row)] - row[0]

proc rowScore2(row: seq[int]): int =
    var row: seq[int] = sorted(row, system.cmp[int], order=SortOrder.Descending)
    for i, first in row:
        for j in (i + 1)..<len(row):
            if first mod row[j] == 0:
                return first div row[j]

proc scoreSum(rows: seq[seq[int]], scoreProc: (seq[int]) -> int): int =
    for row in rows:
        result += scoreProc(row)

check:
    rowScore1(@[5, 1, 9, 5]) == 8
    rowScore1(@[7, 5, 3]) == 4
    rowScore1(@[2, 4, 6, 8]) == 6
    scoreSum(@[
        @[5, 1, 9, 5],
        @[7, 5, 3],
        @[2, 4, 6, 8],
    ], rowScore1) == 18


    rowScore2(@[5, 9, 2, 8]) == 4
    rowScore2(@[9, 4, 7, 3]) == 3
    rowScore2(@[3, 8, 6, 5]) == 2
    scoreSum(@[
        @[5, 9, 2, 8],
        @[9, 4, 7, 3],
        @[3, 8, 6, 5],
    ], rowScore2) == 9

echo scoreSum(rows, rowScore1)
echo scoreSum(rows, rowScore2)
