from coord import Coord, BlockCoord


def walk(instructions):
    """
    >>> walk("R2, L3")
    (5, None)
    >>> walk("R2, R2, R2")
    (2, None)
    >>> walk("R5, L5, R5, R3")
    (12, None)
    >>> walk("R8, R4, R4, R8")
    (8, 4)
    """
    position = BlockCoord(0, 0)
    heading = Coord(0, 1)
    visited = set((position, ))
    part2 = None
    for instruction in instructions.strip().split(', '):
        if instruction[0] == 'R':
            heading = heading.rotate_right()
        elif instruction[0] == 'L':
            heading = heading.rotate_left()
        for step in range(int(instruction[1:])):
            position += heading
            if part2 is None and position in visited:
                part2 = position
            visited.add(position)
    return (position.distance_blocks(), part2.distance_blocks() if part2 else None)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    with open('1input.txt', 'r') as inputfile:
        print("Part 1: {0}\nPart 2: {1}".format(*walk(inputfile.read())))
