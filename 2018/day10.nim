import sequtils
import strformat
import strutils
import strscans
from unittest import check

import aoc
import coord


proc parse(lines: seq[string]): tuple[pos, vel: seq[Coord]] =
    for line in lines:
        var px, py, vx, vy: int
        discard line.scanf("position=<$s$i,$s$i>$svelocity=<$s$i,$s$i>", px, py, vx, vy)
        result.pos.add([px, py])
        result.vel.add([vx, vy])

let
    testInput = @[
        "position=< 9,  1> velocity=< 0,  2>",
        "position=< 7,  0> velocity=<-1,  0>",
        "position=< 3, -2> velocity=<-1,  1>",
        "position=< 6, 10> velocity=<-2, -1>",
        "position=< 2, -4> velocity=< 2,  2>",
        "position=<-6, 10> velocity=< 2, -2>",
        "position=< 1,  8> velocity=< 1, -1>",
        "position=< 1,  7> velocity=< 1,  0>",
        "position=<-3, 11> velocity=< 1, -2>",
        "position=< 7,  6> velocity=<-1, -1>",
        "position=<-2,  3> velocity=< 1,  0>",
        "position=<-4,  3> velocity=< 2,  0>",
        "position=<10, -3> velocity=<-1,  1>",
        "position=< 5, 11> velocity=< 1, -2>",
        "position=< 4,  7> velocity=< 0, -1>",
        "position=< 8, -2> velocity=< 0,  1>",
        "position=<15,  0> velocity=<-2,  0>",
        "position=< 1,  6> velocity=< 1,  0>",
        "position=< 8,  9> velocity=< 0, -1>",
        "position=< 3,  3> velocity=<-1,  1>",
        "position=< 0,  5> velocity=< 0, -1>",
        "position=<-2,  2> velocity=< 2,  0>",
        "position=< 5, -2> velocity=< 1,  2>",
        "position=< 1,  4> velocity=< 2,  1>",
        "position=<-2,  7> velocity=< 2, -2>",
        "position=< 3,  6> velocity=<-1, -1>",
        "position=< 5,  0> velocity=< 1,  0>",
        "position=<-6,  0> velocity=< 2,  0>",
        "position=< 5,  9> velocity=< 1, -2>",
        "position=<14,  7> velocity=<-2,  0>",
        "position=<-3,  6> velocity=< 2, -1>",
    ].parse()
    input = input(day=10, year=2018).split("\n").parse()


iterator time(positions, velocities: seq[Coord]): seq[Coord] =
    var positions = positions
    while true:
        positions += velocities
        yield positions


proc render(positions: seq[Coord]): string =
    for y in positions.ymin..positions.ymax:
        for x in positions.xmin..positions.xmax:
            if [x, y] in positions:
                result.add('#')
            else:
                result.add(' ')
        result.add('\n')


proc read(positions, velocities: seq[Coord]): tuple[part1: string, part2: int] =
    var
        prevDistance = manhattenDist(positions.min, positions.max)
        prevPos = positions
    for pos in positions.time(velocities):
        let newDistance = manhattenDist(pos.min, pos.max)
        if newDistance > prevDistance:
            result.part1 = prevPos.render()
            return
        result.part2.inc
        prevDistance = newDistance
        prevPos = pos

check:
    read(testInput.pos, testInput.vel) == ("#   #  ###\n#   #   # \n#   #   # \n#####   # \n#   #   # \n#   #   # \n#   #   # \n#   #  ###\n", 3)

let answer = read(input.pos, input.vel)
echo &"Part 1:\n{answer.part1}"
echo &"Part 2: {answer.part2}"
