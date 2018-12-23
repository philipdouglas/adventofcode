from copy import deepcopy


def coord(value, offset, limit, stuck_lights=False):
    """
    >>> coord(0, -1, 100)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    IndexError: out of bounds
    >>> coord(99, 1, 100)
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    IndexError: out of bounds
    >>> coord(98, 1, 100)
    99
    """
    value = value + offset
    if value < 0 or value >= limit:
        raise IndexError("out of bounds")
    return value


def advance(grid, stuck_lights=False):
    """
    >>> a = advance([['.', '#', '.', '#', '.', '#'], ['.', '.', '.', '#', '#', '.'], ['#', '.', '.', '.', '.', '#'], ['.', '.', '#', '.', '.', '.'], ['#', '.', '#', '.', '.', '#'], ['#', '#', '#', '#', '.', '.']])
    >>> a
    [['.', '.', '#', '#', '.', '.'], ['.', '.', '#', '#', '.', '#'], ['.', '.', '.', '#', '#', '.'], ['.', '.', '.', '.', '.', '.'], ['#', '.', '.', '.', '.', '.'], ['#', '.', '#', '#', '.', '.']]
    """
    new_grid = deepcopy(grid)
    for x in range(len(grid)):
        for y in range(len(grid)):
            on_count = 0
            for xoffset in range(-1, 2):
                for yoffset in range(-1, 2):
                    if xoffset == 0 and yoffset == 0:
                        continue
                    try:
                        if grid[coord(x, xoffset, len(grid), stuck_lights)][coord(y, yoffset, len(grid), stuck_lights)] == '#':
                            on_count += 1
                        # print('x: {} y: {} value: {}'.format(x + xoffset, y + yoffset, grid[x + xoffset][y + yoffset]))
                    except IndexError:
                        # print('x: {} y: {} value: {}'.format(x + xoffset, y + yoffset, 'x'))
                        pass
            if not stuck_lights or x not in [0, len(grid) - 1] or y not in [0, len(grid) - 1]:
                if grid[x][y] == '#' and on_count not in [2, 3]:
                    new_grid[x][y] = '.'
                elif grid[x][y] == '.' and on_count == 3:
                    new_grid[x][y] = '#'
    return new_grid


def adventofcode(part2=False):
    with open('18.txt') as input_file:
        grid = [[char for char in line.strip()] for line in input_file.readlines()]
        # Stuck lights are on by default in my input

    for _ in range(100):
        grid = advance(grid, part2)

    total = 0
    for row in grid:
        for cell in row:
            if cell == '#':
                total += 1
    return total

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print(adventofcode())
    print(adventofcode(True))
