import sequtils
import strformat
import strscans
import sugar

type 
    Coord* = array[2, int]
    Coord3* = array[3, int]

template x*(coord: Coord): int =
    coord[0]

template y*(coord: Coord): int =
    coord[1]

template x*(coord: Coord3): int =
    coord[0]

template y*(coord: Coord3): int =
    coord[1]

template z*(coord: Coord3): int =
    coord[2]

template `+`*(a, b: Coord): Coord =
    [a.x + b.x, a.y + b.y]
template `-`*(a, b: Coord): Coord =
    [a.x - b.x, a.y - b.y]

template `+`*(a, b: Coord3): Coord3 =
    [a.x + b.x, a.y + b.y, a.z + b.z]
template `-`*(a, b: Coord3): Coord3 =
    [a.x - b.x, a.y - b.y, a.z - b.z]

template `+=`*(a: var Coord, b: Coord) =
    a = a + b

template `+=`*(a: var seq[Coord], b: seq[Coord]) =
    assert a.len == b.len
    for i in 0..<a.len:
        a[i] += b[i]

template `-=`*(a: var Coord, b: Coord) =
    a = a - b

template `-=`*(a: var seq[Coord], b: seq[Coord]) =
    assert a.len == b.len
    for i in 0..<a.len:
        a[i] -= b[i]

proc manhattenDist*(a, b: Coord = [0, 0]): int =
    let a = a - b
    return a.x.abs + a.y.abs

proc manhattenDist*(a, b: Coord3 = [0, 0, 0]): int =
    let a = a - b
    return a.x.abs + a.y.abs + a.z.abs

iterator `..`*(a, b: Coord): Coord =
    for x in (a.x)..(b.x):
        for y in (a.y)..(b.y):
            yield [x, y]

iterator `..<`*(a, b: Coord): Coord =
    for x in (a.x)..<(b.x):
        for y in (a.y)..<(b.y):
            yield [x, y]

template xmax*(coords: seq[Coord]): int =
    max(coords.map((c) => c.x))

template ymax*(coords: seq[Coord]): int =
    max(coords.map((c) => c.y))

template max*(coords: seq[Coord]): Coord =
    [xmax(coords), ymax(coords)]

template xmin*(coords: seq[Coord]): int =
    min(coords.map((c) => c.x))

template ymin*(coords: seq[Coord]): int =
    min(coords.map((c) => c.y))

template min*(coords: seq[Coord]): Coord =
    [xmin(coords), ymin(coords)]

proc minmax*(coords: seq[Coord]): tuple[xmin, xmax, ymin, ymax: int] =
    return (coords.xmin, coords.xmax, coords.ymin, coords.ymax)

proc parseCoord*(input: string): Coord =
    var x, y: int
    discard input.scanf("$i, $i", x, y)
    return [x, y]

proc `$`*(coord: Coord): string =
    return &"{coord.x},{coord.y}"


template left*(c: Coord = [0, 0], n: int = 1): Coord =
    c - [n, 0]


template right*(c: Coord = [0, 0], n: int = 1): Coord =
    c + [n, 0]


template up*(c: Coord = [0, 0], n: int = 1): Coord =
    c - [0, n]


template down*(c: Coord = [0, 0], n: int = 1): Coord =
    c + [0, n]


template diag*(c: Coord = [0, 0], n: int = 1): Coord =
    c + [n, n]

proc rotateLeft*(c: Coord): Coord =
    return [c.y, -c.x]

proc rotateRight*(c: Coord): Coord =
    return [-c.y, c.x]


proc cmp*(a, b: Coord): int =
    result = cmp(a.y, b.y)
    if result == 0:
        result = cmp(a.x, b.x)


template `[]`*[T](multiarray: seq[seq[T]], pos: Coord): T =
    multiarray[pos.y][pos.x]


when isMainModule:
    import unittest

    var
        plusEquals = [-1, 2]
        minusEquals = [3, 4]
    plusEquals += [2, 1]
    minusEquals -= [2, 1]

    check:
        [0, 0] + [1, 1] == [1, 1]
        [1, 0] + [1, 1] == [2, 1]

        [0, 0] - [1, 1] == [-1, -1]
        [1, 0] - [1, 1] == [0, -1]

        [1, 1] == [1, 1]
        not ([0, 0] == [1, 1])
        [1, 0] != [1, 1]

        [3, 4].x == 3
        [3, 4].y == 4

        [3, 4].manhattenDist == 7
        [-2, 5].manhattenDist == 7
        [-2, 5].manhattenDist([2, 5]) == 4
        [3, 4].manhattenDist([4, 5]) == 2

        plusEquals == [1, 3]
        minusEquals == [1, 3]

        @[[1, 2], [0, 1], [2, 3]].xmax == 2
        @[[1, 2], [0, 1], [2, 3]].ymax == 3
        @[[1, 2], [0, 1], [2, 3]].max == [2, 3]

        [0, 1].rotateLeft() == [1, 0]
        [0, 1].rotateRight() == [-1, 0]
        [1, 0].rotateLeft() == [0, -1]
        [1, 0].rotateRight() == [0, 1]

    var
        rangeInc: seq[Coord] = @[]
        rangeExcl: seq[Coord] = @[]
    for pos in [0, 0]..[2, 3]:
        rangeInc.add(pos)
    for pos in [0, 0]..<[2, 3]:
        rangeExcl.add(pos)

    check:
        rangeInc == @[[0, 0], [0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2], [1, 3], [2, 0], [2, 1], [2, 2], [2, 3]]
        rangeExcl == @[[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2]]
