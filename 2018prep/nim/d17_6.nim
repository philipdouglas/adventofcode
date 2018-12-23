import hashes
import sequtils
import strformat
import strutils
import sugar
import tables
from unittest import check

let input = readFile("2017/.cache/input_2017_6").strip.split('\t').map(parseInt)


proc realloc(blocks: seq[int]): seq[int] =
    var
        blocks = blocks
        biggest_num = 0
        biggest_index = 0
    for index, blck in blocks:
        if blck > biggest_num:
            biggest_num = blck
            biggest_index = index
    blocks[biggest_index] = 0
    let
        allinc = biggest_num div blocks.len
        overflow = biggest_num mod blocks.len
    for index, blck in blocks:
        blocks[index] = blck + allinc
        var offset = index - biggest_index
        if offset <= 0: offset += blocks.len
        if offset <= overflow: blocks[index] += 1
    return blocks


proc repair(blocks: seq[int]): (int, int) =
    var
        blocks = blocks
        blocks_hash = blocks.hash
        seen = initTable[int, int]()
        count = 0
    while blocks_hash notin seen:
        count += 1
        seen[blocks_hash] = count
        blocks = blocks.realloc
        blocks_hash = blocks.hash
    return (seen.len, (seen.len - seen[blocks_hash] + 1))


check:
    realloc(@[0, 2, 7, 0]) == @[2, 4, 1, 2]
    realloc(@[2, 4, 1, 2]) == @[3, 1, 2, 3]
    realloc(@[3, 1, 2, 3]) == @[0, 2, 3, 4]
    realloc(@[0, 2, 3, 4]) == @[1, 3, 4, 1]
    realloc(@[1, 3, 4, 1]) == @[2, 4, 1, 2]

    repair(@[0, 2, 7, 0]) == (5, 4)

let output = input.repair
echo &"Part 1: {output[0]}"
echo &"Part 2: {output[1]}"
