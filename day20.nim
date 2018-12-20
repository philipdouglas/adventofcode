import queues
import sequtils
import sets
import strformat
import strutils
import sugar
import tables
from unittest import check

import aoc
import coord

let input = input(day=20, year=2018)


proc furthest(regex: string, debug: bool = false): tuple[part1: int, part2: int] =
    # var
    #     branches: seq[seq[seq[Coord]]] = @[@[@[[0, 0]]]]
    # for cha in regex:
    #     let pos = branches[^1][^1][^1]
    #     case cha:
    #         of '^': continue
    #         of '$': return branches[0][0]
    #         of '(': branches.add(@[@[@[pos]]])
    #         of ')':
    #             let fin = branches.pop().max
    #             branches[^1][^1] += fin
    #         of '|': branches[^1].add(@[0])
    #         else: branches[^1][^1].inc
    #     if debug: pause(&"{cha}: {branches}")
    var
        rooms = initTable[Coord, seq[Coord]]()
        stack = @[[0, 0]]
        depths = initTable[Coord, int]()
    rooms[[0, 0]] = @[]
    depths[[0, 0]] = 0
    for cha in regex:
        let
            pos = stack.pop()
            depth = depths[pos]
        case cha:
            of '^': stack.add(pos)
            of '$': break
            of '(':
                stack.add(pos)
                stack.add(pos)
            of ')': discard
            of '|':
                stack.add(stack[^1])
            of 'N':
                let newPos = pos.up
                if newPos notin rooms:
                    rooms[pos].add(newPos)
                    rooms[newPos] = @[]
                    depths[newPos] = depth + 1
                stack.add(newPos)
            of 'E':
                let newPos = pos.right
                if newPos notin rooms:
                    rooms[pos].add(newPos)
                    rooms[newPos] = @[]
                    depths[newPos] = depth + 1
                stack.add(newPos)
            of 'S':
                let newPos = pos.down
                if newPos notin rooms:
                    rooms[pos].add(newPos)
                    rooms[newPos] = @[]
                    depths[newPos] = depth + 1
                stack.add(newPos)
            of 'W':
                let newPos = pos.left
                if newPos notin rooms:
                    rooms[pos].add(newPos)
                    rooms[newPos] = @[]
                    depths[newPos] = depth + 1
                stack.add(newPos)
            else: echo "Error!"
        if debug: pause(&"{cha}: {stack} {rooms}")
    if debug: echo rooms

    # var
    #     open = initQueue[Coord]()
    #     closed = initSet[Coord]()
    #     depths = initTable[Coord, int]()
    #     deepest = 0
    #     # deepestPos = [0, 0]
    # open.enqueue([0, 0])
    # depths[[0, 0]] = 0
    # while open.len > 0:
    #     let
    #         curr = open.dequeue()
    #         depth = depths[curr]
    #     if depth > deepest:
    #         deepest = depth
    #         # deepestPos = curr
    #     for child in rooms[curr]:
    #         if child notin closed:
    #             open.add(child)
    #             depths[child] = depth + 1
    #     closed.incl(curr)
    # return deepest
    result.part1 = toSeq(depths.values).max
    result.part2 = toSeq(depths.values).filterIt(it >= 1000).len



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
