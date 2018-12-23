"To continue, please consult the code grid in the manual.  Enter the code at row 2947, column 3029."


def calc_value(num):
    """
    >>> calc_value(1)
    20151125
    >>> calc_value(2)
    31916031
    >>> calc_value(3)
    18749137
    >>> calc_value(4)
    16080970
    >>> calc_value(5)
    21629792
    >>> calc_value(6)
    17289845
    >>> calc_value(61)
    27995004
    >>> calc_value(21)
    33511524
    """
    value = 20151125
    count = 1
    while count < num:
        value = (value * 252533) % 33554393
        count += 1
    return value


def coord_to_num(x, y):
    """
    >>> coord_to_num(1, 1)
    1
    >>> coord_to_num(1, 2)
    2
    >>> coord_to_num(2, 1)
    3
    >>> coord_to_num(3, 4)
    18
    >>> coord_to_num(6, 6)
    61
    """
    triangle_length = (x - 1) + (y - 1)
    return ((triangle_length * (triangle_length + 1)) // 2) + x


def adventofcodefast():
    return calc_value(coord_to_num(3029, 2947))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print(adventofcodefast())
