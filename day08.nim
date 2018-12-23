import math
import sequtils
import strformat
import strutils
import sugar
from unittest import check

import aoc

let input = input(day=8, year=2018).split(" ").map(parseInt)
type Node = ref object
    children: seq[Node]
    value: int


proc initNode(): Node =
    new(result)


template peek[T](s: seq[T]): T =
    s[s.high]


proc checksum(data: seq[int]): tuple[sum: int, rootValue: int] =
    var
        index = 2
        childStack = @[data[0]]
        metaStack = @[data[1]]
        root = initNode()
        nodeStack = @[root]
    while childStack.len > 0:
        let children = childStack.pop()
        if children > 0:
            childStack.add(children - 1)
            childStack.add(data[index])
            metaStack.add(data[index + 1])
            index += 2
            let newNode = initNode()
            nodeStack.peek().children.add(newNode)
            nodeStack.add(newNode)
        else:
            let
                metalen = metaStack.pop()
                meta = data[index..<index + metalen]
                metasum = sum(meta)
                node = nodeStack.pop()
            if node.children.len == 0:
                node.value = metasum
            else:
                for i in meta:
                    if i <= node.children.len:
                        node.value += node.children[i - 1].value
            result.sum += metasum
            index += metalen
    result.rootValue = root.value



check:
    @[2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2].checksum() == (138, 66)

let answer = input.checksum()
echo &"Part 1: {answer.sum}"
echo &"Part 2: {answer.rootValue}"
