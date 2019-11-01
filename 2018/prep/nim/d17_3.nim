import tables
from unittest import check

type Coord* = array[2, int]

proc x*(coord: Coord): int =
    return coord[0]

proc y*(coord: Coord): int =
    return coord[1]

proc `+`*(a: Coord, b: Coord): Coord =
    return [a.x + b.x, a.y + b.y]

proc `+=`*(a: var Coord, b: Coord) =
    a = a + b


const
    input = 265149
    directions: array[4, Coord] = [[1, 0], [0, 1], [-1, 0], [0, -1]]

proc manhatten_dist(pos: Coord): int =
    return pos[0].abs + pos[1].abs

iterator coords(): Coord =
    var
        pos: Coord = [0, 0]
        counter = 2
    yield pos
    while true:
        for direction in directions:
            for _ in 1..(counter div 2):
                pos += direction
                yield pos
            counter += 1

proc part1(dest: int): int =
    var curr = 1
    for coord in coords():
        if curr == dest:
            return coord.manhattenDist
        curr += 1

proc part2(dest: int): int =
    var seen = initTable[Coord, int]()
    for coord in coords():
        var value = 0
        for dx in -1..1:
            for dy in -1..1:
                value += seen.getOrDefault(coord + [dx, dy])
        if value == 0:
            value = 1
        if value > dest:
            return value
        seen[coord] = value

var a: Coord = [1, 3]
a += [-4, 8]
check:
    [1, 2] + [3, 4] == [4, 6]
    [1, 2] + [-3, 4] == [-2, 6]
    [1, 2] + [-3, 4] == [-2, 6]

    a == [-3, 11]

    manhatten_dist([1, 2]) == 3
    manhatten_dist([-1, 2]) == 3
    manhatten_dist([-1, -5]) == 6

    part1(1) == 0
    part1(12) == 3
    part1(23) == 2
    part1(1024) == 31

    part2(1) == 2
    part2(2) == 4
    part2(4) == 5
    part2(30) == 54
    part2(360) == 362

input.part1.echo
input.part2.echo
