def read_seq(sequence):
    """
    >>> read_seq('1')
    '11'
    >>> read_seq('11')
    '21'
    >>> read_seq('21')
    '1211'
    >>> read_seq('1211')
    '111221'
    >>> read_seq('111221')
    '312211'
    """
    new_seq = []
    index = 0
    while index < len(sequence):
        count = 1
        try:
            while sequence[index + 1] == sequence[index]:
                count += 1
                index += 1
        except IndexError:
            pass
        new_seq += [str(count), sequence[index]]
        index += 1
    return ''.join(new_seq)


def adventofcode(seed, repetitions):
    """
    >>> adventofcode('1', 5)
    '312211'
    """
    for _ in range(repetitions):
        seed = read_seq(seed)
    return seed

if __name__ == "__main__":
    # import doctest
    # doctest.testmod()
    print(len(adventofcode('1321131112', 40)))
    print(len(adventofcode('1321131112', 50)))
