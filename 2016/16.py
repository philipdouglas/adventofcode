def onepad(a):
    """
    >>> onepad('1')
    '100'
    >>> onepad('0')
    '001'
    >>> onepad('11111')
    '11111000000'
    >>> onepad('111100001010')
    '1111000010100101011110000'
    """
    b = a[::-1].replace('1', '2').replace('0', '1').replace('2', '0')
    return a + '0' + b


def pad(a, length):
    """
    >>> pad('10000', 20)
    '10000011110010000111'
    """
    while len(a) < length:
        a = onepad(a)
    return a[:length]


def checksum(data):
    """
    >>> checksum('110010110100')
    '100'
    """
    while len(data) % 2 == 0:
        data = ['1' if data[index] == data[index + 1] else '0'
                for index in range(0, len(data), 2)]
    return ''.join(data)


def fill_disk(initial, length):
    """
    >>> fill_disk('10000', 20)
    '01100'
    """
    return checksum(pad(initial, length))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("Test 1: {}".format(fill_disk('10111100110001111', 272)))
    print("Test 2: {}".format(fill_disk('10111100110001111', 35651584)))
