import sequtils
import strformat
import strutils
import tables
from unittest import check

import aoc
import coord

let input = input(day=20, year=2018)


template move(direction: untyped) =
    let newPos = pos.direction
    if newPos notin rooms:
        rooms[pos].add(newPos)
        rooms[newPos] = @[]
        depths[newPos] = depths[pos] + 1
    stack.add(newPos)


proc furthest(regex: string, debug: bool = false): tuple[part1: int, part2: int] =
    var
        rooms = initTable[Coord, seq[Coord]]()
        depths = initTable[Coord, int]()
        stack = @[[0, 0]]
    rooms[[0, 0]] = @[]
    depths[[0, 0]] = 0
    for cha in regex:
        let pos = stack.pop()
        case cha:
            of '^': stack.add(pos)
            of '$': break
            of '(': stack.add(@[pos, pos])
            of ')': discard
            of '|': stack.add(stack[^1])
            of 'N': move(up)
            of 'E': move(right)
            of 'S': move(down)
            of 'W': move(left)
            else: echo "Error!"
        if debug: pause(&"{cha}: {stack} {rooms}")

    let finalDepths = toSeq(depths.values)
    result.part1 = finalDepths.max
    result.part2 = finalDepths.filterIt(it >= 1000).len


check:
    "^WNE$".furthest() == (3, 0)
    "^S(E|W|)$".furthest() == (2, 0)
    "^ENWWW(NEEE|SSE(EE|N))$".furthest() == (10, 0)
    "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$".furthest() == (18, 0)
    "^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$".furthest() == (23, 0)
    "^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$".furthest() == (31, 0)

let (p1, p2) = input.furthest()
echo &"Part 1: {p1}"
echo &"Part 2: {p2}"
