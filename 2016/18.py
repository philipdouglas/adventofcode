TEST_ROW = '..^^.'
ROW1 = '.^..^....^....^^.^^.^.^^.^.....^.^..^...^^^^^^.^^^^.^.^^^^^^^.^^^^^..^.^^^.^^..^.^^.^....^.^...^^.^.'

UNSAFE = (
    '^^.',
    '.^^',
    '^..',
    '..^',
)

def is_safe(col, previous_row):
    """
    >>> is_safe(0, TEST_ROW)
    True
    >>> is_safe(1, TEST_ROW)
    False
    >>> is_safe(2, TEST_ROW)
    False
    >>> is_safe(3, TEST_ROW)
    False
    >>> is_safe(4, TEST_ROW)
    False
    """
    lower = col - 1
    upper = col + 1
    above = previous_row[max(lower, 0):upper + 1]
    if lower < 0:
        above = '.' + above
    if upper >= len(previous_row):
        above = above + '.'
    return above not in UNSAFE


def generate_row(previous_row):
    """
    >>> row2 = generate_row(TEST_ROW)
    >>> row2
    '.^^^^'
    >>> row3 = generate_row(row2)
    >>> row3
    '^^..^'
    """
    new_row = ''
    for index in range(len(previous_row)):
        new_row += '.' if is_safe(index, previous_row) else '^'
    return new_row


def get_safe_tiles(row1, rowmax=40):
    """
    >>> get_safe_tiles('.^^.^.^^^^', rowmax=10)
    38
    """
    previous_row = row1
    row_count = 1
    safe_count = previous_row.count('.')
    while row_count < rowmax:
        previous_row = generate_row(previous_row)
        row_count += 1
        safe_count += previous_row.count('.')
    return safe_count


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("Part 1: {}".format(get_safe_tiles(ROW1)))
    print("Part 1: {}".format(get_safe_tiles(ROW1, rowmax=400000)))
