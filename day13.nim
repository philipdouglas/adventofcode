import algorithm
import sequtils
import strformat
import strutils
import sugar
import tables
from unittest import check

import aoc
import coord

let input = input(day=13, year=2018).split("\n")


type
    TurnDirection = enum left, straight, right
    Cart = ref object
        heading: Coord
        nextDirection: TurnDirection


template `[]`(map: seq[string], coord: Coord): char =
    map[coord.y][coord.x]


proc `$`(cart: Cart): string =
    if cart.heading == [0, 1]: return &"v"
    elif cart.heading == [1, 0]: return &">"
    elif cart.heading == [0, -1]: return &"^"
    elif cart.heading == [-1, 0]: return &"<"
    else: return &"!"


proc initCart(heading: Coord): Cart =
    new(result)
    result.heading = heading
    result.nextDirection = left


proc newHeading(cart: var Cart, track: char) =
    case track:
        of '+':
            case cart.nextDirection:
                of left:
                    cart.heading = cart.heading.rotateLeft()
                    cart.nextDirection = straight
                of straight:
                    cart.nextDirection = right
                of right:
                    cart.heading = cart.heading.rotateRight()
                    cart.nextDirection = left
                else: echo "BAD DIRECTION"
        of '/':
            if cart.heading.x == 0:
                cart.heading = cart.heading.rotateRight()
            else:
                cart.heading = cart.heading.rotateLeft()
        of '\\':
            if cart.heading.x == 0:
                cart.heading = cart.heading.rotateLeft()
            else:
                cart.heading = cart.heading.rotateRight()
        else: return


proc collision(map: seq[string], part2: bool = false): string =
    var carts = initTable[Coord, Cart]()
    for pos in [0,0]..<[map[0].len, map.len]:
        case map[pos]:
            of '^': carts[pos] = initCart([0, -1])
            of '<': carts[pos] = initCart([-1, 0])
            of 'v': carts[pos] = initCart([0, 1])
            of '>': carts[pos] = initCart([1, 0])
            else: continue
    while true:
        for pos in toSeq(carts.keys).sorted(cmp):
            if pos notin carts:
                continue
            var currentCart = carts[pos]
            carts.del(pos)
            let newPos = pos + currentCart.heading
            if newPos in carts:
                if not part2:
                    return $newPos
                else:
                    carts.del(newPos)
                    continue
            currentCart.newHeading(map[newPos])
            carts[newPos] = currentCart
        if carts.len == 1:
            return $toSeq(carts.keys)[0]


check:
    @[
        r"/->-\        ",
        r"|   |  /----\",
        r"| /-+--+-\  |",
        r"| | |  | v  |",
        r"\-+-/  \-+--/",
        r"  \------/   ",
    ].collision() == "7,3"
    @[
        r"/>-<\  ",
        r"|   |  ",
        r"| /<+-\",
        r"| | | v",
        r"\>+</ |",
        r"  |   ^",
        r"  \<->/",
    ].collision(true) == "6,4"

echo &"Part 1: {input.collision()}"
echo &"Part 1: {input.collision(part2=true)}"
