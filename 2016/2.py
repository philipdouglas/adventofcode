KEYPAD1 = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 9),
)
KEYPAD2 = (
    (None, None, 1, None, None),
    (None, 2, 3, 4, None),
    (5, 6, 7, 8, 9),
    (None, 'A', 'B', 'C', None),
    (None, None, 'D', None, None),
)


def find_five(keypad):
    for tryy in range(len(keypad)):
        for tryx in range(len(keypad[0])):
            if keypad[tryy][tryx] == 5:
                return tryx, tryy


def follow_instructions(keypad, instructions):
    """
    >>> follow_instructions(KEYPAD1, ['ULL', 'RRDDD', 'LURDL', 'UUUD'])
    '1985'
    >>> follow_instructions(KEYPAD2, ['ULL', 'RRDDD', 'LURDL', 'UUUD'])
    '5DB3'
    """
    x, y = find_five(keypad)

    def move(movx, movy):
        newx, newy = max(x + movx, 0), max(y + movy, 0)
        if keypad[newy][newx] is None:
            raise IndexError("Nope")
        else:
            return newx, newy

    result = ''
    for line in instructions:
        for char in line:
            try:
                if char == 'U':
                    x, y = move(0, -1)
                elif char == 'D':
                    x, y = move(0, 1)
                elif char == 'L':
                    x, y = move(-1, 0)
                elif char == 'R':
                    x, y = move(1, 0)
            except IndexError:
                pass
        result += str(keypad[y][x])
    return result


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    with open('2input.txt', 'r') as inputfile:
        instructions = inputfile.readlines()
        print("Part 1: {}".format(follow_instructions(KEYPAD1, instructions)))
        print("Part 2: {}".format(follow_instructions(KEYPAD2, instructions)))
