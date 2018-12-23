def is_possible(sides):
    """
    >>> is_possible((5, 10, 25))
    False
    >>> is_possible((3, 3, 4))
    True
    """
    for side in sides:
        if sum(other for other in sides if other != side) <= side:
            return False
    return True


def count_triangles(lines, generator):
    count = 0
    for triangle in generator(lines):
        count += 1 if is_possible(triangle) else 0
    return count


def row_generator(lines):
    for line in lines:
        yield tuple(int(edge) for edge in line.split(' ') if edge)


def col_generator(lines):
    for index in range(0, len(lines), 3):
        triplet = tuple(row_generator(lines[index:index + 3]))
        for index in range(0, 3):
            yield tuple(edges[index] for edges in triplet)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    with open('3input.txt', 'r') as inputfile:
        lines = inputfile.readlines()
        print("Part 1: {}".format(count_triangles(lines, row_generator)))
        print("Part 2: {}".format(count_triangles(lines, col_generator)))
